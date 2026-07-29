# Homepage terminal hero

This folder documents the custom landing page for the blog root. It is outside `docs/` so Zensical does not publish it or include it in generated navigation.

## Requirements

The homepage renders these strings exactly:

- Title: `不擅生长的大脑`
- Subtitle: `这里是Amarantosy的笔记本`
- Terminal wordmark: `AMARANTOSY`

On desktop, the title group and terminal share the vertical center of the available homepage area. The terminal is shifted right by one fifth of its own width and deliberately clipped by the viewport. On mobile, the terminal returns to the normal page width above the title without clipping. The first viewport contains only the two-line title (`不擅生长` / `的大脑`), subtitle, terminal, and a built-in `octicons-chevron-down-12` scroll cue. The rendered `docs/index.md` body starts below that viewport and appears after scrolling or activating the cue.

## Implementation

- `docs/index.md` selects the homepage-only template, hides navigation and the table of contents, and supplies the introduction rendered below the hero.
- `overrides/home.html` extends the normal theme and replaces only its content container. It contains the semantic title/subtitle, a static line-art brain behind the `大脑` characters, the terminal's complete static end state, the Material scroll cue, and the rendered `page.content`.
- `docs/css/home.css` owns the responsive layout, theme colors, brain backdrop, terminal chrome, character grid, and cursor animation.
- `docs/js/home-terminal.js` types the command and reveals the wordmark from left to right. It runs only when the homepage terminal exists and leaves normal article pages unchanged.
- `mkdocs.yml` loads the homepage stylesheet and controller through `extra_css` and `extra_javascript`.

The title and subtitle load the specified [Huiwen Mincho stylesheet](https://cn-font.claude-code-best.win/packages/hwmct/dist/%E6%B1%87%E6%96%87%E6%98%8E%E6%9C%9D%E4%BD%93/result.css) and use its declared `Huiwen-mincho` family at the available weight of 400. The site name and primary navigation use the same family globally through `docs/css/font_modified.css`, including desktop tabs and the mobile navigation drawer. Songti system fonts remain as network-failure fallbacks.

The terminal uses a system monospace stack and Material/Zensical color variables around a consistently dark screen. The complete command and wordmark are present in the HTML, so disabling JavaScript or enabling `prefers-reduced-motion: reduce` displays the final state immediately. The animated version plays once, pauses its timing while the document is hidden, and stops on the complete wordmark.

## Animation references and license

The implementation was checked against mature open-source projects before development:

- [Termynal](https://github.com/ines/termynal) — MIT-licensed reference and code basis for the dependency-free `data-ty` API and async/await character typing model. `docs/js/home-terminal.js` retains the Termynal copyright and MIT permission notice, then adds the site-specific wordmark reveal, visibility-aware timing, and reduced-motion behavior.
- [Ghostty website](https://github.com/ghostty-org/website/tree/main/src/components/animated-terminal) — MIT-licensed reference for a terminal-shaped hero, text-frame animation, pausing away from the visible page, and reduced-motion handling.
- [OpenCode logo](https://github.com/anomalyco/opencode/blob/dev/packages/web/src/assets/logo-dark.svg) — MIT-licensed visual reference for a compact grid-based wordmark. No SVG path or asset is copied.

The seven-row `AMARANTOSY` character matrix and its `░▒▓█` resolving animation are original to this site. The implementation does not bundle Termynal's stylesheet or any Ghostty/OpenCode asset, framework, terminal emulator, canvas renderer, or particle dependency.

## Verification

From the repository root:

```bash
node --check docs/js/home-terminal.js
.venv/bin/python -m unittest discover -s tests
PATH="$PWD/.venv/bin:$PATH" .venv/bin/zensical-nav expand -f mkdocs.yml
PATH="$PWD/.venv/bin:$PATH" .venv/bin/zensical-nav build -f mkdocs.yml
PATH="$PWD/.venv/bin:$PATH" .venv/bin/zensical-nav serve -f mkdocs.yml
```

Check the homepage in light and dark themes, at desktop and mobile widths, and with reduced motion enabled. Confirm the title breaks only between `不擅生长` and `的大脑`, there is no horizontal scrolling, the command types before the complete `AMARANTOSY` wordmark appears, and the introduction is below the initial viewport. Activate the Material down-chevron and confirm it scrolls to the current `docs/index.md` content. Switch to another browser tab during playback and confirm the animation continues from the same point after returning.

With JavaScript disabled or reduced motion enabled, confirm the complete command, wordmark, and `ready` line render without an entrance animation or blinking cursor. Confirm a normal article page still uses the standard content layout and footer navigation.
