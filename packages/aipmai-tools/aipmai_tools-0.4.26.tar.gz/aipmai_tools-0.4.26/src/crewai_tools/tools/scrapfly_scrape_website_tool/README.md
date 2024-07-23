## ScrapflyScrapeWebsiteTool

## 描述

[ScrapFly](https://scrapfly.io/) 是一个网页抓取 API，具有无头浏览器功能、代理和反机器人绕过功能。它允许将网页数据提取为可访问的 LLM Markdown 或文本。

## 设置和安装

1. **安装 ScrapFly Python SDK**：安装 `scrapfly-sdk` Python 软件包以使用 ScrapFly Web Loader。使用以下命令通过 pip 安装：

   ```bash
   pip install scrapfly-sdk
   ```

2. **API 密钥**：从 [scrapfly.io/register](https://www.scrapfly.io/register/) 免费注册以获取您的 API 密钥。

## 示例用法

使用 ScrapflyScrapeWebsiteTool 如下所示检索网页数据为文本、Markdown（LLM 可访问）或 HTML：

```python
from crewai_tools import ScrapflyScrapeWebsiteTool

tool = ScrapflyScrapeWebsiteTool(
    api_key="您的 ScrapFly API 密钥"
)

result = tool._run(
    url="https://web-scraping.dev/products",
    scrape_format="markdown",
    ignore_scrape_failures=True
)
```

## 附加参数

ScrapflyScrapeWebsiteTool 还允许传递 ScrapeConfig 对象以自定义抓取请求。有关完整功能详细信息及其 API 参数，请参阅 [API 参数文档](https://scrapfly.io/docs/scrape-api/getting-started)：

```python
from crewai_tools import ScrapflyScrapeWebsiteTool

tool = ScrapflyScrapeWebsiteTool(
    api_key="您的 ScrapFly API 密钥"
)

scrapfly_scrape_config = {
    "asp": True, # 绕过抓取阻止和解决方案，例如 Cloudflare
    "render_js": True, # 使用云无头浏览器启用 JavaScript 渲染
    "proxy_pool": "public_residential_pool", # 选择代理池（数据中心或住宅）
    "country": "us", # 选择代理位置
    "auto_scroll": True, # 自动滚动页面
    "js": "" # 由无头浏览器执行自定义 JavaScript 代码
}

result = tool._run(
    url="https://web-scraping.dev/products",
    scrape_format="markdown",
    ignore_scrape_failures=True,
    scrape_config=scrapfly_scrape_config
)
```
