from typing import Optional, Any, Type, Dict, Literal
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.base_tool import BaseTool

class SpiderToolSchema(BaseModel):
    url: str = Field(description="网站 URL")
    params: Optional[Dict[str, Any]] = Field(
        description="设置附加参数。选项包括：\n"
                    "- `limit`: Optional[int] - 每个网站允许爬取的最大页面数。删除该值或将其设置为 `0` 以爬取所有页面。\n"
                    "- `depth`: Optional[int] - 最大深度的爬取限制。如果为 `0`，则不应用限制。\n"
                    "- `metadata`: Optional[bool] - 是否包含元数据的布尔值。默认为 `False`，除非设置为 `True`。如果用户想要元数据，请包含 params.metadata = True。\n"
                    "- `query_selector`: Optional[str] - 从标记中提取内容时使用的 CSS 查询选择器。\n"
    )
    mode: Literal["scrape", "crawl"] = Field(
        default="scrape",
        description="模式，仅允许两种模式：`scrape` 或 `crawl`。使用 `scrape` 抓取单个页面，使用 `crawl` 抓取整个网站（包括子页面）。即使设置了 ANY 参数，这些模式也是唯一允许的值。"
    )

class SpiderTool(BaseTool):
    name: str = "Spider 抓取和爬取工具"
    description: str = "抓取和爬取任何 URL 并返回 LLM 就绪的数据。"
    args_schema: Type[BaseModel] = SpiderToolSchema
    api_key: Optional[str] = None
    spider: Optional[Any] = None

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        try:
            from spider import Spider # type: ignore
        except ImportError:
           raise ImportError(
               "找不到 `spider-client` 包，请运行 `pip install spider-client`"
           )

        self.spider = Spider(api_key=api_key)

    def _run(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        mode: Optional[Literal["scrape", "crawl"]] = "scrape"
    ):
        if mode not in ["scrape", "crawl"]:
            raise ValueError(
                "在 `mode` 参数中使用了未知模式，允许的模式为 `scrape` 或 `crawl`"
            )

        # 确保始终包含 'return_format': 'markdown'
        if params:
            params["return_format"] = "markdown"
        else:
            params = {"return_format": "markdown"}

        action = (
            self.spider.scrape_url if mode == "scrape" else self.spider.crawl_url
        )
        spider_docs = action(url=url, params=params)

        return spider_docs
