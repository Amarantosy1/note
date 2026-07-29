# Third-party notices

This feature adapts the core integration design of the following MIT-licensed projects. The Python integration in this repository is an independent Markdown treeprocessor for Zensical and does not copy the upstream MkDocs plugin source verbatim.

## GLightbox 3.3.1

- Project: https://github.com/biati-digital/glightbox
- Version: 3.3.1
- License: MIT
- Local files:
  - `docs/vendor/glightbox/glightbox.min.css`
  - `docs/vendor/glightbox/glightbox.min.js`
  - `docs/vendor/glightbox/LICENSE.md`
- Source snapshot: vendored by `mkdocs-glightbox` commit `cd67e432a0684ef350a4987c2661e1189034815d`
- SHA-256:
  - CSS: `6d3f62d4d17969f9c70e9438cf671004725019e868123f2ebc295a006f8d5d2d`
  - JavaScript: `c67c59cdf980793b0216c9de9c6ebf688418838822af1e50b09439e3aa289ff3`

The complete GLightbox MIT license is preserved in `docs/vendor/glightbox/LICENSE.md`.

## mkdocs-glightbox 0.5.2

- Project: https://github.com/blueswen/mkdocs-glightbox
- Version: 0.5.2
- License: MIT
- Copyright: Copyright (c) 2022 Blueswen

The local implementation adapts these upstream ideas: wrapping eligible images with `.glightbox` anchors, the core GLightbox options, Material theme color compatibility, and reload behavior for instant navigation.

MIT License

Copyright (c) 2022 Blueswen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
