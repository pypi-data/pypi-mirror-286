# RagTool：动态知识库工具

RagTool 旨在通过利用 RAG 的强大功能（利用 EmbedChain）来回答问题。它与 CrewAI 生态系统无缝集成，为信息检索提供了一种通用且强大的解决方案。

## **概述**

RagTool 使用户能够动态查询知识库，使其成为需要访问大量信息的应用程序的理想工具。其灵活的设计允许与各种数据源集成，包括文件、目录、网页、YouTube 视频和自定义配置。

## **用法**

可以使用来自不同来源的数据实例化 RagTool，包括：

- 📰 PDF 文件
- 📊 CSV 文件
- 📃 JSON 文件
- 📝 文本文件
- 📁 目录/文件夹
- 🌐 HTML 网页
- 📽️ YouTube 频道
- 📺 YouTube 视频
- 📚 文档网站
- 📝 MDX 文件
- 📄 DOCX 文件
- 🧾 XML 文件
- 📬 Gmail
- 📝 Github
- 🐘 Postgres
- 🐬 MySQL
- 🤖 Slack
- 💬 Discord
- 🗨️ Discourse
- 📝 Substack
- 🐝 Beehiiv
- 💾 Dropbox
- 🖼️ 图像
- ⚙️ 自定义

#### **创建实例**

```python
from crewai_tools.tools.rag_tool import RagTool

# 示例：从文件加载
rag_tool = RagTool().from_file('path/to/your/file.txt')

# 示例：从目录加载
rag_tool = RagTool().from_directory('path/to/your/directory')

# 示例：从网页加载
rag_tool = RagTool().from_web_page('https://example.com')
```

## **贡献**

欢迎为 RagTool 和更广泛的 CrewAI 工具生态系统做出贡献。要做出贡献，请遵循标准的 GitHub 工作流程，即 fork 存储库、进行更改并提交拉取请求。

## **许可证**

RagTool 是开源的，可在 MIT 许可证下使用。

感谢您考虑将 RagTool 用于您的知识库需求。您的贡献和反馈对于使 RagTool 变得更好至关重要。
