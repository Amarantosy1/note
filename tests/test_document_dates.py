from __future__ import annotations

import os
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from markdown import Markdown
from zensical.extensions.context import ContextExtension, Page

from zensical_document_dates import DocumentDatesExtension
from zensical_document_dates.dates import (
    GitDates,
    load_git_dates,
    normalize_page_path,
    parse_datetime,
    parse_git_log,
    resolve_document_dates,
)


class DocumentDateResolutionTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.docs = Path(self.temporary_directory.name)
        self.source = self.docs / "notes" / "article.md"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("# Article", encoding="utf-8")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_front_matter_dates_override_git(self):
        git_dates = GitDates(
            created={"notes/article.md": datetime(2020, 1, 1, tzinfo=timezone.utc)},
            updated={"notes/article.md": datetime(2021, 1, 1, tzinfo=timezone.utc)},
        )
        meta = {
            "created": date(2026, 4, 13),
            "modified": "2026-07-29T14:30:00+08:00",
        }

        with patch("zensical_document_dates.dates.load_git_dates", return_value=git_dates):
            dates = resolve_document_dates(self.docs, "notes/article.md", meta)

        self.assertIsNotNone(dates)
        self.assertEqual(dates.created.date().isoformat(), "2026-04-13")
        self.assertEqual(dates.updated.isoformat(), "2026-07-29T14:30:00+08:00")

    def test_nested_front_matter_and_scalar_date_are_supported(self):
        empty_git = GitDates(created={}, updated={})
        with patch("zensical_document_dates.dates.load_git_dates", return_value=empty_git):
            nested = resolve_document_dates(
                self.docs,
                "notes/article.md",
                {"date": {"created": "2026-05-13", "updated": "2026-06-14"}},
            )
            scalar = resolve_document_dates(
                self.docs,
                "notes/article.md",
                {"date": "2026-05-13"},
            )

        self.assertEqual(nested.created.date().isoformat(), "2026-05-13")
        self.assertEqual(nested.updated.date().isoformat(), "2026-06-14")
        self.assertEqual(scalar.created.date().isoformat(), "2026-05-13")

    def test_git_creation_date_precedes_file_system_creation_date(self):
        git_created = datetime(2022, 2, 2, tzinfo=timezone.utc)
        file_created = datetime(2020, 1, 1, tzinfo=timezone.utc)
        git_updated = datetime(2025, 5, 5, tzinfo=timezone.utc)
        git_dates = GitDates(
            created={"notes/article.md": git_created},
            updated={"notes/article.md": git_updated},
        )

        with patch("zensical_document_dates.dates.load_git_dates", return_value=git_dates), patch(
            "zensical_document_dates.dates._file_created_at",
            return_value=file_created,
        ):
            dates = resolve_document_dates(self.docs, "notes/article.md", {})

        self.assertEqual(dates.created, git_created)
        self.assertEqual(dates.updated, git_updated)

    def test_file_system_creation_date_is_used_when_git_date_is_unavailable(self):
        file_created = datetime(2020, 1, 1, tzinfo=timezone.utc)
        git_dates = GitDates(created={}, updated={})

        with patch("zensical_document_dates.dates.load_git_dates", return_value=git_dates), patch(
            "zensical_document_dates.dates._file_created_at",
            return_value=file_created,
        ):
            dates = resolve_document_dates(self.docs, "notes/article.md", {})

        self.assertEqual(dates.created, file_created)

    def test_file_system_fallback_uses_modification_time(self):
        timestamp = 1_700_000_000
        os.utime(self.source, (timestamp, timestamp))
        with patch(
            "zensical_document_dates.dates.load_git_dates",
            return_value=GitDates(created={}, updated={}),
        ), patch(
            "zensical_document_dates.dates._file_created_at",
            return_value=datetime(2020, 1, 1, tzinfo=timezone.utc),
        ):
            dates = resolve_document_dates(self.docs, "notes/article.md", {})

        self.assertEqual(dates.created.isoformat(), "2020-01-01T00:00:00+00:00")
        self.assertEqual(int(dates.updated.timestamp()), timestamp)

    def test_invalid_front_matter_falls_back_to_git(self):
        created = datetime(2022, 2, 2, tzinfo=timezone.utc)
        git_dates = GitDates(created={"notes/article.md": created}, updated={})
        with patch("zensical_document_dates.dates.load_git_dates", return_value=git_dates), patch(
            "zensical_document_dates.dates._file_created_at",
            return_value=None,
        ):
            dates = resolve_document_dates(
                self.docs,
                "notes/article.md",
                {"created": "not-a-date"},
            )

        self.assertEqual(dates.created, created)

    def test_normalize_page_path_rejects_traversal(self):
        project_docs = self.docs / "docs"
        project_docs.mkdir()
        self.assertEqual(
            normalize_page_path("docs/notes/article.md", project_docs),
            "notes/article.md",
        )
        self.assertIsNone(normalize_page_path("../secret.md", project_docs))

    def test_parse_datetime_supports_z_and_rejects_other_types(self):
        self.assertEqual(
            parse_datetime("2026-07-29T12:00:00Z").isoformat(),
            "2026-07-29T12:00:00+00:00",
        )
        self.assertIsNone(parse_datetime(1_700_000_000))

    def test_parse_git_log_collects_first_and_latest_commit(self):
        output = """@@ZENSICAL_DOCUMENT_DATE@@2026-07-29T10:00:00+00:00
notes/article.md

@@ZENSICAL_DOCUMENT_DATE@@2026-04-13T08:00:00+00:00
notes/article.md
other.txt
"""
        dates = parse_git_log(output)

        self.assertEqual(
            dates.updated["notes/article.md"].isoformat(),
            "2026-07-29T10:00:00+00:00",
        )
        self.assertEqual(
            dates.created["notes/article.md"].isoformat(),
            "2026-04-13T08:00:00+00:00",
        )
        self.assertNotIn("other.txt", dates.created)

    def test_git_unavailable_returns_empty_dates(self):
        load_git_dates.cache_clear()
        with patch("zensical_document_dates.dates.subprocess.run", side_effect=OSError):
            dates = load_git_dates(str(self.docs))
        load_git_dates.cache_clear()

        self.assertEqual(dates, GitDates(created={}, updated={}))


class DocumentDatesExtensionTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.docs = Path(self.temporary_directory.name)
        self.source = self.docs / "article.md"
        self.source.write_text("# Article", encoding="utf-8")
        self.fixed_dates = SimpleNamespace(
            created=datetime(2026, 4, 13, tzinfo=timezone.utc),
            updated=datetime(2026, 7, 29, 14, 30, tzinfo=timezone.utc),
        )

    def tearDown(self):
        self.temporary_directory.cleanup()

    def render(
        self,
        source: str,
        *,
        path: str = "article.md",
        meta: dict | None = None,
        exclude: list[str] | None = None,
    ) -> str:
        page = Page(url="article/", path=path, meta=meta or {})
        config = {"docs_dir": str(self.docs)}
        md = Markdown(
            extensions=[
                ContextExtension(page=page, config=config),
                DocumentDatesExtension(
                    docs_dir=str(self.docs),
                    date_format="%Y-%m-%d",
                    tooltip_format="%Y-%m-%d %H:%M:%S %Z",
                    created_label="创建于",
                    updated_label="修改于",
                    exclude=exclude or [],
                ),
            ]
        )
        with patch(
            "zensical_document_dates.resolve_document_dates",
            return_value=self.fixed_dates,
        ):
            return md.convert(source)

    def test_inserts_dates_after_explicit_h1(self):
        html = self.render("# 标题\n\n正文")

        self.assertLess(html.index("<h1>"), html.index('class="document-dates"'))
        self.assertLess(html.index('class="document-dates"'), html.index("<p>正文</p>"))
        self.assertIn('datetime="2026-04-13T00:00:00+00:00"', html)
        self.assertIn('data-tooltip="创建于 2026-04-13 00:00:00 UTC"', html)
        self.assertIn('data-tooltip="修改于 2026-07-29 14:30:00 UTC"', html)
        self.assertEqual(html.count('class="document-dates__icon"'), 2)
        self.assertEqual(html.count('viewBox="0 0 24 24"'), 2)
        self.assertEqual(html.count('aria-hidden="true"'), 2)
        self.assertEqual(html.count('tabindex="0"'), 2)
        self.assertNotIn('class="document-dates__label"', html)

    def test_prepends_dates_when_theme_will_generate_title(self):
        html = self.render("## 小节\n\n正文")

        self.assertTrue(html.startswith('<div aria-label="文档日期" class="document-dates">'))
        self.assertLess(html.index('class="document-dates"'), html.index("<h2>小节</h2>"))

    def test_exclude_pattern_skips_document(self):
        html = self.render("# 首页", path="index.md", exclude=["index.md"])
        self.assertNotIn("document-dates", html)

    def test_page_level_switches_hide_individual_dates(self):
        html = self.render("# 标题", meta={"show_created": False})
        self.assertNotIn("document-dates__item--created", html)
        self.assertIn("document-dates__item--updated", html)
        self.assertIn("修改于", html)

    def test_both_page_level_switches_skip_resolution(self):
        page = Page(
            url="article/",
            path="article.md",
            meta={"show_created": False, "show_updated": False},
        )
        md = Markdown(
            extensions=[
                ContextExtension(page=page, config={"docs_dir": str(self.docs)}),
                DocumentDatesExtension(docs_dir=str(self.docs)),
            ]
        )
        with patch("zensical_document_dates.resolve_document_dates") as resolve:
            html = md.convert("# 标题")

        resolve.assert_not_called()
        self.assertNotIn("document-dates", html)

    def test_labels_are_html_escaped(self):
        page = Page(url="article/", path="article.md", meta={})
        md = Markdown(
            extensions=[
                ContextExtension(page=page, config={"docs_dir": str(self.docs)}),
                DocumentDatesExtension(
                    docs_dir=str(self.docs),
                    created_label='<script>alert("x")</script>',
                    show_updated=False,
                ),
            ]
        )
        with patch(
            "zensical_document_dates.resolve_document_dates",
            return_value=self.fixed_dates,
        ):
            html = md.convert("# 标题")

        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("aria-label=", html)
        self.assertIn("data-tooltip=", html)

    def test_extension_instances_do_not_share_configuration(self):
        first = DocumentDatesExtension(show_updated=False, exclude=["first.md"])
        second = DocumentDatesExtension()

        self.assertFalse(first.getConfig("show_updated"))
        self.assertEqual(first.getConfig("exclude"), ["first.md"])
        self.assertTrue(second.getConfig("show_updated"))
        self.assertEqual(second.getConfig("exclude"), [])

    def test_relative_docs_dir_uses_zensical_project_root(self):
        project = self.docs / "project"
        project_docs = project / "docs"
        project_docs.mkdir(parents=True)
        (project_docs / "article.md").write_text("# Article", encoding="utf-8")
        page = Page(url="article/", path="article.md", meta={})
        md = Markdown(
            extensions=[
                ContextExtension(page=page, config={"root_dir": str(project)}),
                DocumentDatesExtension(docs_dir="docs"),
            ]
        )
        with patch(
            "zensical_document_dates.resolve_document_dates",
            return_value=self.fixed_dates,
        ) as resolve:
            md.convert("# 标题")

        self.assertEqual(resolve.call_args.args[0], project_docs.resolve())


if __name__ == "__main__":
    unittest.main()
