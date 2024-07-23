# GithubSearchTool

## 描述

GithubSearchTool 是一款专为在 GitHub 仓库中进行语义搜索而设计的读取、追加和生成 (RAG) 工具。它利用先进的语义搜索功能，筛选代码、拉取请求、问题和仓库，使其成为开发人员、研究人员或任何需要从 GitHub 获取精确信息的人员的必备工具。

## 安装

要使用 GithubSearchTool，首先确保您的 Python 环境中已安装 crewai_tools 包：

```shell
pip install 'crewai[tools]'
```

此命令将安装运行 GithubSearchTool 以及 crewai_tools 包中包含的任何其他工具所需的包。

## 示例

以下是如何使用 GithubSearchTool 在 GitHub 仓库中执行语义搜索：
```python
from crewai_tools import GithubSearchTool

# 初始化工具以在特定的 GitHub 仓库中进行语义搜索
tool = GithubSearchTool(
    gh_token='...',
	github_repo='https://github.com/example/repo',
	content_types=['code', 'issue'] # 选项：code, repo, pr, issue
)

# 或者

# 初始化工具以在特定的 GitHub 仓库中进行语义搜索，以便代理可以在执行过程中了解到任何仓库时进行搜索
tool = GithubSearchTool(
    gh_token='...',
	content_types=['code', 'issue'] # 选项：code, repo, pr, issue
)
```

## 参数

- `gh_token`：用于对搜索进行身份验证的 GitHub 令牌。这是一个必填字段，允许工具访问 GitHub API 进行搜索。
- `github_repo`：将进行搜索的 GitHub 仓库的 URL。这是一个必填字段，用于指定搜索的目标仓库。
- `content_types`：指定要在搜索中包含的内容类型。您必须从以下选项中提供一个内容类型列表：`code` 用于在代码中搜索，`repo` 用于在仓库的一般信息中搜索，`pr` 用于在拉取请求中搜索，以及 `issue` 用于在问题中搜索。此字段是必填字段，允许将搜索范围缩小到 GitHub 仓库中的特定内容类型。

## 自定义模型和嵌入

默认情况下，该工具使用 OpenAI 进行嵌入和摘要。要自定义模型，可以使用如下配置字典：

```python
tool = GithubSearchTool(
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
