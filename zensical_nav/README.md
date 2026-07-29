# Zensical Markdown Extensions

本项目包含 Zensical 使用的 Markdown 扩展，以及支持手动导航与自动导航混排的 `zensical-nav` 工具。

## 安装

```bash
pip install -e .
```

## 混合导航

Zensical 当前尚未公开第三方插件 API，因此 `zensical-nav` 会先把自动导航占位符展开为标准 `nav`，再调用 Zensical。它通过启动自身的 Python 解释器执行 `python -m zensical`，因此始终委派给同一个虚拟环境，不依赖 `PATH` 中的其他 `zensical` 命令。构建和预览时需要使用：

```bash
zensical-nav build -f mkdocs.yml
zensical-nav serve -f mkdocs.yml
```

查看展开结果而不构建：

```bash
zensical-nav expand -f mkdocs.yml
```

### 配置示例

```yaml
zensical_nav:
  recursive: true
  include_index: true
  allow_empty: false

nav:
  - Home:
    - index.md
  - Computer Science:
    - cs/index.md
    - missing-semester: cs/missing-semester.md
  - Reading:
    - reading/index.md
    - auto: reading
```

`Home` 和 `Computer Science` 完全手动维护；`Reading` 保留手动固定的首页，其余文章和子目录从 `docs/reading` 自动生成。手动列出的 Markdown 页面不会被自动块重复添加。

自动块也支持完整写法，并可覆盖全局默认值：

```yaml
- auto:
    path: reading
    recursive: true
    include_index: false
    allow_empty: false
```

选项：

- `path`：相对 `docs_dir` 的目录，必填。
- `recursive`：是否递归生成子目录，默认 `true`。
- `include_index`：是否自动添加每个目录下的 `index.md`，默认 `true`。手动列出的 `index.md` 始终会自动去重。
- `allow_empty`：是否允许自动块不生成任何页面，默认 `false`。

页面标题依次取自 YAML front matter 的 `title`、第一个一级标题和文件名。目录标题使用目录名。`index.md` 排在同目录其他页面之前，其余条目按名称稳定排序。

> 直接运行 `zensical build` 或 `zensical serve` 不会识别 `auto` 占位符。待 Zensical 发布官方模块 API 后，导航生成核心可直接接入该接口。
