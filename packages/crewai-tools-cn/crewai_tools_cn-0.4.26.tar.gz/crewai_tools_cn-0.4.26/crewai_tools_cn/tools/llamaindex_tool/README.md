# LlamaIndexTool 文档

## 描述

此工具旨在成为 LlamaIndex 工具和查询引擎的通用包装器，使您能够利用 LlamaIndex 资源（就 RAG/代理管道而言）作为工具插入到 CrewAI 代理中。

## 安装

要将此工具集成到您的项目中，请按照以下安装说明进行操作：
```shell
pip install 'crewai[tools]'
```

## 示例

以下示例演示了如何初始化工具并使用给定查询执行搜索：

```python
from crewai_tools import LlamaIndexTool

# 从 LlamaIndex 工具初始化工具

## 示例 1：从 FunctionTool 初始化
from llama_index.core.tools import FunctionTool

your_python_function = lambda ...: ...
og_tool = FunctionTool.from_defaults(your_python_function, name="<name>", description='<description>')
tool = LlamaIndexTool.from_tool(og_tool)

## 示例 2：从 LlamaHub 工具初始化
from llama_index.tools.wolfram_alpha import WolframAlphaToolSpec
wolfram_spec = WolframAlphaToolSpec(app_id="<app_id>")
wolfram_tools = wolfram_spec.to_tool_list()
tools = [LlamaIndexTool.from_tool(t) for t in wolfram_tools]


# 从 LlamaIndex 查询引擎初始化工具

## 注意：LlamaIndex 有很多查询引擎，定义您想要的任何查询引擎
query_engine = index.as_query_engine() 
query_tool = LlamaIndexTool.from_query_engine(
    query_engine,
    name="Uber 2019 10K 查询工具",
    description="使用此工具查找 2019 年 Uber 10K 年度报告"
)

```

## 使用步骤

要有效使用 `LlamaIndexTool`，请按照以下步骤操作：

1. **安装 CrewAI**: 确认您的 Python 环境中已安装 `crewai[tools]` 包。
2. **安装和使用 LlamaIndex**: 按照 LlamaIndex 文档 (https://docs.llamaindex.ai/) 设置 RAG/代理管道。
