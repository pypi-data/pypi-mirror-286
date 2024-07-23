## SeleniumScrapingTool

## 描述

此工具专为高效的网页抓取而设计，使用户能够从网页中提取内容。它通过允许指定所需元素的 CSS 选择器来支持目标抓取。该工具的灵活性使其能够用于用户提供的任何网站 URL，使其成为满足各种网页抓取需求的多功能工具。

## 安装

安装 crewai_tools 软件包
```
pip install 'crewai[tools]'
```

## 示例

```python
from crewai_tools import SeleniumScrapingTool

# 示例 1：抓取其执行期间找到的任何网站
tool = SeleniumScrapingTool()

# 示例 2：抓取整个网页
tool = SeleniumScrapingTool(website_url='https://example.com')

# 示例 3：从网页中抓取特定的 CSS 元素
tool = SeleniumScrapingTool(website_url='https://example.com', css_element='.main-content')

# 示例 4：使用可选参数进行自定义抓取
tool = SeleniumScrapingTool(website_url='https://example.com', css_element='.main-content', cookie={'name': 'user', 'value': 'John Doe'})
```

## 参数

- `website_url`：必填。要抓取的网站的 URL。
- `css_element`：必填。要从网站抓取的特定元素的 CSS 选择器。
- `cookie`：可选。包含 Cookie 信息的字典。此参数允许工具使用 Cookie 信息模拟会话，从而提供对可能仅限登录用户访问的内容的访问权限。
- `wait_time`：可选。工具在加载网站和设置 Cookie 后，在抓取内容之前等待的秒数。这允许动态内容正确加载。
