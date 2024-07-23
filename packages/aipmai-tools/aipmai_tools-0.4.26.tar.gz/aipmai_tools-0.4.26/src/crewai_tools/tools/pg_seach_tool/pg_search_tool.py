from typing import Any, Type

from embedchain.loaders.postgres import PostgresLoader
from pydantic.v1 import BaseModel, Field

from ..rag.rag_tool import RagTool


class PGSearchToolSchema(BaseModel):
    """PGSearchTool 的输入。"""

    search_query: str = Field(
        ...,
        description="要用于搜索数据库内容的必需语义搜索查询",
    )


class PGSearchTool(RagTool):
    name: str = "搜索数据库的表内容"
    description: str = "一个可以用来从数据库表的内容中进行语义搜索的工具。"
    args_schema: Type[BaseModel] = PGSearchToolSchema
    db_uri: str = Field(..., description="必需的数据库 URI")

    def __init__(self, table_name: str, **kwargs):
        super().__init__(**kwargs)
        self.add(table_name)
        self.description = f"一个可以用来在 {table_name} 数据库表的内容中进行语义搜索的工具。"
        self._generate_description()

    def add(
        self,
        table_name: str,
        **kwargs: Any,
    ) -> None:
        kwargs["data_type"] = "postgres"
        kwargs["loader"] = PostgresLoader(config=dict(url=self.db_uri))
        super().add(f"SELECT * FROM {table_name};", **kwargs)

    def _run(
        self,
        search_query: str,
        **kwargs: Any,
    ) -> Any:
        return super()._run(query=search_query, **kwargs)
