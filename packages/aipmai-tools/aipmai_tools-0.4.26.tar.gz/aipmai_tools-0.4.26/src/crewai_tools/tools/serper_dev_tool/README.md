## SerperDevTool 文档

## 描述

此工具旨在根据用户提供的查询，从互联网上的文本内容中执行语义搜索。它利用 `serper.dev` API 获取并显示与查询最相关的搜索结果。

## 安装

要将此工具整合到您的项目中，请按照以下安装说明进行操作：

```shell
pip install 'crewai[tools]'
```

## 示例

以下示例演示了如何初始化该工具并使用给定的查询执行搜索：

```python
from crewai_tools import SerperDevTool

# 初始化该工具以获得互联网搜索功能
tool = SerperDevTool()
```

## 入门步骤

要有效使用 `SerperDevTool`，请按照以下步骤操作：

1. **安装软件包**：确认您的 Python 环境中已安装 `crewai[tools]` 软件包。
2. **获取 API 密钥**：通过在 `serper.dev` 上注册免费帐户来获取 `serper.dev` API 密钥。
3. **配置环境**：将您获得的 API 密钥存储在名为 `SERPER_API_KEY` 的环境变量中，以便该工具使用。

## 结论

通过将 `SerperDevTool` 集成到 Python 项目中，用户可以直接从其应用程序中进行实时、相关的互联网搜索。通过遵循提供的设置和使用指南，可以简化并将此工具轻松整合到项目中。
