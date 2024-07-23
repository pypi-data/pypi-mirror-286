# CodeInterpreterTool

## 描述

此工具用于使代理能够运行由代理本身生成的代码 (Python3)。代码在沙盒环境中执行，因此可以安全地运行任何代码。

它非常有用，因为它允许代理生成代码，在相同的环境中运行它，获取结果并使用它来做出决策。

## 要求

- Docker

## 安装

安装 crewai_tools 包
```shell
pip install 'crewai[tools]'
```

## 示例

请记住，使用此工具时，代码必须由代理本身生成。代码必须是 Python3 代码。第一次运行需要一些时间，因为它需要构建 Docker 镜像。

```python
from crewai_tools import CodeInterpreterTool

Agent(
    ...
    tools=[CodeInterpreterTool()],
)
```
