"""Multion 工具规范。"""

from typing import Any, Optional

from crewai_tools.tools.base_tool import BaseTool


class MultiOnTool(BaseTool):
    """用于封装 MultiOn 浏览功能的工具。"""

    name: str = "Multion 浏览工具"
    description: str = """Multion 使大型语言模型能够使用自然语言指令控制网络浏览器。
            如果状态为“继续”，则重新发出相同的指令以继续执行
        """
    multion: Optional[Any] = None
    session_id: Optional[str] = None
    local: bool = False
    max_steps: int = 3

    def __init__(
        self,
        api_key: Optional[str] = None,
        local: bool = False,
        max_steps: int = 3,
        **kwargs,
    ):
        super().__init__(**kwargs)
        try:
            from multion.client import MultiOn  # type: ignore
        except ImportError:
            raise ImportError(
                "找不到 `multion` 包，请运行 `pip install multion`"
            )
        self.session_id = None
        self.local = local
        self.multion = MultiOn(api_key=api_key)
        self.max_steps = max_steps

    def _run(
        self,
        cmd: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        """
        使用给定的命令运行 Multion 客户端。

        参数：
            cmd (str)：用于网页浏览的详细且具体的自然语言指令

            *args (Any)：要传递给 Multion 客户端的附加参数
            **kwargs (Any)：要传递给 Multion 客户端的附加关键字参数
        """

        browse = self.multion.browse(
            cmd=cmd,
            session_id=self.session_id,
            local=self.local,
            max_steps=self.max_steps,
            *args,
            **kwargs,
        )
        self.session_id = browse.session_id

        return browse.message + "\n\n 状态：" + browse.status
