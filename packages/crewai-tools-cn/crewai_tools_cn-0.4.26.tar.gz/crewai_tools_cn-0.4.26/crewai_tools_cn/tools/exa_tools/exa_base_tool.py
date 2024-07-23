import os
from typing import Type
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.base_tool import BaseTool

class EXABaseToolToolSchema(BaseModel):
    """EXABaseTool 的输入"""
    search_query: str = Field(..., description="您想用来搜索互联网的必需搜索查询")

class EXABaseTool(BaseTool):
    name: str = "搜索互联网"
    description: str = "一个可以使用 search_query 搜索互联网的工具"
    args_schema: Type[BaseModel] = EXABaseToolToolSchema
    search_url: str = "https://api.exa.ai/search"
    n_results: int = None
    headers: dict = {
            "accept": "application/json",
            "content-type": "application/json",
        }

    def _parse_results(self, results):
        stirng = []
        for result in results:
            try:
                stirng.append('\n'.join([
                        f"标题：{result['title']}",
                        f"分数：{result['score']}",
                        f"网址：{result['url']}",
                        f"ID：{result['id']}",
                        "---"
                ]))
            except KeyError:
                next

        content = '\n'.join(stirng)
        return f"\n搜索结果：{content}\n"
