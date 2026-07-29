# zensical_obsidian

`zensical_obsidian` 为 Zensical/Markdown 提供 Obsidian 风格的页面链接与图片嵌入：

```markdown
[[页面]]
[[页面#标题|显示文字]]
![[image.webp]]
```

## 调整图片尺寸

图片嵌入支持 Obsidian 的数字尺寸语法：

```markdown
![[image.webp|300]]
![[image.webp|300x200]]
```

- `|300` 将图片最大宽度设为 300px，高度继续使用插件默认上限。
- `|300x200` 将图片最大宽度和最大高度分别设为 300px 与 200px。
- 尺寸必须是正整数，不接受单位、零或负数。
- 尺寸是响应式上限，不会强制拉伸图片。图片始终保持原始宽高比，也不会超出正文宽度。

## 配置

```yaml
markdown_extensions:
  - zensical_obsidian:
      docs_dir: docs
      base_url: /
      strict: false
      image_max_width: 800
      image_max_height: 600
      image_center: true
      image_border_radius: 0.5rem
```

图片配置项：

- `image_max_width`：未指定单图宽度时的最大宽度，单位为 px，默认 `800`。
- `image_max_height`：未指定单图高度时的最大高度，单位为 px，默认 `600`。
- `image_center`：是否默认水平居中图片，默认 `true`。
- `image_border_radius`：图片圆角，默认 `0.5rem`；支持非负的 `px`、`rem`、`em`、`%` 值以及 `0`。

`strict: true` 时，未找到、存在歧义或使用无效尺寸语法的目标会直接抛出错误；默认情况下会输出诊断标记并产生 `ObsidianWikiWarning`。
