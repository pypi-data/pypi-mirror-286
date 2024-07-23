import os
import requests
from urllib.parse import urlencode
from typing import Type, Any, Optional
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.base_tool import BaseTool


class SerplyWebSearchToolSchema(BaseModel):
    """Serply 网络搜索的输入。"""
    search_query: str = Field(..., description="要用于 Google 搜索的必填搜索查询")


class SerplyWebSearchTool(BaseTool):
    name: str = "Google 搜索"
    description: str = "使用 search_query 执行 Google 搜索的工具。"
    args_schema: Type[BaseModel] = SerplyWebSearchToolSchema
    search_url: str = "https://api.serply.io/v1/search/"
    hl: Optional[str] = "us"
    limit: Optional[int] = 10
    device_type: Optional[str] = "desktop"
    proxy_location: Optional[str] = "US"
    query_payload: Optional[dict] = {}
    headers: Optional[dict] = {}

    def __init__(
            self,
            hl: str = "us",
            limit: int = 10,
            device_type: str = "desktop",
            proxy_location: str = "US",
            **kwargs
    ):
        """
            param: query (str): 要搜索的查询
            param: hl (str): 用于显示结果的主机语言代码
                （参考 https://developers.google.com/custom-search/docs/xml_results?hl=en#wsInterfaceLanguages）
            param: limit (int): 要返回的最大结果数 [10-100，默认为 10]
            param: device_type (str): 桌面/移动设备结果（默认为桌面）
            proxy_location: (str): 在哪里执行搜索，特别是针对本地/区域结果。
                 ['US', 'CA', 'IE', 'GB', 'FR', 'DE', 'SE', 'IN', 'JP', 'KR', 'SG', 'AU', 'BR']（默认为美国）
        """
        super().__init__(**kwargs)

        self.limit = limit
        self.device_type = device_type
        self.proxy_location = proxy_location

        # 构建查询参数
        self.query_payload = {
            "num": limit,
            "gl": proxy_location.upper(),
            "hl": hl.lower()
        }
        self.headers = {
            "X-API-KEY": os.environ["SERPLY_API_KEY"],
            "X-User-Agent": device_type,
            "User-Agent": "crew-tools",
            "X-Proxy-Location": proxy_location
        }

    def _run(
            self,
            **kwargs: Any,
    ) -> Any:
        if "query" in kwargs:
            self.query_payload["q"] = kwargs["query"]
        elif "search_query" in kwargs:
            self.query_payload["q"] = kwargs["search_query"]

        # 构建 URL
        url = f"{self.search_url}{urlencode(self.query_payload)}"

        response = requests.request("GET", url, headers=self.headers)
        results = response.json()
        if "results" in results:
            results = results['results']
            string = []
            for result in results:
                try:
                    string.append('\n'.join([
                        f"标题：{result['title']}",
                        f"链接：{result['link']}",
                        f"描述：{result['description'].strip()}",
                        "---"
                    ]))
                except KeyError:
                    continue

            content = '\n'.join(string)
            return f"\n搜索结果：{content}\n"
        else:
            return results
