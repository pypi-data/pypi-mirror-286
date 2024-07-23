# JSONSearchTool

## 描述

此工具用于在 JSON 文件内容中执行 RAG 搜索。它允许用户使用特定的 JSON 路径启动搜索，将搜索操作集中在该特定 JSON 文件中。如果在初始化时提供了路径，则该工具会将其搜索范围限制在指定的 JSON 文件内，从而提高搜索结果的精度。

## 安装

通过在终端中执行以下命令来安装 crewai_tools 包：

```shell
pip install 'crewai[tools]'
```

## 示例

以下示例演示了如何使用 JSONSearchTool 在 JSON 文件中进行搜索。您可以搜索任何 JSON 内容，也可以将搜索限制在特定的 JSON 文件中。

```python
from crewai_tools import JSONSearchTool

# 示例 1：初始化工具以在任何 JSON 内容中进行常规搜索。当路径已知或可以在执行期间发现时，此方法很有用。
tool = JSONSearchTool()

# 示例 2：使用特定的 JSON 路径初始化工具，将搜索限制在特定的 JSON 文件中。
tool = JSONSearchTool(json_path='./path/to/your/file.json')
```

## 参数

- `json_path` (str)：一个可选参数，用于定义要搜索的 JSON 文件的路径。仅当工具在初始化时没有指定 JSON 路径时才需要此参数。提供此参数会将搜索限制在指定的 JSON 文件中。

## 自定义模型和嵌入

默认情况下，该工具使用 OpenAI 进行嵌入和摘要。要自定义模型，可以使用如下配置字典：

```python
tool = JSONSearchTool(
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
