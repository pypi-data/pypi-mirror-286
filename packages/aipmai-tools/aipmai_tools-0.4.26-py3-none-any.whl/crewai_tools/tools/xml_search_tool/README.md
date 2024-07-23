# XMLSearchTool

## 描述
XMLSearchTool 是一款先进的 RAG 工具，专为在 XML 文件中进行语义搜索而设计。此工具非常适合需要高效地解析和提取 XML 内容信息的的用户，它支持输入搜索查询和可选的 XML 文件路径。通过指定 XML 路径，用户可以更精确地将搜索目标定位到该文件的内容，从而获得更相关的搜索结果。

## 安装
要开始使用 XMLSearchTool，您必须首先安装 crewai_tools 包。可以使用以下命令轻松完成：

```shell
pip install 'crewai[tools]'
```

## 示例
以下两个示例演示了如何使用 XMLSearchTool。第一个示例展示了在特定 XML 文件中进行搜索，而第二个示例说明了如何在没有预定义 XML 路径的情况下启动搜索，从而提供了搜索范围的灵活性。

```python
from crewai_tools.tools.xml_search_tool import XMLSearchTool

# 允许代理在执行期间了解到任何 XML 文件的路径时，在其中搜索内容
tool = XMLSearchTool()

# 或者

# 使用特定的 XML 文件路径初始化工具，以便仅在该文档中进行搜索
tool = XMLSearchTool(xml='path/to/your/xmlfile.xml')
```

## 参数
- `xml`：这是您要搜索的 XML 文件的路径。它在工具初始化期间是一个可选参数，但必须在初始化时提供，或者作为 `run` 方法参数的一部分提供，才能执行搜索。

## 自定义模型和嵌入

默认情况下，该工具使用 OpenAI 进行嵌入和摘要。要自定义模型，您可以使用如下配置字典：

```python
tool = XMLSearchTool(
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
