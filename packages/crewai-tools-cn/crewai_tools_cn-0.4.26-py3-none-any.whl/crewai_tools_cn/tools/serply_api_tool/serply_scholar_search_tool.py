import os
import requests
from urllib.parse import urlencode
from typing import Type, Any, Optional
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.base_tool import BaseTool


class SerplyScholarSearchToolSchema(BaseModel):
    """Serply 学术搜索的输入。"""
    search_query: str = Field(..., description="要用于获取学术文献的必填搜索查询")


class SerplyScholarSearchTool(BaseTool):
    name: str = "学术搜索"
    description: str = "使用 search_query 执行学术文献搜索的工具。"
    args_schema: Type[BaseModel] = SerplyScholarSearchToolSchema
    search_url: str = "https://api.serply.io/v1/scholar/"
    hl: Optional[str] = "us"
    proxy_location: Optional[str] = "US"
    headers: Optional[dict] = {}

    def __init__(
            self,
            hl: str = "us",
            proxy_location: Optional[str] = "US",
            **kwargs
    ):
        """
            param: hl (str): 用于显示结果的主机语言代码
                （参考 https://developers.google.com/custom-search/docs/xml_results?hl=en#wsInterfaceLanguages）
            proxy_location: (str): 指定搜索的代理位置，特别是针对特定国家/地区的结果。
                 ['US', 'CA', 'IE', 'GB', 'FR', 'DE', 'SE', 'IN', 'JP', 'KR', 'SG', 'AU', 'BR']（默认为美国）
        """
        super().__init__(**kwargs)
        self.hl = hl
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
        query_payload = {
            "hl": self.hl
        }

        if "query" in kwargs:
            query_payload["q"] = kwargs["query"]
        elif "search_query" in kwargs:
            query_payload["q"] = kwargs["search_query"]

        # 构建 URL
        url = f"{self.search_url}{urlencode(query_payload)}"

        response = requests.request("GET", url, headers=self.headers)
        articles = response.json().get("articles", "")

        if not articles:
            return ""

        string = []
        for article in articles:
            try:
                if "doc" in article:
                    link = article['doc']['link']
                else:
                    link = article['link']
                authors = [author['name'] for author in article['author']['authors']]
                string.append('\n'.join([
                    f"标题：{article['title']}",
                    f"链接：{link}",
                    f"描述：{article['description']}",
                    f"引用：{article['cite']}",
                    f"作者：{', '.join(authors)}",
                    "---"
                ]))
            except KeyError:
                continue

        content = '\n'.join(string)
        return f"\n搜索结果：{content}\n"
