from typing import Any, Optional, Type
from pydantic import BaseModel, Field
from pypdf import PdfReader, PdfWriter, PageObject, ContentStream, NameObject, Font
from pathlib import Path


class PDFTextWritingToolSchema(BaseModel):
    """PDFTextWritingTool 的输入模式。"""
    pdf_path: str = Field(..., description="要修改的 PDF 文件的路径")
    text: str = Field(..., description="要添加到 PDF 的文本")
    position: tuple = Field(..., description="文本放置的 (x, y) 坐标元组")
    font_size: int = Field(default=12, description="文本的字体大小")
    font_color: str = Field(default="0 0 0 rg", description="文本的 RGB 颜色代码")
    font_name: Optional[str] = Field(default="F1", description="标准字体的字体名称")
    font_file: Optional[str] = Field(None, description="用于自定义字体的 .ttf 字体文件的路径")
    page_number: int = Field(default=0, description="要添加文本的页码")


class PDFTextWritingTool(RagTool):
    """一个用于在 PDF 中的特定位置添加文本的工具，支持自定义字体。"""
    name: str = "PDF 文本写入工具"
    description: str = "一个可以在 PDF 文档的特定位置写入文本的工具，可以选择嵌入自定义字体。"
    args_schema: Type[BaseModel] = PDFTextWritingToolSchema

    def run(self, pdf_path: str, text: str, position: tuple, font_size: int, font_color: str,
            font_name: str = "F1", font_file: Optional[str] = None, page_number: int = 0, **kwargs) -> str:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        if page_number >= len(reader.pages):
            return "页码超出范围。"

        page: PageObject = reader.pages[page_number]
        content = ContentStream(page["/Contents"].data, reader)

        if font_file:
            # 检查字体文件是否存在
            if not Path(font_file).exists():
                return "字体文件不存在。"

            # 嵌入自定义字体
            font_name = self.embed_font(writer, font_file)

        # 使用自定义或标准字体准备文本操作
        x_position, y_position = position
        text_operation = f"BT /{font_name} {font_size} Tf {x_position} {y_position} Td ({text}) Tj ET"
        content.operations.append([font_color])  # 设置颜色
        content.operations.append([text_operation])  # 添加文本

        # 用新内容替换旧内容
        page[NameObject("/Contents")] = content
        writer.add_page(page)

        # 保存新的 PDF
        output_pdf_path = "modified_output.pdf"
        with open(output_pdf_path, "wb") as out_file:
            writer.write(out_file)

        return f"文本已成功添加到 {output_pdf_path}。"

    def embed_font(self, writer: PdfWriter, font_file: str) -> str:
        """将 TTF 字体嵌入 PDF 并返回字体名称。"""
        with open(font_file, "rb") as file:
            font = Font.true_type(file.read())
        font_ref = writer.add_object(font)
        return font_ref
