# zensical-document-dates

`zensical_document_dates` 是一个面向 Zensical 的 Python Markdown 扩展，用于在文档标题下方显示创建日期和最后修改日期。它受 MIT 许可的 [mkdocs-document-dates](https://github.com/jaywhj/mkdocs-document-dates) 启发，但针对 Zensical 的 Markdown 渲染上下文重新实现，不依赖 MkDocs 插件事件。

## 配置

```yaml
markdown_extensions:
  - zensical_document_dates:
      docs_dir: docs
      date_format: "%Y-%m-%d"
      tooltip_format: "%Y-%m-%d %H:%M:%S %Z"
      created_label: 创建于
      updated_label: 修改于
      exclude:
        - index.md
```

可用选项：

- `docs_dir`：Markdown 文档目录，默认 `docs`。
- `date_format`：页面中可见日期的 Python `strftime` 格式，默认 `%Y-%m-%d`。
- `tooltip_format`：鼠标悬停或键盘聚焦时，浮层中具体日期的 `strftime` 格式，默认 `%Y-%m-%d %H:%M:%S %Z`。
- `created_label` / `updated_label`：浮层和屏幕阅读器使用的日期语义标签；页面中分别显示 `timer-edit-outline` 和 `timer-plus-outline` 图标。
- `exclude`：相对于 `docs_dir` 的 Unix shell 风格路径匹配列表。
- `show_created` / `show_updated`：全局控制是否显示相应日期，默认均为 `true`。

单篇文章可以在 Front Matter 中设置 `show_created: false` 或 `show_updated: false`。

## 日期来源

创建日期按以下顺序选择：

1. Front Matter 的 `created`、`date.created` 或标量 `date`
2. Git 首次提交日期
3. 文件系统创建日期；不支持创建日期的平台回退到修改日期

修改日期按以下顺序选择：

1. Front Matter 的 `updated`、`modified`、`date.updated` 或 `date.modified`
2. Git 最近提交日期
3. 文件系统修改日期

支持 YAML 日期、日期时间和 ISO 8601 字符串：

```yaml
---
created: 2026-04-13
updated: 2026-07-29T14:30:00+08:00
---
```

也可以使用嵌套格式：

```yaml
---
date:
  created: 2026-04-13
  updated: 2026-07-29
---
```

为了在 CI 中可靠读取首次提交日期，检出仓库时应保留完整 Git 历史。例如 GitHub Actions 的 `actions/checkout` 需配置 `fetch-depth: 0`。
