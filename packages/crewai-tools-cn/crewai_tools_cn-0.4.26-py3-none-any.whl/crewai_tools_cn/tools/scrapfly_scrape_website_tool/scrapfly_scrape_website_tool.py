import logging

from typing import Optional, Any, Type, Dict, Literal
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.base_tool import BaseTool

logger = logging.getLogger(__file__)

class ScrapflyScrapeWebsiteToolSchema(BaseModel):
    url: str = Field(description="网页 URL")
    scrape_format: Optional[Literal["raw", "markdown", "text"]] = Field(default="markdown", description="网页提取格式")
    scrape_config: Optional[Dict[str, Any]] = Field(default=None, description="Scrapfly 请求抓取配置")
    ignore_scrape_failures: Optional[bool] = Field(default=None, description="是否忽略失败")

class ScrapflyScrapeWebsiteTool(BaseTool):
    name: str = "Scrapfly 网页抓取 API 工具"
    description: str = "使用 Scrapfly 抓取网页 URL 并将其内容作为 Markdown 或文本返回"
    args_schema: Type[BaseModel] = ScrapflyScrapeWebsiteToolSchema
    api_key: str = None
    scrapfly: Optional[Any] = None

    def __init__(self, api_key: str):
        super().__init__()
        try:
            from scrapfly import ScrapflyClient
        except ImportError:
            raise ImportError(
                "找不到 `scrapfly` 包，请运行 `pip install scrapfly-sdk`"
            )
        self.scrapfly = ScrapflyClient(key=api_key)

    def _run(self, url: str, scrape_format: str = "markdown", scrape_config: Optional[Dict[str, Any]] = None, ignore_scrape_failures: Optional[bool] = None):
        from scrapfly import ScrapeApiResponse, ScrapeConfig

        scrape_config = scrape_config if scrape_config is not None else {}
        try:
            response: ScrapeApiResponse = self.scrapfly.scrape(
                ScrapeConfig(url, format=scrape_format, **scrape_config)
            )
            return response.scrape_result["content"]
        except Exception as e:
            if ignore_scrape_failures:
                logger.error(f"从 {url} 获取数据时出错，异常：{e}")
                return None
            else:
                raise e
