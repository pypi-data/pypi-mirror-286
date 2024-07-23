from typing import Any, Optional, Type

from embedchain.models.data_type import DataType
from pydantic.v1 import BaseModel, Field

from ..rag.rag_tool import RagTool


class FixedCodeDocsSearchToolSchema(BaseModel):
    """CodeDocsSearchTool 的输入"""

    search_query: str = Field(
        ...,
        description="您要用於搜索代码文档内容的必填搜索查询",
    )


class CodeDocsSearchToolSchema(FixedCodeDocsSearchToolSchema):
    """CodeDocsSearchTool 的输入"""

    docs_url: str = Field(..., description="您要搜索的必填 docs_url 路径")


class CodeDocsSearchTool(RagTool):
    name: str = "搜索代码文档内容"
    description: str = (
        "可用于从代码文档内容中进行语义搜索查询的工具。"
    )
    args_schema: Type[BaseModel] = CodeDocsSearchToolSchema

    def __init__(self, docs_url: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if docs_url is not None:
            self.add(docs_url)
            self.description = f"一个可以用来对 {docs_url} 代码文档内容进行语义搜索查询的工具。"
            self.args_schema = FixedCodeDocsSearchToolSchema
            self._generate_description()

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        kwargs["data_type"] = DataType.DOCS_SITE
        super().add(*args, **kwargs)

    def _before_run(
        self,
        query: str,
        **kwargs: Any,
    ) -> Any:
        if "docs_url" in kwargs:
            self.add(kwargs["docs_url"])

    def _run(
        self,
        search_query: str,
        **kwargs: Any,
    ) -> Any:
        return super()._run(query=search_query, **kwargs)