from typing import Any, Optional, Type

from embedchain.models.data_type import DataType
from pydantic.v1 import BaseModel, Field

from ..rag.rag_tool import RagTool


class FixedWebsiteSearchToolSchema(BaseModel):
    """WebsiteSearchTool 的输入"""

    search_query: str = Field(
        ...,
        description="用于在特定网站上进行搜索的必需搜索查询",
    )


class WebsiteSearchToolSchema(FixedWebsiteSearchToolSchema):
    """WebsiteSearchTool 的输入"""

    website: str = Field(
        ..., description="要在其上进行搜索的必需的有效网站 URL"
    )


class WebsiteSearchTool(RagTool):
    name: str = "在特定网站中搜索"
    description: str = "一个可以用来从特定 URL 内容中进行语义搜索的工具。"
    args_schema: Type[BaseModel] = WebsiteSearchToolSchema

    def __init__(self, website: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if website is not None:
            self.add(website)
            self.description = f"一个可以用来从 {website} 网站内容中进行语义搜索的工具。"
            self.args_schema = FixedWebsiteSearchToolSchema
            self._generate_description()

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        kwargs["data_type"] = DataType.WEB_PAGE
        super().add(*args, **kwargs)

    def _before_run(
        self,
        query: str,
        **kwargs: Any,
    ) -> Any:
        if "website" in kwargs:
            self.add(kwargs["website"])

    def _run(
        self,
        search_query: str,
        **kwargs: Any,
    ) -> Any:
        return super()._run(query=search_query, **kwargs)
