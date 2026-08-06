import unittest

from markdown import markdown


class ParagraphIndentExtensionTest(unittest.TestCase):
    def render(self, source, *extensions):
        return markdown(
            source,
            extensions=["zensical_paragraph_indent", *extensions],
        )

    def test_indents_body_paragraphs(self):
        self.assertEqual(
            self.render("第一段\n\n第二段"),
            '<p class="zensical-paragraph-indent">第一段</p>\n'
            '<p class="zensical-paragraph-indent">第二段</p>',
        )

    def test_indents_paragraph_with_inline_content(self):
        self.assertEqual(
            self.render("这是 **重要** 的 [链接](https://example.com)。"),
            '<p class="zensical-paragraph-indent">这是 <strong>重要</strong> 的 '
            '<a href="https://example.com">链接</a>。</p>',
        )

    def test_works_with_hardbreak(self):
        self.assertEqual(
            self.render("第一行\n第二行", "zensical_hardbreak"),
            '<p class="zensical-paragraph-indent">第一行<br />\n  第二行</p>',
        )

    def test_does_not_indent_heading(self):
        self.assertEqual(self.render("# 标题"), "<h1>标题</h1>")

    def test_does_not_indent_image_only_paragraph(self):
        self.assertEqual(
            self.render("![图片](image.png)"),
            '<p><img alt="图片" src="image.png" /></p>',
        )

    def test_indents_paragraph_containing_image_and_text(self):
        self.assertEqual(
            self.render("![图片](image.png) 图片说明"),
            '<p class="zensical-paragraph-indent"><img alt="图片" src="image.png" /> '
            "图片说明</p>",
        )

    def test_skips_structural_content(self):
        rendered = self.render(
            "> 引用\n\n- 列表项\n\n```text\n代码\n```\n\n| 表头 |\n| --- |\n| 单元格 |",
            "fenced_code",
            "tables",
        )
        self.assertNotIn('class="zensical-paragraph-indent"', rendered)
        self.assertIn("<blockquote>\n<p>引用</p>", rendered)
        self.assertIn("<li>列表项</li>", rendered)
        self.assertIn("<pre><code", rendered)
        self.assertIn("<td>单元格</td>", rendered)

    def test_does_not_duplicate_existing_class(self):
        from xml.etree import ElementTree

        from zensical_paragraph_indent import ParagraphIndentTreeprocessor

        root = ElementTree.fromstring(
            '<div><p class="zensical-paragraph-indent">正文</p></div>'
        )
        ParagraphIndentTreeprocessor(
            None,
            class_name="zensical-paragraph-indent",
            skip_classes=frozenset(),
        ).run(root)
        self.assertEqual(
            ElementTree.tostring(root, encoding="unicode"),
            '<div><p class="zensical-paragraph-indent">正文</p></div>',
        )

    def test_supports_custom_class_name(self):
        self.assertEqual(
            markdown(
                "正文",
                extensions=["zensical_paragraph_indent"],
                extension_configs={
                    "zensical_paragraph_indent": {"class_name": "article-indent"}
                },
            ),
            '<p class="article-indent">正文</p>',
        )

    def test_supports_skipped_ancestor_class(self):
        from xml.etree import ElementTree

        from zensical_paragraph_indent import ParagraphIndentTreeprocessor

        root = ElementTree.fromstring('<div class="article"><p>正文</p></div>')
        ParagraphIndentTreeprocessor(
            None,
            class_name="zensical-paragraph-indent",
            skip_classes=frozenset({"article"}),
        ).run(root)
        self.assertEqual(
            ElementTree.tostring(root, encoding="unicode"),
            '<div class="article"><p>正文</p></div>',
        )


if __name__ == "__main__":
    unittest.main()
