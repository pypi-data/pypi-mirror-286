# DirectoryReadTool

## 描述

DirectoryReadTool 是一款高效的实用工具，旨在全面列出目录内容。它递归地导航到指定的目录，为用户提供所有文件的详细列表，包括嵌套在子目录中的文件。对于需要彻底清点目录结构或验证目录中文件组织的任务来说，此工具必不可少。

## 安装

在您的项目中安装 `crewai_tools` 包以使用 DirectoryReadTool。如果您的环境中尚未添加此包，您可以使用以下命令通过 pip 轻松安装：

```shell
pip install 'crewai[tools]'
```

这将安装最新版本的 `crewai_tools` 包，从而可以访问 DirectoryReadTool 和其他实用程序。

## 示例

DirectoryReadTool 使用起来很简单。以下代码片段显示了如何设置和使用该工具列出指定目录的内容：

```python
from crewai_tools import DirectoryReadTool

# 使用要浏览的目录初始化工具
tool = DirectoryReadTool(directory='/path/to/your/directory')

# 使用该工具列出指定目录的内容
directory_contents = tool.run()
print(directory_contents)
```

此示例演示了有效利用 DirectoryReadTool 的基本步骤，突出了其简单性和用户友好的设计。

## 参数

DirectoryReadTool 使用时只需极少的配置。此工具的基本参数如下：

- `directory`：一个必需的参数，用于指定要列出其内容的目录的路径。它接受绝对路径和相对路径，引导工具到所需的目录进行内容列表。

DirectoryReadTool 提供了一种用户友好且高效的方式来列出目录内容，使其成为管理和检查目录结构的宝贵工具。
```

此修订后的 DirectoryReadTool 文档保留了概述的结构和内容要求，并对清晰度、一致性和对所提供文档示例中体现的高质量标准的遵守进行了一些调整。
