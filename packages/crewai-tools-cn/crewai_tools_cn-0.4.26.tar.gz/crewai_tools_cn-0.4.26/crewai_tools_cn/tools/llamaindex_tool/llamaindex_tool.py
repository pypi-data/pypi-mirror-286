import os
import json
import requests

from typing import Type, Any, cast, Optional
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.base_tool import BaseTool

class LlamaIndexTool(BaseTool):
    """用于包装 LlamaIndex 工具/查询引擎的工具。"""
    llama_index_tool: Any

    def _run(
		self,
        *args: Any,
		**kwargs: Any,
	) -> Any:
        """运行工具。"""
        from llama_index.core.tools import BaseTool as LlamaBaseTool
        tool = cast(LlamaBaseTool, self.llama_index_tool)
        return tool(*args, **kwargs)
	
    @classmethod
    def from_tool(
        cls,
        tool: Any,
        **kwargs: Any
    ) -> "LlamaIndexTool":
        from llama_index.core.tools import BaseTool as LlamaBaseTool
        
        if not isinstance(tool, LlamaBaseTool):
            raise ValueError(f"预期为 LlamaBaseTool，但得到了 {type(tool)}")
        tool = cast(LlamaBaseTool, tool)

        if tool.metadata.fn_schema is None:
            raise ValueError("LlamaIndex 工具没有指定 fn_schema。")
        args_schema = cast(Type[BaseModel], tool.metadata.fn_schema)
        
        return cls(
            name=tool.metadata.name,
            description=tool.metadata.description,
            args_schema=args_schema,
            llama_index_tool=tool,
            **kwargs
        )


    @classmethod
    def from_query_engine(
        cls,
        query_engine: Any,
        name: Optional[str] = None,
        description: Optional[str] = None,
        return_direct: bool = False,
        **kwargs: Any
    ) -> "LlamaIndexTool":
        from llama_index.core.query_engine import BaseQueryEngine
        from llama_index.core.tools import QueryEngineTool

        if not isinstance(query_engine, BaseQueryEngine):
            raise ValueError(f"预期为 BaseQueryEngine，但得到了 {type(query_engine)}")

        # 注意：默认情况下，模式需要一个 `input` 变量。但这会让 crewAI 感到困惑，所以我们将其重命名为 `query`。
        class QueryToolSchema(BaseModel):
            """查询工具的模式。"""
            query: str = Field(..., description="查询工具的搜索查询。")

        # 注意：将 `resolve_input_errors` 设置为 True 很重要，因为模式需要 `input`，但我们使用的是 `query`
        query_engine_tool = QueryEngineTool.from_defaults(
            query_engine,
            name=name,
            description=description,
            return_direct=return_direct,
            resolve_input_errors=True,  
        )
        # HACK：我们将模式替换为我们的自定义模式
        query_engine_tool.metadata.fn_schema = QueryToolSchema
        
        return cls.from_tool(
            query_engine_tool,
            **kwargs
        )
