from typing import Any, Optional, Type

from embedchain.models.data_type import DataType
from pydantic.v1 import BaseModel, Field

from ..rag.rag_tool import RagTool


class FixedTXTSearchToolSchema(BaseModel):
    """TXTSearchTool 的输入"""

    search_query: str = Field(
        ...,
        description="用于搜索文本内容的必需搜索查询",
    )


class TXTSearchToolSchema(FixedTXTSearchToolSchema):
    """TXTSearchTool 的输入"""

    txt: str = Field(..., description="要搜索的文本文件的必需路径")


class TXTSearchTool(RagTool):
    name: str = "搜索文本内容"
    description: str = (
        "一个可以用来从文本内容中进行语义搜索的工具。"
    )
    args_schema: Type[BaseModel] = TXTSearchToolSchema

    def __init__(self, txt: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if txt is not None:
            self.add(txt)
            self.description = f"一个可以用来在 {txt} 文本内容中进行语义搜索的工具。"
            self.args_schema = FixedTXTSearchToolSchema
            self._generate_description()

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        kwargs["data_type"] = DataType.TEXT_FILE
        super().add(*args, **kwargs)

    def _before_run(
        self,
        query: str,
        **kwargs: Any,
    ) -> Any:
        if "txt" in kwargs:
            self.add(kwargs["txt"])

    def _run(
        self,
        search_query: str,
        **kwargs: Any,
    ) -> Any:
        return super()._run(query=search_query, **kwargs)
