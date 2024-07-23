from typing import Any, Optional, Type

from embedchain.models.data_type import DataType
from pydantic.v1 import BaseModel, Field

from ..rag.rag_tool import RagTool


class FixedDOCXSearchToolSchema(BaseModel):
    """DOCXSearchTool 的输入"""
    docx: Optional[str] = Field(..., description="您要搜索的 docx 文件的必填路径")
    search_query: str = Field(
        ...,
        description="您要用于搜索 DOCX 内容的必需搜索查询",
    )

class DOCXSearchToolSchema(FixedDOCXSearchToolSchema):
    """DOCXSearchTool 的输入"""
    search_query: str = Field(
        ...,
        description="您要用于搜索 DOCX 内容的必需搜索查询",
    )

class DOCXSearchTool(RagTool):
    name: str = "搜索 DOCX 内容"
    description: str = (
        "一个可以用来从 DOCX 内容中语义搜索查询的工具。"
    )
    args_schema: Type[BaseModel] = DOCXSearchToolSchema

    def __init__(self, docx: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if docx is not None:
            self.add(docx)
            self.description = f"一个可以用来语义搜索 {docx} DOCX 内容的查询工具。"
            self.args_schema = FixedDOCXSearchToolSchema
            self._generate_description()

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        kwargs["data_type"] = DataType.DOCX
        super().add(*args, **kwargs)

    def _before_run(
        self,
        query: str,
        **kwargs: Any,
    ) -> Any:
        if "docx" in kwargs:
            self.add(kwargs["docx"])

    def _run(
        self,
        **kwargs: Any,
    ) -> Any:
        search_query = kwargs.get('search_query')
        if search_query is None:
            search_query = kwargs.get('query')

        docx = kwargs.get("docx")
        if docx is not None:
            self.add(docx)
        return super()._run(query=search_query, **kwargs)
