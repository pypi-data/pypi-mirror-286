# DOCXSearchTool

## 描述

DOCXSearchTool 是一款专为在 DOCX 文档中进行语义搜索而设计的 RAG 工具。它使用户能够使用基于查询的搜索有效地搜索和提取 DOCX 文件中的相关信息。该工具对于数据分析、信息管理和研究任务非常宝贵，简化了在大型文档集合中查找特定信息的过程。

## 安装

在您的终端中运行以下命令来安装 crewai_tools 包：

```shell
pip install 'crewai[tools]'
```

## 示例

以下示例演示了如何初始化 DOCXSearchTool 以搜索任何 DOCX 文件的内容或使用特定的 DOCX 文件路径进行搜索。

```python
from crewai_tools import DOCXSearchTool

# 初始化工具以搜索任何 DOCX 文件的内容
tool = DOCXSearchTool()

# 或者

# 使用特定的 DOCX 文件初始化工具，以便代理只能搜索指定的 DOCX 文件的内容
tool = DOCXSearchTool(docx='path/to/your/document.docx')
```

## 参数

- `docx`：要搜索的特定 DOCX 文档的可选文件路径。如果在初始化期间未提供，则该工具允许稍后指定任何 DOCX 文件的内容路径以进行搜索。

## 自定义模型和嵌入

默认情况下，该工具使用 OpenAI 进行嵌入和摘要。要自定义模型，可以使用如下配置字典：

```python
tool = DOCXSearchTool(
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
