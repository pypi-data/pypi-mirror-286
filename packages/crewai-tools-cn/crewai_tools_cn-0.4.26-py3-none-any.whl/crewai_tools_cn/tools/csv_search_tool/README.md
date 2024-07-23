# CSVSearchTool

## 描述

此工具用于在 CSV 文件内容中执行 RAG（检索增强生成）搜索。它允许用户在指定的 CSV 文件内容中进行语义搜索查询。此功能对于从大型 CSV 数据集中提取信息特别有用，在这些数据集中，传统的搜索方法可能效率低下。所有名称中带有“搜索”的工具，包括 CSVSearchTool，都是为搜索不同数据源而设计的 RAG 工具。

## 安装

安装 crewai_tools 包

```shell
pip install 'crewai[tools]'
```

## 示例

```python
from crewai_tools import CSVSearchTool

# 使用特定的 CSV 文件初始化工具。此设置允许代理仅搜索给定的 CSV 文件。
tool = CSVSearchTool(csv='path/to/your/csvfile.csv')

# 或者

# 在没有特定 CSV 文件的情况下初始化工具。代理需要在运行时提供 CSV 路径。
tool = CSVSearchTool()
```

## 参数

- `csv`：要搜索的 CSV 文件的路径。如果工具在初始化时没有指定 CSV 文件，则此参数是必需的；否则，它是可选的。

## 自定义模型和嵌入

默认情况下，该工具使用 OpenAI 进行嵌入和摘要。要自定义模型，可以使用如下配置字典：

```python
tool = CSVSearchTool(
    config=dict(
        llm=dict(
            provider="ollama", # 或 google, openai, anthropic, llama2, ...
            config=dict(
                model="llama2",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google",
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)
```
