from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree

from markdown import markdown


class GlightboxExtensionTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.docs = Path(self.temporary_directory.name)
        image = self.docs / "cover.webp"
        image.write_bytes(b"image")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def render(self, source: str, *, extensions=None, extension_configs=None, **config) -> str:
        extension_names = extensions or ["attr_list", "zensical_glightbox"]
        configurations = dict(extension_configs or {})
        configurations["zensical_glightbox"] = config
        return markdown(
            source,
            extensions=extension_names,
            extension_configs=configurations,
        )

    def test_wraps_standard_markdown_image_and_preserves_attributes(self):
        html = self.render('![Cover](images/cover.png "Title"){ .hero width=320 }')
        root = ElementTree.fromstring(html)
        anchor = root.find("a")
        self.assertIsNotNone(anchor)
        self.assertEqual(anchor.get("class"), "glightbox")
        self.assertEqual(anchor.get("href"), "images/cover.png")
        self.assertEqual(anchor.get("data-type"), "image")
        options = json.loads(anchor.get("data-glightbox-options"))
        self.assertEqual(
            options,
            {
                "touchNavigation": True,
                "loop": False,
                "zoomable": True,
                "draggable": True,
                "openEffect": "zoom",
                "closeEffect": "zoom",
                "slideEffect": "slide",
            },
        )
        image = anchor.find("img")
        self.assertEqual(image.get("alt"), "Cover")
        self.assertEqual(image.get("title"), "Title")
        self.assertEqual(image.get("class"), "hero")
        self.assertEqual(image.get("width"), "320")

    def test_wraps_obsidian_image_and_preserves_visual_style(self):
        html = self.render(
            "![[cover.webp|300x200]]",
            extensions=["zensical_obsidian", "zensical_glightbox"],
            extension_configs={
                "zensical_obsidian": {
                    "docs_dir": str(self.docs),
                    "base_url": "/",
                }
            },
        )
        root = ElementTree.fromstring(html)
        anchor = root.find("a")
        image = anchor.find("img")
        self.assertEqual(anchor.get("href"), "/cover.webp")
        self.assertIn("obsidian-wiki-image--centered", image.get("class"))
        self.assertIn("--obsidian-image-max-width: 300px", image.get("style"))
        self.assertIn("--obsidian-image-max-height: 200px", image.get("style"))

    def test_skips_linked_emoji_and_disabled_images(self):
        source = (
            "[![Linked](linked.png)](target/)\n\n"
            "![Emoji](emoji.png){ .twemoji }\n\n"
            "![Disabled](disabled.png){ .off-glb }\n\n"
            "![Custom](custom.png){ .skip-lightbox }"
        )
        html = self.render(source, skip_classes=["skip-lightbox"])
        self.assertNotIn('class="glightbox"', html)
        self.assertIn('href="target/"', html)

    def test_wraps_multiple_nested_images_once(self):
        source = "- ![One](one.png)\n- **![Two](two.png)**"
        html = self.render(source)
        self.assertEqual(html.count('class="glightbox"'), 2)
        self.assertNotIn('<a class="glightbox" href="one.png"><a', html)

    def test_preserves_text_after_inline_image(self):
        html = self.render("Before ![Image](image.png) after")
        self.assertIn('</a> after</p>', html)
        self.assertNotIn('after</a>', html)

    def test_applies_valid_custom_options(self):
        html = self.render(
            "![Image](image.png)",
            touch_navigation=False,
            loop=True,
            effect="fade",
            slide_effect="none",
            zoomable=False,
            draggable=False,
        )
        root = ElementTree.fromstring(html)
        options = json.loads(root.find("a").get("data-glightbox-options"))
        self.assertEqual(
            options,
            {
                "touchNavigation": False,
                "loop": True,
                "zoomable": False,
                "draggable": False,
                "openEffect": "fade",
                "closeEffect": "fade",
                "slideEffect": "none",
            },
        )

    def test_rejects_invalid_configuration(self):
        invalid_configs = [
            {"touch_navigation": []},
            {"loop": []},
            {"zoomable": []},
            {"draggable": []},
            {"effect": "slide"},
            {"slide_effect": "spin"},
            {"skip_classes": "skip"},
            {"skip_classes": [""]},
            {"skip_classes": ["two classes"]},
        ]
        for config in invalid_configs:
            with self.subTest(config=config), self.assertRaises(ValueError):
                self.render("![Image](image.png)", **config)

    def test_custom_config_does_not_leak_into_next_instance(self):
        custom = self.render("![Image](image.png)", effect="none", skip_classes=["hero"])
        default = self.render("![Image](image.png){ .hero }")
        custom_root = ElementTree.fromstring(custom)
        default_root = ElementTree.fromstring(default)
        custom_options = json.loads(custom_root.find("a").get("data-glightbox-options"))
        default_options = json.loads(default_root.find("a").get("data-glightbox-options"))
        self.assertEqual(custom_options["openEffect"], "none")
        self.assertEqual(default_options["openEffect"], "zoom")
        self.assertEqual(default_root.find("a").get("class"), "glightbox")


if __name__ == "__main__":
    unittest.main()
