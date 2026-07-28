import unittest

from markdown import markdown


class HardBreakExtensionTest(unittest.TestCase):
    def render(self, source):
        return markdown(source, extensions=["fenced_code", "zensical_hardbreak"])

    def test_converts_single_newline(self):
        self.assertEqual(
            self.render("第一行\n第二行"),
            "<p>第一行<br />\n第二行</p>",
        )

    def test_preserves_paragraph_break(self):
        self.assertEqual(
            self.render("第一段\n\n第二段"),
            "<p>第一段</p>\n<p>第二段</p>",
        )

    def test_does_not_modify_fenced_code(self):
        self.assertEqual(
            self.render("```text\na\nb\n```"),
            '<pre><code class="language-text">a\nb\n</code></pre>',
        )


if __name__ == "__main__":
    unittest.main()
