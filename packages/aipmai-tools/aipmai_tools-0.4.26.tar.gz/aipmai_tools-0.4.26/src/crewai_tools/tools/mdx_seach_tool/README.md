## MDXSearchTool

## 描述

MDX 搜索工具是 `crewai_tools` 软件包的关键组件，专为高级市场数据提取而设计，为需要即时获取人工智能领域市场洞察力的研究人员和分析师提供宝贵支持。它能够与各种数据源和工具交互，从而简化了高效获取、读取和组织市场数据的流程。

## 安装

要使用 MDX 搜索工具，请确保已安装 `crewai_tools` 软件包。如果尚未安装，请使用以下命令进行安装：

```shell
pip install 'crewai[tools]'
```

## 示例

配置和使用 MDX 搜索工具涉及设置环境变量并在 crewAI 项目中使用该工具进行市场调查。以下是一个简单的示例：

```python
from crewai_tools import MDXSearchTool

# 初始化工具，以便代理可以在执行过程中搜索任何了解到的 MDX 内容
tool = MDXSearchTool()

# 或

# 使用特定的 MDX 文件路径初始化工具，以便仅在该文档中进行搜索
tool = MDXSearchTool(mdx='path/to/your/document.mdx')
```

## 参数

- mdx：**可选** 用于搜索的 MDX 路径。可以在初始化时提供

## 自定义模型和嵌入

默认情况下，该工具使用 OpenAI 进行嵌入和摘要。要自定义模型，可以使用如下所示的配置字典：

```python
tool = MDXSearchTool(
    config=dict(
        llm=dict(
            provider="ollama", # 或 google, openai, anthropic, llama2, ...
            config=dict(
                model="llama2",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google",
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)
```
