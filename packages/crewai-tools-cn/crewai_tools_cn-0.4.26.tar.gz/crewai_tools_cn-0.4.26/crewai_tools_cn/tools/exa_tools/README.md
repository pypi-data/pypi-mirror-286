# EXASearchTool 文档

## 描述

此工具旨在对整个互联网上的文本内容执行指定查询的语义搜索。它利用 `https://exa.ai/` API 根据用户提供的查询获取并显示最相关的搜索结果。

## 安装

要将此工具集成到您的项目中，请按照以下安装说明进行操作：
```shell
pip install 'crewai[tools]'
```

## 示例

以下示例演示了如何初始化工具并使用给定查询执行搜索：

```python
from crewai_tools import EXASearchTool

# 初始化工具以实现互联网搜索功能
tool = EXASearchTool()
```

## 使用步骤

要有效使用 `EXASearchTool`，请按照以下步骤操作：

1. **安装软件包**: 确认您的 Python 环境中已安装 `crewai[tools]` 包。
2. **获取 API 密钥**: 通过在 `https://exa.ai/` 注册免费帐户来获取 `https://exa.ai/` API 密钥。
3. **配置环境**: 将您获得的 API 密钥存储在名为 `EXA_API_KEY` 的环境变量中，以便工具使用。

## 结论

通过将 `EXASearchTool` 集成到 Python 项目中，用户可以直接从其应用程序进行实时、相关的互联网搜索。通过遵循提供的设置和使用指南，可以简化并将此工具轻松集成到项目中。
