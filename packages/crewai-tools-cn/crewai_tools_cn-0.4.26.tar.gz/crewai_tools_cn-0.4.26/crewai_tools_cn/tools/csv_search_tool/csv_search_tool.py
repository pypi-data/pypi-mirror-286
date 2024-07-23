from typing import Any, Optional, Type

from embedchain.models.data_type import DataType
from pydantic.v1 import BaseModel, Field

from ..rag.rag_tool import RagTool


class FixedCSVSearchToolSchema(BaseModel):
    """CSVSearchTool 的输入"""

    search_query: str = Field(
        ...,
        description="您想用于搜索 CSV 内容的必需搜索查询",
    )


class CSVSearchToolSchema(FixedCSVSearchToolSchema):
    """CSVSearchTool 的输入"""

    csv: str = Field(..., description="您想搜索的必需 CSV 路径")


class CSVSearchTool(RagTool):
    name: str = "搜索 CSV 内容"
    description: str = (
        "一个可以用来从 CSV 内容中语义搜索查询的工具。"
    )
    args_schema: Type[BaseModel] = CSVSearchToolSchema

    def __init__(self, csv: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if csv is not None:
            self.add(csv)
            self.description = f"一个可以用来语义搜索 {csv} CSV 内容的查询工具。"
            self.args_schema = FixedCSVSearchToolSchema
            self._generate_description()

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        kwargs["data_type"] = DataType.CSV
        super().add(*args, **kwargs)

    def _before_run(
        self,
        query: str,
        **kwargs: Any,
    ) -> Any:
        if "csv" in kwargs:
            self.add(kwargs["csv"])

    def _run(
        self,
        search_query: str,
        **kwargs: Any,
    ) -> Any:
        return super()._run(query=search_query, **kwargs)
    