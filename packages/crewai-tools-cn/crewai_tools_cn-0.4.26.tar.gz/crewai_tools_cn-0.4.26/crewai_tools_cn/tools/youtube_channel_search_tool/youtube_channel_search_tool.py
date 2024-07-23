from typing import Any, Optional, Type

from embedchain.models.data_type import DataType
from pydantic.v1 import BaseModel, Field

from ..rag.rag_tool import RagTool


class FixedYoutubeChannelSearchToolSchema(BaseModel):
    """YoutubeChannelSearchTool 的输入"""

    search_query: str = Field(
        ...,
        description="用于搜索 Youtube 频道内容的必需搜索查询",
    )


class YoutubeChannelSearchToolSchema(FixedYoutubeChannelSearchToolSchema):
    """YoutubeChannelSearchTool 的输入"""

    youtube_channel_handle: str = Field(
        ..., description="要搜索的 Youtube 频道句柄的必需路径"
    )


class YoutubeChannelSearchTool(RagTool):
    name: str = "搜索 Youtube 频道内容"
    description: str = "一个可以用来从 Youtube 频道内容中进行语义搜索的工具。"
    args_schema: Type[BaseModel] = YoutubeChannelSearchToolSchema

    def __init__(self, youtube_channel_handle: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if youtube_channel_handle is not None:
            self.add(youtube_channel_handle)
            self.description = f"一个可以用来在 {youtube_channel_handle} Youtube 频道内容中进行语义搜索的工具。"
            self.args_schema = FixedYoutubeChannelSearchToolSchema
            self._generate_description()

    def add(
        self,
        youtube_channel_handle: str,
        **kwargs: Any,
    ) -> None:
        if not youtube_channel_handle.startswith("@"):
            youtube_channel_handle = f"@{youtube_channel_handle}"

        kwargs["data_type"] = DataType.YOUTUBE_CHANNEL
        super().add(youtube_channel_handle, **kwargs)

    def _before_run(
        self,
        query: str,
        **kwargs: Any,
    ) -> Any:
        if "youtube_channel_handle" in kwargs:
            self.add(kwargs["youtube_channel_handle"])

    def _run(
        self,
        search_query: str,
        **kwargs: Any,
    ) -> Any:
        return super()._run(query=search_query, **kwargs)
