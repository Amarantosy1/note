# zensical_glightbox

`zensical_glightbox` 是针对 Zensical 的本地 Markdown 图片灯箱扩展，迁移自 [`mkdocs-glightbox`](https://github.com/blueswen/mkdocs-glightbox) 的核心设计。它无需 MkDocs 插件钩子或 `selectolax`，而是在 Python-Markdown 的 ElementTree 阶段直接包装图片。

## 功能

扩展默认处理所有文章图片，包括：

```markdown
![标准 Markdown 图片](image.png)
![[Obsidian image.webp]]
```

生成的图片会被一个 `.glightbox` 链接包装，点击后使用本地托管的 GLightbox 3.3.1 放大。支持触摸导航、缩放、拖动、打开/关闭动画、键盘操作和 Material 明暗主题。

以下图片不会被包装：

- 已经位于链接 `<a>` 中的图片；
- 带有 `emojione`、`twemoji` 或 `gemoji` 类的 emoji；
- 带有 `off-glb` 类的图片；
- 带有 `skip_classes` 配置中任一类名的图片。

使用 `attr_list` 时可以关闭单张图片的灯箱：

```markdown
![不放大的图片](image.png){ .off-glb }
```

## 配置

扩展应放在 `zensical_obsidian` 后面，以便同时处理 Obsidian 图片：

```yaml
markdown_extensions:
  - zensical_obsidian:
      docs_dir: docs
  - zensical_glightbox:
      touch_navigation: true
      loop: false
      effect: zoom
      slide_effect: slide
      zoomable: true
      draggable: true
      skip_classes: []
```

配置项：

- `touch_navigation`：启用触摸滑动，默认 `true`。
- `loop`：最后一张图片后循环，默认 `false`。
- `effect`：打开与关闭动画，可选 `zoom`、`fade`、`none`，默认 `zoom`。
- `slide_effect`：图片切换动画，可选 `slide`、`zoom`、`fade`、`none`，默认 `slide`。
- `zoomable`：允许继续缩放灯箱中的图片，默认 `true`。
- `draggable`：允许鼠标拖动切换图片，默认 `true`。
- `skip_classes`：额外跳过的图片 CSS 类名列表。

站点还需按顺序加载资源：

```yaml
extra_css:
  - vendor/glightbox/glightbox.min.css
  - css/glightbox-overrides.css

extra_javascript:
  - vendor/glightbox/glightbox.min.js
  - js/glightbox-init.js
```

## 来源与许可证

- GLightbox 3.3.1：MIT，资源与完整许可证位于 `docs/vendor/glightbox/`。
- mkdocs-glightbox 0.5.2：MIT，核心集成设计的来源。
- 详细来源、固定提交和 SHA-256 见 `THIRD_PARTY_NOTICES.md`。
