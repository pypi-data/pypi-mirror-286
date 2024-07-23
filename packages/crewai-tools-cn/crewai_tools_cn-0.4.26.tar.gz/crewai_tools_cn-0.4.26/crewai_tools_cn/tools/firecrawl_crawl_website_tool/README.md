# FirecrawlCrawlWebsiteTool

## 描述

[Firecrawl](https://firecrawl.dev) 是一个用于抓取任何网站并将其转换为干净的 Markdown 或结构化数据的平台。

## 安装

- 从 [firecrawl.dev](https://firecrawl.dev) 获取 API 密钥，并将其设置在环境变量中（`FIRECRAWL_API_KEY`）。
- 安装 [Firecrawl SDK](https://github.com/mendableai/firecrawl) 以及 `crewai[tools]` 包：

```
pip install firecrawl-py 'crewai[tools]'
```

## 示例

如下使用 FirecrawlScrapeFromWebsiteTool 以允许您的代理加载网站：

```python
from crewai_tools import FirecrawlCrawlWebsiteTool

tool = FirecrawlCrawlWebsiteTool(url='firecrawl.dev')
```

## 参数

- `api_key`：可选。指定 Firecrawl API 密钥。默认为 `FIRECRAWL_API_KEY` 环境变量。
- `url`：要开始抓取的基准 URL。
- `page_options`：可选。
  - `onlyMainContent`：可选。仅返回页面的主要内容，不包括页眉、导航、页脚等。
  - `includeHtml`：可选。包含页面的原始 HTML 内容。将在响应中输出一个 html 键。
- `crawler_options`：可选。用于控制抓取行为的选项。
  - `includes`：可选。要包含在抓取中的 URL 模式。
  - `exclude`：可选。要从抓取中排除的 URL 模式。
  - `generateImgAltText`：可选。使用 LLM 生成图像的替代文本（需要付费计划）。
  - `returnOnlyUrls`：可选。如果为 true，则仅返回抓取状态中的 URL 列表。注意：响应将是数据内部的 URL 列表，而不是文档列表。
  - `maxDepth`：可选。要抓取的最大深度。深度 1 是基准 URL，深度 2 包括基准 URL 及其直接子级，依此类推。
  - `mode`：可选。要使用的抓取模式。快速模式在没有站点地图的网站上抓取速度快 4 倍，但可能不如准确，不应在大量使用 JavaScript 渲染的网站上使用。
  - `limit`：可选。要抓取的最大页面数。
  - `timeout`：可选。抓取操作的超时时间（以毫秒为单位）。
