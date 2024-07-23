import os
import requests
from urllib.parse import urlencode
from typing import Type, Any, Optional
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.base_tool import BaseTool


class SerplyNewsSearchToolSchema(BaseModel):
    """Serply 新闻搜索的输入。"""
    search_query: str = Field(..., description="要用于获取新闻文章的必填搜索查询")


class SerplyNewsSearchTool(BaseTool):
    name: str = "新闻搜索"
    description: str = "使用 search_query 执行新闻文章搜索的工具。"
    args_schema: Type[BaseModel] = SerplyNewsSearchToolSchema
    search_url: str = "https://api.serply.io/v1/news/"
    proxy_location: Optional[str] = "US"
    headers: Optional[dict] = {}
    limit: Optional[int] = 10

    def __init__(
            self,
            limit: Optional[int] = 10,
            proxy_location: Optional[str] = "US",
            **kwargs
    ):
        """
            param: limit (int): 要返回的最大结果数 [10-100，默认为 10]
            proxy_location: (str): 在哪里获取新闻，特别是针对特定国家/地区的结果。
                 ['US', 'CA', 'IE', 'GB', 'FR', 'DE', 'SE', 'IN', 'JP', 'KR', 'SG', 'AU', 'BR']（默认为美国）
        """
        super().__init__(**kwargs)
        self.limit = limit
        self.proxy_location = proxy_location
        self.headers = {
            "X-API-KEY": os.environ["SERPLY_API_KEY"],
            "User-Agent": "crew-tools",
            "X-Proxy-Location": proxy_location
        }

    def _run(
            self,
            **kwargs: Any,
    ) -> Any:
        # 构建查询参数
        query_payload = {}

        if "query" in kwargs:
            query_payload["q"] = kwargs["query"]
        elif "search_query" in kwargs:
            query_payload["q"] = kwargs["search_query"]

        # 构建 URL
        url = f"{self.search_url}{urlencode(query_payload)}"

        response = requests.request("GET", url, headers=self.headers)
        results = response.json()
        if "entries" in results:
            results = results['entries']
            string = []
            for result in results[:self.limit]:
                try:
                    # 跟踪 URL
                    r = requests.get(result['link'])
                    final_link = r.history[-1].headers['Location']
                    string.append('\n'.join([
                        f"标题：{result['title']}",
                        f"链接：{final_link}",
                        f"来源：{result['source']['title']}",
                        f"发布时间：{result['published']}",
                        "---"
                    ]))
                except KeyError:
                    continue

            content = '\n'.join(string)
            return f"\n搜索结果：{content}\n"
        else:
            return results
