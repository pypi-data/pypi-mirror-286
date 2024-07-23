from typing import Optional, Any, Type, Dict, List
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.base_tool import BaseTool

class FirecrawlSearchToolSchema(BaseModel):
    query: str = Field(description="搜索查询")
    page_options: Optional[Dict[str, Any]] = Field(default=None, description="结果格式化选项")
    search_options: Optional[Dict[str, Any]] = Field(default=None, description="搜索选项")

class FirecrawlSearchTool(BaseTool):
    name: str = "Firecrawl 网站搜索工具"
    description: str = "使用 Firecrawl 搜索网页并返回结果"
    args_schema: Type[BaseModel] = FirecrawlSearchToolSchema
    api_key: Optional[str] = None
    firecrawl: Optional[Any] = None

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        try:
            from firecrawl import FirecrawlApp # type: ignore
        except ImportError:
           raise ImportError(
               "找不到 `firecrawl` 包，请运行 `pip install firecrawl-py`"
           )

        self.firecrawl = FirecrawlApp(api_key=api_key)

    def _run(self, query: str, page_options: Optional[Dict[str, Any]] = None, result_options: Optional[Dict[str, Any]] = None):
        options = {
            "pageOptions": page_options,
            "resultOptions": result_options
        }
        return self.firecrawl.search(query, options)
