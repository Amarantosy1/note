# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development commands

Use the repository virtual environment so the installed Zensical and local extension entry points are consistent.

```bash
# Install the Python packages in editable mode
.venv/bin/python -m pip install -e .

# Build or serve the site after expanding `auto` navigation entries
PATH="$PWD/.venv/bin:$PATH" .venv/bin/zensical-nav build -f mkdocs.yml
PATH="$PWD/.venv/bin:$PATH" .venv/bin/zensical-nav serve -f mkdocs.yml

# Print the expanded configuration without building
PATH="$PWD/.venv/bin:$PATH" .venv/bin/zensical-nav expand -f mkdocs.yml

# Run the full unittest suite
.venv/bin/python -m unittest discover -s tests

# Run one test module or one test method
.venv/bin/python -m unittest tests.test_extension
.venv/bin/python -m unittest tests.test_extension.HardBreakExtensionTest.test_converts_single_newline
```

Do not invoke `zensical build` or `zensical serve` directly while `mkdocs.yml` contains `auto` navigation entries. `zensical-nav` must expand those entries before delegating to Zensical. The CLI delegates through `sys.executable -m zensical`, so it always uses the same virtual environment that launched `zensical-nav`.

There is no configured lint, formatter, or static type-check command in this repository.

## Architecture

This repository combines a Zensical 0.0.51 Material-compatible documentation site with three local Python packages registered through `pyproject.toml`.

- `mkdocs.yml` is the source of truth for the theme, plugins, Markdown extensions, navigation, palettes, and custom stylesheets.
- `docs/` contains published Markdown, images, and CSS. `site/` is generated output and should not be edited.
- `overrides/` contains Jinja templates layered over the installed Material-compatible theme through `theme.custom_dir`.
- `zensical_nav/` preprocesses `mkdocs.yml`. It combines manually listed pages with recursive `auto` sections, excludes duplicates, emits section index pages first, writes a temporary expanded config, and then invokes Zensical.
- `zensical_hardbreak/` is a Markdown inline extension that converts single newlines to hard breaks without changing paragraph or fenced-code behavior.
- `zensical_obsidian/` indexes pages and images under `docs/` and resolves Obsidian-style `[[wiki links]]` and `![[image embeds]]`, including aliases and headings. Its unresolved and ambiguous states are styled by `docs/css/obsidian_wiki.css`.
- `tests/` contains standard-library `unittest` coverage for the custom Markdown extensions.

Navigation in `mkdocs.yml` mixes explicit section index pages with `auto` entries. Keep section indexes explicit and let `zensical_nav` discover their descendants rather than duplicating generated entries manually.
