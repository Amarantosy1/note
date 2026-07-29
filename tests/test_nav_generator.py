from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

from zensical_nav import NavConfigError, expand_nav


class NestedAutoNavigationTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.docs = self.root / "docs"
        self._write("reading/index.md", "# Reading")
        self._write("reading/其它/被讨厌的勇气.md", "# 被讨厌的勇气")
        self._write("reading/其它集/条目.md", "# 条目")
        self._write("reading/小说/作品.md", "# 作品")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_descendant_auto_owns_subtree_without_hiding_siblings(self):
        navigation = self._expand(
            [
                {
                    "Reading": [
                        "reading/index.md",
                        {"auto": "reading"},
                        {"其它": [{"auto": "reading/其它"}]},
                    ]
                }
            ]
        )

        self.assertEqual(
            navigation,
            [
                {
                    "Reading": [
                        "reading/index.md",
                        {"其它集": [{"条目": "reading/其它集/条目.md"}]},
                        {"小说": [{"作品": "reading/小说/作品.md"}]},
                        {"其它": [{"被讨厌的勇气": "reading/其它/被讨厌的勇气.md"}]},
                    ]
                }
            ],
        )
        self.assertEqual(self._count_path(navigation, "reading/其它/被讨厌的勇气.md"), 1)

    def test_descendant_auto_ownership_is_independent_of_declaration_order(self):
        parent_first = self._expand(
            [
                {"auto": "reading"},
                {"其它": [{"auto": "reading/其它"}]},
            ]
        )
        child_first = self._expand(
            [
                {"其它": [{"auto": "reading/其它"}]},
                {"auto": "reading"},
            ]
        )

        for navigation in (parent_first, child_first):
            self.assertEqual(self._count_path(navigation, "reading/其它/被讨厌的勇气.md"), 1)
            self.assertEqual(self._count_path(navigation, "reading/其它集/条目.md"), 1)
            self.assertEqual(self._count_path(navigation, "reading/小说/作品.md"), 1)

    def test_parent_auto_may_be_empty_after_descendant_takes_its_only_subtree(self):
        self._remove("reading/index.md")
        self._remove("reading/其它集/条目.md")
        self._remove("reading/小说/作品.md")

        navigation = self._expand(
            [
                {"auto": "reading"},
                {"其它": [{"auto": "reading/其它"}]},
            ]
        )

        self.assertEqual(
            navigation,
            [{"其它": [{"被讨厌的勇气": "reading/其它/被讨厌的勇气.md"}]}],
        )

    def test_nonrecursive_empty_parent_still_requires_allow_empty(self):
        self._remove("reading/index.md")

        with self.assertRaisesRegex(NavConfigError, "generated no pages"):
            self._expand(
                [
                    {"auto": {"path": "reading", "recursive": False}},
                    {"其它": [{"auto": "reading/其它"}]},
                ]
            )

    def _expand(self, nav: list[Any]) -> list[Any]:
        return expand_nav({"docs_dir": "docs", "nav": nav}, self.root)

    def _write(self, relative_path: str, content: str) -> None:
        path = self.docs / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _remove(self, relative_path: str) -> None:
        (self.docs / relative_path).unlink()

    def _count_path(self, value: Any, expected: str) -> int:
        if isinstance(value, str):
            return int(value == expected)
        if isinstance(value, dict):
            return sum(self._count_path(child, expected) for child in value.values())
        if isinstance(value, list):
            return sum(self._count_path(child, expected) for child in value)
        return 0


if __name__ == "__main__":
    unittest.main()
