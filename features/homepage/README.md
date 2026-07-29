# Homepage guitar hero

This folder documents the custom landing page for the blog root. It is outside `docs/` so Zensical does not publish it or include it in generated navigation.

## Requirements

The homepage renders these strings exactly:

- Title: `不擅生长的大脑`
- Subtitle: `这里是Amarantosy的笔记本`

The title sits at the lower left of the available homepage content area. A self-drawn line-art guitar sits at the lower right and emits animated music notes. The homepage does not display the previous/next page footer navigation.

## Implementation

- `docs/index.md` selects the homepage-only template and hides navigation, table of contents, and footer pagination for this page.
- `overrides/home.html` extends the normal theme and replaces only its content container. It contains the semantic title/subtitle, an inline SVG guitar, and a static line-art brain behind the `大脑` characters.
- `docs/css/home.css` owns the responsive layout, theme colors, the static brain backdrop, and the guitar's CSS-only floating-note/string animations. The brain has no drawing, morphing, motion-path, or entrance animation.
- `mkdocs.yml` loads `css/home.css` after the existing project stylesheets.

The title and subtitle load the specified [Huiwen Mincho stylesheet](https://cn-font.claude-code-best.win/packages/hwmct/dist/%E6%B1%87%E6%96%87%E6%98%8E%E6%9C%9D%E4%BD%93/result.css) and use its declared `Huiwen-mincho` family at the available weight of 400. The site name and primary navigation use the same family globally through `docs/css/font_modified.css`, including desktop tabs and the mobile navigation drawer. Songti system fonts remain as network-failure fallbacks.

The illustration uses `currentColor` and Material/Zensical color variables so it follows both the `default` and `slate` palettes. It is decorative and hidden from assistive technology. Under `prefers-reduced-motion: reduce`, the notes remain visible but all custom animation stops.

### Guitar construction references

The inline SVG is an original redraw, but its instrument proportions and hardware placement were checked against mature open-source icon libraries:

- [Phosphor Icons guitar](https://github.com/phosphor-icons/core/blob/main/assets/regular/guitar.svg) — MIT-licensed reference for the joined upper/lower bouts and neck-to-body relationship.
- [Font Awesome guitar](https://github.com/FortAwesome/Font-Awesome/blob/7.x/svgs/solid/guitar.svg) — CC BY 4.0 icon reference for the overall acoustic silhouette.
- [Game Icons guitar head](https://github.com/game-icons/icons/blob/master/delapouite/guitar-head.svg) — CC BY 3.0 reference for a three-per-side tuning-machine layout.

No source path data is embedded in this homepage. The final drawing uses six continuous strings, six bridge pins, a nut, a tapered fretboard, six tuner posts, and six external tuner keys.

### Animation references

The guitar's lightweight SVG/CSS animation architecture was checked against mature MIT-licensed GitHub projects before implementation:

- [Vivus](https://github.com/maxwellito/vivus) — reference for progressive SVG line drawing with `stroke-dashoffset` and coordinated path scenarios.
- [Anime.js](https://github.com/juliangarnier/anime) — reference for unified timelines, SVG attributes, and motion-path animation.

The homepage does not include either dependency or copy their assets. It implements the established techniques directly with original SVG paths, CSS keyframes, and native SVG `animateMotion`.

## Verification

From the repository root:

```bash
.venv/bin/python -m unittest discover -s tests
PATH="$PWD/.venv/bin:$PATH" .venv/bin/zensical-nav expand -f mkdocs.yml
PATH="$PWD/.venv/bin:$PATH" .venv/bin/zensical-nav build -f mkdocs.yml
PATH="$PWD/.venv/bin:$PATH" .venv/bin/zensical-nav serve -f mkdocs.yml
```

Check the homepage in light and dark themes, at desktop and mobile widths, and with reduced motion enabled. Confirm the exact strings are present, the title and illustration do not overlap, there is no horizontal scrolling, the music notes animate when motion is allowed, and “下一页” is not visible. Confirm a normal article page still uses the standard content layout and footer navigation.
