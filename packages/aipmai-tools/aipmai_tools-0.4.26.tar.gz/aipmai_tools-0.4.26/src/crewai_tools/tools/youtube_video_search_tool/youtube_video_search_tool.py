from typing import Any, Optional, Type

from embedchain.models.data_type import DataType
from pydantic.v1 import BaseModel, Field

from ..rag.rag_tool import RagTool


class FixedYoutubeVideoSearchToolSchema(BaseModel):
    """YoutubeVideoSearchTool 的输入"""

    search_query: str = Field(
        ...,
        description="用于搜索 Youtube 视频内容的必需搜索查询",
    )


class YoutubeVideoSearchToolSchema(FixedYoutubeVideoSearchToolSchema):
    """YoutubeVideoSearchTool 的输入"""

    youtube_video_url: str = Field(
        ..., description="要搜索的 Youtube 视频网址的必需路径"
    )


class YoutubeVideoSearchTool(RagTool):
    name: str = "搜索 Youtube 视频内容"
    description: str = "一个可以用来从 Youtube 视频内容中进行语义搜索的工具。"
    args_schema: Type[BaseModel] = YoutubeVideoSearchToolSchema

    def __init__(self, youtube_video_url: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if youtube_video_url is not None:
            self.add(youtube_video_url)
            self.description = f"一个可以用来在 {youtube_video_url} Youtube 视频内容中进行语义搜索的工具。"
            self.args_schema = FixedYoutubeVideoSearchToolSchema
            self._generate_description()

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        kwargs["data_type"] = DataType.YOUTUBE_VIDEO
        super().add(*args, **kwargs)

    def _before_run(
        self,
        query: str,
        **kwargs: Any,
    ) -> Any:
        if "youtube_video_url" in kwargs:
            self.add(kwargs["youtube_video_url"])

    def _run(
        self,
        search_query: str,
        **kwargs: Any,
    ) -> Any:
        return super()._run(query=search_query, **kwargs)
