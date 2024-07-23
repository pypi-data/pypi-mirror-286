from typing import Optional, Type, Any
from pydantic.v1 import BaseModel, Field
from ..base_tool import BaseTool


class FixedFileReadToolSchema(BaseModel):
    """FileReadTool 的输入"""
    pass


class FileReadToolSchema(FixedFileReadToolSchema):
    """FileReadTool 的输入"""
    file_path: str = Field(
        ...,
        description="要读取的文件的完整路径（必填）"
    )


class FileReadTool(BaseTool):
    name: str = "读取文件内容"
    description: str = "一个可以用来读取文件内容的工具。"
    args_schema: Type[BaseModel] = FileReadToolSchema
    file_path: Optional[str] = None

    def __init__(
        self,
        file_path: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        if file_path is not None:
            self.file_path = file_path
            self.description = f"一个可以用来读取 {file_path} 内容的工具。"
            self.args_schema = FixedFileReadToolSchema
            self._generate_description()

    def _run(
        self,
        **kwargs: Any,
    ) -> Any:
        try:
            file_path = kwargs.get('file_path', self.file_path)
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            return f"读取文件 {file_path} 失败。错误：{e}"
