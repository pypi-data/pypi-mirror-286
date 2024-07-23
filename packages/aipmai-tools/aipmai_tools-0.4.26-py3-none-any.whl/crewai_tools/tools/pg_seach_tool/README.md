## PGSearchTool

## 描述

此工具旨在促进 PostgreSQL 数据库表内的语义搜索。PGSearchTool 利用 RAG（检索和生成）技术，为用户提供了一种高效的数据库表内容查询方法，专为 PostgreSQL 数据库量身定制。它通过语义搜索查询简化了查找相关数据的过程，使其成为需要对 PostgreSQL 数据库中的大型数据集执行高级查询的用户的宝贵资源。

## 安装

要安装 `crewai_tools` 软件包并使用 PGSearchTool，请在终端中执行以下命令：

```shell
pip install 'crewai[tools]'
```

## 示例

以下示例展示了如何使用 PGSearchTool 对 PostgreSQL 数据库中的表进行语义搜索：

```python
from crewai_tools import PGSearchTool

# 使用数据库 URI 和目标表名初始化工具
tool = PGSearchTool(db_uri='postgresql://user:password@localhost:5432/mydatabase', table_name='employees')

```

## 参数

PGSearchTool 需要以下参数才能运行：

- `db_uri`：表示要查询的 PostgreSQL 数据库的 URI 的字符串。此参数是必需的，并且必须包含必要的身份验证详细信息和数据库的位置。
- `table_name`：指定将在其上执行语义搜索的数据库中表的名称的字符串。此参数是必需的。

## 自定义模型和嵌入

默认情况下，该工具使用 OpenAI 进行嵌入和摘要。要自定义模型，可以使用如下所示的配置字典：

```python
tool = PGSearchTool(
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
