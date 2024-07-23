from typing import Any, Optional, Type

from embedchain.models.data_type import DataType
from pydantic.v1 import BaseModel, Field

from ..rag.rag_tool import RagTool


class FixedXMLSearchToolSchema(BaseModel):
    """XMLSearchTool 的输入"""

    search_query: str = Field(
        ...,
        description="用于搜索 XML 内容的必需搜索查询",
    )


class XMLSearchToolSchema(FixedXMLSearchToolSchema):
    """XMLSearchTool 的输入"""

    xml: str = Field(..., description="要搜索的 XML 文件的必需路径")


class XMLSearchTool(RagTool):
    name: str = "搜索 XML 内容"
    description: str = (
        "一个可以用来从 XML 内容中进行语义搜索的工具。"
    )
    args_schema: Type[BaseModel] = XMLSearchToolSchema

    def __init__(self, xml: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if xml is not None:
            self.add(xml)
            self.description = f"一个可以用来在 {xml} XML 内容中进行语义搜索的工具。"
            self.args_schema = FixedXMLSearchToolSchema
            self._generate_description()

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        kwargs["data_type"] = DataType.XML
        super().add(*args, **kwargs)

    def _before_run(
        self,
        query: str,
        **kwargs: Any,
    ) -> Any:
        if "xml" in kwargs:
            self.add(kwargs["xml"])

    def _run(
        self,
        search_query: str,
        **kwargs: Any,
    ) -> Any:
        return super()._run(query=search_query, **kwargs)
