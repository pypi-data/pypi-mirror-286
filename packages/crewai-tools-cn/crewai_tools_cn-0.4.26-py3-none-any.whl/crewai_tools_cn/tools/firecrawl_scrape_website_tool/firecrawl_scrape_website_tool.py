from typing import Optional, Any, Type, Dict
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.base_tool import BaseTool

class FirecrawlScrapeWebsiteToolSchema(BaseModel):
    url: str = Field(description="网站 URL")
    page_options: Optional[Dict[str, Any]] = Field(default=None, description="页面抓取选项")
    extractor_options: Optional[Dict[str, Any]] = Field(default=None, description="数据提取选项")
    timeout: Optional[int] = Field(default=None, description="抓取操作超时时间")

class FirecrawlScrapeWebsiteTool(BaseTool):
    name: str = "Firecrawl 网站抓取工具"
    description: str = "使用 Firecrawl 抓取网页并返回内容"
    args_schema: Type[BaseModel] = FirecrawlScrapeWebsiteToolSchema
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

    def _run(self, url: str, page_options: Optional[Dict[str, Any]] = None, extractor_options: Optional[Dict[str, Any]] = None, timeout: Optional[int] = None):
        options = {
            "pageOptions": page_options,
            "extractorOptions": extractor_options,
            "timeout": timeout
        }
        return self.firecrawl.scrape_url(url, options)
