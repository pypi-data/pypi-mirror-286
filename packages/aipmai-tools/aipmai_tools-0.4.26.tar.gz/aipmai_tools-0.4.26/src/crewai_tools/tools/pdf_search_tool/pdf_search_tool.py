from typing import Any, Optional, Type

from embedchain.models.data_type import DataType
from pydantic import model_validator
from pydantic.v1 import BaseModel, Field

from ..rag.rag_tool import RagTool


class FixedPDFSearchToolSchema(BaseModel):
    """PDFSearchTool 的输入。"""

    query: str = Field(
        ..., description="要用于搜索 PDF 内容的必填查询"
    )


class PDFSearchToolSchema(FixedPDFSearchToolSchema):
    """PDFSearchTool 的输入。"""

    pdf: str = Field(..., description="要搜索的必填 PDF 路径")


class PDFSearchTool(RagTool):
    name: str = "搜索 PDF 内容"
    description: str = (
        "一个可以用来从 PDF 内容中进行语义搜索的工具。"
    )
    args_schema: Type[BaseModel] = PDFSearchToolSchema

    def __init__(self, pdf: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if pdf is not None:
            self.add(pdf)
            self.description = f"一个可以用来在 {pdf} PDF 内容中进行语义搜索的工具。"
            self.args_schema = FixedPDFSearchToolSchema
            self._generate_description()

    @model_validator(mode="after")
    def _set_default_adapter(self):
        if isinstance(self.adapter, RagTool._AdapterPlaceholder):
            from embedchain import App

            from crewai_tools.adapters.pdf_embedchain_adapter import (
                PDFEmbedchainAdapter,
            )

            app = App.from_config(config=self.config) if self.config else App()
            self.adapter = PDFEmbedchainAdapter(
                embedchain_app=app, summarize=self.summarize
            )

        return self

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        kwargs["data_type"] = DataType.PDF_FILE
        super().add(*args, **kwargs)

    def _before_run(
        self,
        query: str,
        **kwargs: Any,
    ) -> Any:
        if "pdf" in kwargs:
            self.add(kwargs["pdf"])
