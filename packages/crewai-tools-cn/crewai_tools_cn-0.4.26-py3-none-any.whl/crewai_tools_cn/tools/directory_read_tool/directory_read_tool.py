import os
from typing import Optional, Type, Any
from pydantic.v1 import BaseModel, Field
from ..base_tool import BaseTool

class FixedDirectoryReadToolSchema(BaseModel):
    """DirectoryReadTool 的输入"""
    pass

class DirectoryReadToolSchema(FixedDirectoryReadToolSchema):
    """DirectoryReadTool 的输入"""
    directory: str = Field(..., description="要列出内容的必需目录")

class DirectoryReadTool(BaseTool):
    name: str = "列出目录中的文件"
    description: str = "一个可以用来递归列出目录内容的工具。"
    args_schema: Type[BaseModel] = DirectoryReadToolSchema
    directory: Optional[str] = None

    def __init__(self, directory: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if directory is not None:
            self.directory = directory
            self.description = f"一个可以用来列出 {directory} 内容的工具。"
            self.args_schema = FixedDirectoryReadToolSchema
            self._generate_description()

    def _run(
        self,
        **kwargs: Any,
    ) -> Any:
        directory = kwargs.get('directory', self.directory)
        if directory[-1] == "/":
            directory = directory[:-1]
        files_list = [f"{directory}/{(os.path.join(root, filename).replace(directory, '').lstrip(os.path.sep))}" for root, dirs, files in os.walk(directory) for filename in files]
        files = "\n- ".join(files_list)
        return f"文件路径：\n-{files}"
