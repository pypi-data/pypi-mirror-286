import os
import requests
from typing import Type, Any, Optional
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.rag.rag_tool import RagTool


class SerplyWebpageToMarkdownToolSchema(BaseModel):
    """Serply 网页请求的输入。"""
    url: str = Field(..., description="要用于获取并转换为 Markdown 的必填 URL")

class SerplyWebpageToMarkdownTool(RagTool):
    name: str = "网页转 Markdown"
    description: str = "将网页转换为 Markdown 以便 LLM 更容易理解的工具"
    args_schema: Type[BaseModel] = SerplyWebpageToMarkdownToolSchema
    request_url: str = "https://api.serply.io/v1/request"
    proxy_location: Optional[str] = "US"
    headers: Optional[dict] = {}

    def __init__(
            self,
            proxy_location: Optional[str] = "US",
            **kwargs
    ):
        """
            proxy_location: (str): 指定搜索的代理位置，特别是针对特定国家/地区的结果。
                 ['US', 'CA', 'IE', 'GB', 'FR', 'DE', 'SE', 'IN', 'JP', 'KR', 'SG', 'AU', 'BR']（默认为美国）
        """
        super().__init__(**kwargs)
        self.proxy_location = proxy_location
        self.headers = {
            "X-API-KEY": os.environ["SERPLY_API_KEY"],
            "User-Agent": "crew-tools",
            "X-Proxy-Location": proxy_location
        }

    def _run(
            self,
            **kwargs: Any,
    ) -> Any:
        data = {
            "url": kwargs["url"],
            "method": "GET",
            "response_type": "markdown"
        }
        response = requests.request("POST", self.request_url, headers=self.headers, json=data)
        return response.text
