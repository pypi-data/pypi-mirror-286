# DirectorySearchTool

## 描述

此工具旨在对指定目录的内容执行语义搜索查询。它利用 RAG（检索增强生成）方法，提供了一种在给定目录的文件中进行语义导航的强大方法。该工具可以动态设置为搜索运行时指定的任何目录，也可以预先配置为在初始化时搜索特定目录。

## 安装

要开始使用 DirectorySearchTool，您需要安装 crewai_tools 包。在您的终端中执行以下命令：

```shell
pip install 'crewai[tools]'
```

## 示例

以下示例演示了如何针对不同的用例初始化 DirectorySearchTool 以及如何执行搜索：

```python
from crewai_tools import DirectorySearchTool

# 启用在运行时搜索任何指定目录
tool = DirectorySearchTool()

# 或者，将搜索限制在特定目录
tool = DirectorySearchTool(directory='/path/to/directory')
```

## 参数

- `directory`：此字符串参数指定要在其中进行搜索的目录。如果工具未在初始化时指定目录，则此参数是必需的；否则，工具将仅在初始化的目录中进行搜索。

## 自定义模型和嵌入

默认情况下，该工具使用 OpenAI 进行嵌入和摘要。要自定义模型，可以使用如下配置字典：

```python
tool = DirectorySearchTool(
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
