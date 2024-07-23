from typing import Optional, Any, Type, Dict, List
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.base_tool import BaseTool

class FirecrawlCrawlWebsiteToolSchema(BaseModel):
    url: str = Field(description="网站 URL")
    crawler_options: Optional[Dict[str, Any]] = Field(default=None, description="抓取选项")
    page_options: Optional[Dict[str, Any]] = Field(default=None, description="页面选项")

class FirecrawlCrawlWebsiteTool(BaseTool):
    name: str = "Firecrawl 网站抓取工具"
    description: str = "使用 Firecrawl 抓取网页并返回内容"
    args_schema: Type[BaseModel] = FirecrawlCrawlWebsiteToolSchema
    api_key: Optional[str] = None
    firecrawl: Optional[Any] = None

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        try:
            from firecrawl import FirecrawlApp # type: ignore
        except ImportError:
           raise ImportError(
               "找不到 `firecrawl` 包，请运行 `pip install firecrawl-py`"
           )

        self.firecrawl = FirecrawlApp(api_key=api_key)

    def _run(self, url: str, crawler_options: Optional[Dict[str, Any]] = None, page_options: Optional[Dict[str, Any]] = None):
        options = {
            "crawlerOptions": crawler_options,
            "pageOptions": page_options
        }
        return self.firecrawl.crawl_url(url, options)
