# FirecrawlSearchTool

## 描述

[Firecrawl](https://firecrawl.dev) 是一个用于抓取任何网站并将其转换为干净的 Markdown 或结构化数据的平台。

## 安装

- 从 [firecrawl.dev](https://firecrawl.dev) 获取 API 密钥，并将其设置在环境变量中 (`FIRECRAWL_API_KEY`)。
- 安装 [Firecrawl SDK](https://github.com/mendableai/firecrawl) 以及 `crewai[tools]` 包：

```
pip install firecrawl-py 'crewai[tools]'
```

## 示例

如下使用 FirecrawlSearchTool 以允许您的代理加载网站：

```python
from crewai_tools import FirecrawlSearchTool

tool = FirecrawlSearchTool(query='firecrawl 是什么？')
```

## 参数

- `api_key`：可选。指定 Firecrawl API 密钥。默认为 `FIRECRAWL_API_KEY` 环境变量。
- `query`：用于搜索的搜索查询字符串。
- `page_options`：可选。结果格式化选项。
  - `onlyMainContent`：可选。仅返回页面的主要内容，不包括页眉、导航、页脚等。
  - `includeHtml`：可选。包含页面的原始 HTML 内容。将在响应中输出一个 html 键。
  - `fetchPageContent`：可选。获取页面的完整内容。
- `search_options`：可选。用于控制抓取行为的选项。
  - `limit`：可选。要抓取的最大页面数。
