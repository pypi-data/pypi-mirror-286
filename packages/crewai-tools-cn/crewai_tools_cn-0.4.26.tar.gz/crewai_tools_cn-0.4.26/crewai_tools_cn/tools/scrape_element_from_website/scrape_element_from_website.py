import os
import requests
from bs4 import BeautifulSoup
from typing import Optional, Type, Any
from pydantic.v1 import BaseModel, Field
from ..base_tool import BaseTool


class FixedScrapeElementFromWebsiteToolSchema(BaseModel):
    """ScrapeElementFromWebsiteTool 的输入。"""
    pass


class ScrapeElementFromWebsiteToolSchema(FixedScrapeElementFromWebsiteToolSchema):
    """ScrapeElementFromWebsiteTool 的输入。"""
    website_url: str = Field(..., description="要读取文件的网站 URL（必填）")
    css_element: str = Field(..., description="要从网站抓取的元素的 CSS 参考（必填）")


class ScrapeElementFromWebsiteTool(BaseTool):
    name: str = "读取网站内容"
    description: str = "一个可以用来读取网站内容的工具。"
    args_schema: Type[BaseModel] = ScrapeElementFromWebsiteToolSchema
    website_url: Optional[str] = None
    cookies: Optional[dict] = None
    css_element: Optional[str] = None
    headers: Optional[dict] = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    def __init__(self, website_url: Optional[str] = None, cookies: Optional[dict] = None, css_element: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if website_url is not None:
            self.website_url = website_url
            self.css_element = css_element
            self.description = f"一个可以用来读取 {website_url} 内容的工具。"
            self.args_schema = FixedScrapeElementFromWebsiteToolSchema
            self._generate_description()
            if cookies is not None:
                self.cookies = {cookies["name"]: os.getenv(cookies["value"])}

    def _run(
        self,
        **kwargs: Any,
    ) -> Any:
        website_url = kwargs.get('website_url', self.website_url)
        css_element = kwargs.get('css_element', self.css_element)
        page = requests.get(website_url, headers=self.headers, cookies=self.cookies if self.cookies else {})
        parsed = BeautifulSoup(page.content, "html.parser")
        elements = parsed.select(css_element)
        return "\n".join([element.get_text() for element in elements])
