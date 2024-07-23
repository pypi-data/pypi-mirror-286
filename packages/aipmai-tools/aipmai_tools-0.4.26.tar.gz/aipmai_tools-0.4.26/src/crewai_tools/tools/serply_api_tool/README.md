# Serply API 文档

## 描述

此工具旨在根据用户提供的查询，从互联网上的文本内容中执行网络/新闻/学术搜索。它利用 [Serply.io](https://serply.io) API 获取并显示与查询最相关的搜索结果。

## 安装

要将此工具整合到您的项目中，请按照以下安装说明进行操作：

```shell
pip install 'crewai[tools]'
```

## 示例

## 网络搜索

以下示例演示了如何初始化该工具并使用给定的查询执行网络搜索：

```python
from crewai_tools import SerplyWebSearchTool

# 初始化该工具以获得互联网搜索功能
tool = SerplyWebSearchTool()

# 将搜索限制增加到 100 个结果
tool = SerplyWebSearchTool(limit=100)

# 更改结果语言（fr - 法语）
tool = SerplyWebSearchTool(hl="fr")
```

## 新闻搜索

以下示例演示了如何初始化该工具并使用给定的查询执行新闻搜索：

```python
from crewai_tools import SerplyNewsSearchTool

# 初始化该工具以获得互联网搜索功能
tool = SerplyNewsSearchTool()

# 更改国家/地区新闻（JP - 日本）
tool = SerplyNewsSearchTool(proxy_location="JP")
```

## 学术搜索

以下示例演示了如何初始化该工具并使用给定的查询执行学术文章搜索：

```python
from crewai_tools import SerplyScholarSearchTool

# 初始化该工具以获得互联网搜索功能
tool = SerplyScholarSearchTool()

# 更改国家/地区新闻（GB - 英国）
tool = SerplyScholarSearchTool(proxy_location="GB")
```

## 招聘搜索

以下示例演示了如何初始化该工具并在美国搜索招聘信息：

```python
from crewai_tools import SerplyJobSearchTool

# 初始化该工具以获得互联网搜索功能
tool = SerplyJobSearchTool()
```

## 网页转 Markdown

以下示例演示了如何初始化该工具并获取网页并将其转换为 Markdown：

```python
from crewai_tools import SerplyWebpageToMarkdownTool

# 初始化该工具以获得互联网搜索功能
tool = SerplyWebpageToMarkdownTool()

# 更改发出请求的国家/地区（DE - 德国）
tool = SerplyWebpageToMarkdownTool(proxy_location="DE")
```

## 组合多个工具

以下示例演示了执行 Google 搜索以查找相关文章。然后，将这些文章转换为 Markdown 格式，以便更轻松地提取关键点。

```python
from crewai import Agent
from crewai_tools import SerplyWebSearchTool, SerplyWebpageToMarkdownTool

search_tool = SerplyWebSearchTool()
convert_to_markdown = SerplyWebpageToMarkdownTool()

# 创建具有记忆和详细模式的高级研究员代理
researcher = Agent(
  role='高级研究员',
  goal='发现{topic}中的突破性技术',
  verbose=True,
  memory=True,
  backstory=(
    "在好奇心的驱使下，您处于"
    "创新的最前沿，渴望探索和分享可能改变"
    "世界的知识。"
  ),
  tools=[search_tool, convert_to_markdown],
  allow_delegation=True
)
```

## 入门步骤

要有效使用 `SerplyApiTool`，请按照以下步骤操作：

1. **安装软件包**：确认您的 Python 环境中已安装 `crewai[tools]` 软件包。
2. **获取 API 密钥**：通过在 [Serply.io](https://serply.io) 上注册免费帐户来获取 `serper.dev` API 密钥。
3. **配置环境**：将您获得的 API 密钥存储在名为 `SERPLY_API_KEY` 的环境变量中，以便该工具使用。

## 结论

通过将 `SerplyApiTool` 集成到 Python 项目中，用户可以直接从其应用程序中进行实时搜索、获取相关的互联网新闻。通过遵循提供的设置和使用指南，可以简化并将此工具轻松整合到项目中。
