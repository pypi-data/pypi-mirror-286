from typing import Any, Optional, Type

from embedchain.models.data_type import DataType
from pydantic.v1 import BaseModel, Field

from ..rag.rag_tool import RagTool


class FixedMDXSearchToolSchema(BaseModel):
    """MDXSearchTool 的输入"""

    search_query: str = Field(
        ...,
        description="要用于搜索 MDX 内容的必填搜索查询",
    )


class MDXSearchToolSchema(FixedMDXSearchToolSchema):
    """MDXSearchTool 的输入"""

    mdx: str = Field(..., description="要搜索的必填 mdx 路径")


class MDXSearchTool(RagTool):
    name: str = "搜索 MDX 的内容"
    description: str = (
        "可以用来从 MDX 的内容中进行语义搜索的工具。"
    )
    args_schema: Type[BaseModel] = MDXSearchToolSchema

    def __init__(self, mdx: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if mdx is not None:
            self.add(mdx)
            self.description = f"可以用来在 {mdx} MDX 的内容中进行语义搜索的工具。"
            self.args_schema = FixedMDXSearchToolSchema
            self._generate_description()

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        kwargs["data_type"] = DataType.MDX
        super().add(*args, **kwargs)

    def _before_run(
        self,
        query: str,
        **kwargs: Any,
    ) -> Any:
        if "mdx" in kwargs:
            self.add(kwargs["mdx"])

    def _run(
        self,
        search_query: str,
        **kwargs: Any,
    ) -> Any:
        return super()._run(query=search_query, **kwargs)
