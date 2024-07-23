# WebsiteSearchTool

## 描述
此工具专门用于在特定网站的内容中进行语义搜索。它利用检索增强生成 (RAG) 模型，在给定 URL 提供的信息中进行导航。用户可以灵活地在使用期间已知或发现的任何网站上启动搜索，或者将搜索集中在预定义的特定网站上。

## 安装
在终端中执行以下命令安装 crewai_tools 包：

```shell
pip install 'crewai[tools]'
```

## 示例
要将 WebsiteSearchTool 用于不同的用例，请遵循以下示例：

```python
from crewai_tools import WebsiteSearchTool

# 使工具能够搜索代理在其操作期间遇到或了解的任何网站
tool = WebsiteSearchTool()

# 或者

# 将工具限制为仅在特定网站的内容中搜索。
tool = WebsiteSearchTool(website='https://example.com')
```

## 参数
- `website` ：一个可选参数，用于指定要在其上执行搜索的有效网站 URL。如果工具在初始化时未指定特定网站，则此参数 becomes necessary。在 `WebsiteSearchToolSchema` 中，此参数是必需的。但是，在 `FixedWebsiteSearchToolSchema` 中，如果在工具初始化期间提供了网站，则此参数 becomes optional，因为它将仅在预定义网站的内容中进行搜索。

## 自定义模型和嵌入

默认情况下，该工具使用 OpenAI 进行嵌入和摘要。要自定义模型，您可以使用如下配置字典：

```python
tool = WebsiteSearchTool(
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
