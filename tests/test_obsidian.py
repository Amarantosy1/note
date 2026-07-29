import tempfile
import unittest
import warnings
from pathlib import Path

from markdown import markdown

from zensical_obsidian import ObsidianWikiWarning


class ObsidianWikiExtensionTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.docs = Path(self.temporary_directory.name)
        self.write("index.md", "# 首页")
        self.write("reading/夏目漱石/《我是猫》.md", "# 我是猫\n\n## 一\n\n## Hello *world*")
        self.write("reading/福尔摩斯/index.md", "# 福尔摩斯")
        self.write("reading/夏目漱石/cover.webp", "image")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def write(self, relative_path, content):
        path = self.docs / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def render(self, source, strict=False, **config):
        extension_config = {
            "docs_dir": str(self.docs),
            "base_url": "/notes",
            "strict": strict,
        }
        extension_config.update(config)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            html = markdown(
                source,
                extensions=["fenced_code", "toc", "zensical_obsidian"],
                extension_configs={"zensical_obsidian": extension_config},
            )
        return html, caught

    def test_resolves_unique_chinese_page_and_alias(self):
        html, caught = self.render("[[《我是猫》]] 和 [[《我是猫》.md|猫]]")
        self.assertEqual(
            html,
            '<p><a class="obsidian-wiki-link" href="/notes/reading/%E5%A4%8F%E7%9B%AE%E6%BC%B1%E7%9F%B3/%E3%80%8A%E6%88%91%E6%98%AF%E7%8C%AB%E3%80%8B/">《我是猫》</a> 和 <a class="obsidian-wiki-link" href="/notes/reading/%E5%A4%8F%E7%9B%AE%E6%BC%B1%E7%9F%B3/%E3%80%8A%E6%88%91%E6%98%AF%E7%8C%AB%E3%80%8B/">猫</a></p>',
        )
        self.assertEqual(caught, [])

    def test_resolves_explicit_path_and_index(self):
        html, _ = self.render("[[reading/夏目漱石/《我是猫》]] [[index]] [[福尔摩斯]]")
        self.assertIn('href="/notes/reading/', html)
        self.assertIn('href="/notes/"', html)
        self.assertIn('href="/notes/reading/%E7%A6%8F%E5%B0%94%E6%91%A9%E6%96%AF/"', html)

    def test_resolves_heading_with_toc_slug(self):
        html, caught = self.render("[[《我是猫》#一]] [[《我是猫》#Hello world|英文标题]]")
        self.assertIn('/#_2">《我是猫》</a>', html)
        self.assertIn('/#hello-world">英文标题</a>', html)
        self.assertEqual(caught, [])

    def test_resolves_image(self):
        html, caught = self.render("![[cover.webp]]")
        self.assertIn(
            '<img alt="cover.webp" class="obsidian-wiki-image obsidian-wiki-image--centered"',
            html,
        )
        self.assertIn('src="/notes/reading/', html)
        self.assertIn("--obsidian-image-max-width: 800px", html)
        self.assertIn("--obsidian-image-max-height: 600px", html)
        self.assertIn("--obsidian-image-border-radius: 0.5rem", html)
        self.assertEqual(caught, [])

    def test_resolves_image_with_width_and_dimensions(self):
        html, caught = self.render("![[cover.webp|300]] ![[cover.webp|320x200]]")
        self.assertEqual(html.count('alt="cover.webp"'), 2)
        self.assertIn("--obsidian-image-max-width: 300px", html)
        self.assertIn("--obsidian-image-max-width: 320px", html)
        self.assertIn("--obsidian-image-max-height: 200px", html)
        self.assertEqual(html.count("--obsidian-image-max-height: 600px"), 1)
        self.assertEqual(caught, [])

    def test_applies_custom_image_defaults_and_can_disable_centering(self):
        html, caught = self.render(
            "![[cover.webp]]",
            image_max_width=720,
            image_max_height=480,
            image_center=False,
            image_border_radius="12px",
        )
        self.assertIn('class="obsidian-wiki-image"', html)
        self.assertNotIn("obsidian-wiki-image--centered", html)
        self.assertIn("--obsidian-image-max-width: 720px", html)
        self.assertIn("--obsidian-image-max-height: 480px", html)
        self.assertIn("--obsidian-image-border-radius: 12px", html)
        self.assertEqual(caught, [])

    def test_accepts_zero_image_border_radius(self):
        html, caught = self.render("![[cover.webp]]", image_border_radius=0)
        self.assertIn("--obsidian-image-border-radius: 0", html)
        self.assertEqual(caught, [])

    def test_marks_invalid_image_dimensions_unsupported(self):
        invalid = [
            "0",
            "-1",
            "300px",
            "x200",
            "300x",
            "300x0",
            "300x200x100",
            "300|200",
            "３００",
            "9" * 5000,
        ]
        html, caught = self.render(" ".join(f"![[cover.webp|{size}]]" for size in invalid))
        self.assertEqual(html.count("obsidian-wiki-link--unsupported"), len(invalid))
        self.assertEqual(len(caught), len(invalid))

    def test_invalid_image_dimensions_raise_in_strict_mode(self):
        with self.assertRaisesRegex(ValueError, "target invalid"):
            self.render("![[cover.webp|300px]]", strict=True)

    def test_rejects_invalid_image_configuration(self):
        invalid_configs = [
            {"image_max_width": 0},
            {"image_max_height": "600px"},
            {"image_center": "center"},
            {"image_border_radius": "calc(1rem + 1px)"},
            {"image_border_radius": "-1px"},
        ]
        for config in invalid_configs:
            with self.subTest(config=config), self.assertRaises(ValueError):
                self.render("![[cover.webp]]", **config)

    def test_marks_missing_page_and_image(self):
        html, caught = self.render("[[不存在]] ![[missing.webp]]")
        self.assertIn("obsidian-wiki-link--missing", html)
        self.assertIn("obsidian-wiki-link--image", html)
        self.assertEqual(len(caught), 2)
        self.assertTrue(all(item.category is ObsidianWikiWarning for item in caught))

    def test_marks_ambiguous_page_and_lists_sorted_candidates(self):
        self.write("a/shared.md", "# A")
        self.write("b/shared.md", "# B")
        html, caught = self.render("[[shared]]")
        self.assertIn("obsidian-wiki-link--ambiguous", html)
        self.assertIn('data-candidates="a/shared.md;b/shared.md"', html)
        self.assertEqual(len(caught), 1)

    def test_marks_missing_heading(self):
        html, caught = self.render("[[《我是猫》#不存在]]")
        self.assertIn("obsidian-wiki-link--missing", html)
        self.assertEqual(len(caught), 1)

    def test_marks_duplicate_heading_ambiguous(self):
        self.write("duplicate.md", "# Duplicate\n\n## API\n\n## API")
        html, caught = self.render("[[duplicate#API]]")
        self.assertIn("obsidian-wiki-link--ambiguous", html)
        self.assertIn("duplicate.md#api;duplicate.md#api_1", html)
        self.assertEqual(len(caught), 1)

    def test_marks_note_and_heading_embeds_unsupported(self):
        html, caught = self.render("![[《我是猫》]] ![[《我是猫》#一]]")
        self.assertEqual(html.count("obsidian-wiki-link--unsupported"), 2)
        self.assertEqual(len(caught), 2)

    def test_rejects_path_traversal_and_url_scheme(self):
        html, caught = self.render("[[../secret]] [[https://example.com]]")
        self.assertEqual(html.count("obsidian-wiki-link--invalid"), 2)
        self.assertEqual(len(caught), 2)

    def test_escapes_alias_and_attributes(self):
        html, _ = self.render('[[《我是猫》|<script>alert("x")</script>]]')
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_does_not_transform_escaped_or_code_syntax(self):
        source = "\\[[《我是猫》]] `[[《我是猫》]]`\n\n```text\n[[《我是猫》]]\n```"
        html, caught = self.render(source)
        self.assertNotIn("obsidian-wiki-link", html)
        self.assertEqual(caught, [])

    def test_does_not_transform_raw_html_block(self):
        html, caught = self.render("<div>\n[[《我是猫》]]\n</div>")
        self.assertNotIn("obsidian-wiki-link", html)
        self.assertEqual(caught, [])

    def test_does_not_transform_inline_html_attributes(self):
        html, caught = self.render('<span data-target="[[《我是猫》]]">内容</span>')
        self.assertIn('data-target="[[《我是猫》]]"', html)
        self.assertNotIn("obsidian-wiki-link", html)
        self.assertEqual(caught, [])

    def test_strict_mode_raises(self):
        with self.assertRaisesRegex(ValueError, "target missing"):
            self.render("[[不存在]]", strict=True)


if __name__ == "__main__":
    unittest.main()
