from typing import Optional, Type, Any
import time
from pydantic.v1 import BaseModel, Field

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from ..base_tool import BaseTool

class FixedSeleniumScrapingToolSchema(BaseModel):
    """SeleniumScrapingTool 的输入。"""
    pass

class SeleniumScrapingToolSchema(FixedSeleniumScrapingToolSchema):
    """SeleniumScrapingTool 的输入。"""
    website_url: str = Field(..., description="要读取文件的网站 URL（必填）")
    css_element: str = Field(..., description="要从网站抓取的元素的 CSS 参考（必填）")

class SeleniumScrapingTool(BaseTool):
    name: str = "读取网站内容"
    description: str = "一个可以用来读取网站内容的工具。"
    args_schema: Type[BaseModel] = SeleniumScrapingToolSchema
    website_url: Optional[str] = None
    driver: Optional[Any] = webdriver.Chrome
    cookie: Optional[dict] = None
    wait_time: Optional[int] = 3
    css_element: Optional[str] = None

    def __init__(self, website_url: Optional[str] = None, cookie: Optional[dict] = None, css_element: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if cookie is not None:
                self.cookie = cookie

        if css_element is not None:
            self.css_element = css_element

        if website_url is not None:
            self.website_url = website_url
            self.description = f"一个可以用来读取 {website_url} 内容的工具。"
            self.args_schema = FixedSeleniumScrapingToolSchema

        self._generate_description()
    def _run(
        self,
        **kwargs: Any,
    ) -> Any:
        website_url = kwargs.get('website_url', self.website_url)
        css_element = kwargs.get('css_element', self.css_element)
        driver = self._create_driver(website_url, self.cookie, self.wait_time)

        content = []
        if css_element is None or css_element.strip() == "":
            body_text = driver.find_element(By.TAG_NAME, "body").text
            content.append(body_text)
        else:
            for element in driver.find_elements(By.CSS_SELECTOR, css_element):
                content.append(element.text)
        driver.close()
        return "\n".join(content)

    def _create_driver(self, url, cookie, wait_time):
            options = Options()
            options.add_argument("--headless")
            driver = self.driver(options=options)
            driver.get(url)
            time.sleep(wait_time)
            if cookie:
                driver.add_cookie(cookie)
                time.sleep(wait_time)
                driver.get(url)
                time.sleep(wait_time)
            return driver

    def close(self):
        self.driver.close()
