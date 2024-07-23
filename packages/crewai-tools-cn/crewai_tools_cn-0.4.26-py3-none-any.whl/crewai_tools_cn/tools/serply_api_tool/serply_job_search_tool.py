import os
import requests
from urllib.parse import urlencode
from typing import Type, Any, Optional
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.rag.rag_tool import RagTool


class SerplyJobSearchToolSchema(BaseModel):
    """Serply 招聘搜索的输入。"""
    search_query: str = Field(..., description="要用于获取招聘信息的必填搜索查询。")

class SerplyJobSearchTool(RagTool):
    name: str = "招聘搜索"
    description: str = "一个使用 search_query 在美国执行招聘搜索的工具。"
    args_schema: Type[BaseModel] = SerplyJobSearchToolSchema
    request_url: str = "https://api.serply.io/v1/job/search/"
    proxy_location: Optional[str] = "US"
    """
        proxy_location: (str): 在哪里获取招聘信息，特别是针对特定国家/地区的结果。
            - 当前仅支持美国
    """
    headers: Optional[dict] = {}

    def __init__(
            self,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.headers = {
            "X-API-KEY": os.environ["SERPLY_API_KEY"],
            "User-Agent": "crew-tools",
            "X-Proxy-Location": self.proxy_location
        }

    def _run(
            self,
            **kwargs: Any,
    ) -> Any:
        query_payload = {}

        if "query" in kwargs:
            query_payload["q"] = kwargs["query"]
        elif "search_query" in kwargs:
            query_payload["q"] = kwargs["search_query"]

        # 构建 URL
        url = f"{self.request_url}{urlencode(query_payload)}"

        response = requests.request("GET", url, headers=self.headers)

        jobs = response.json().get("jobs", "")

        if not jobs:
            return ""

        string = []
        for job in jobs:
            try:
                string.append('\n'.join([
                    f"职位：{job['position']}",
                    f"雇主：{job['employer']}",
                    f"地点：{job['location']}",
                    f"链接：{job['link']}",
                    f"""最精彩的部分：{', '.join([h for h in job['highlights']])}""",
                    f"是否远程：{job['is_remote']}",
                    f"是否混合：{job['is_remote']}",
                    "---"
                ]))
            except KeyError:
                continue

        content = '\n'.join(string)
        return f"\n搜索结果：{content}\n"
