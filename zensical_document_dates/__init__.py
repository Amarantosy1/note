from __future__ import annotations

import fnmatch
import xml.etree.ElementTree as etree
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

from .dates import DocumentDates, normalize_page_path, resolve_document_dates

if TYPE_CHECKING:
    from markdown import Markdown


_ICON_PATHS = {
    "created": (
        "M13 14H11V8H13V14M15 1H9V3H15V1M5 13C5 9.13 8.13 6 12 6C15.29 6 "
        "18.05 8.28 18.79 11.34L19.39 10.74C19.71 10.42 20.1 10.21 20.5 "
        "10.1C20.18 9.11 19.67 8.19 19.03 7.39L20.45 5.97C20 5.46 19.55 5 "
        "19.04 4.56L17.62 6C16.07 4.74 14.12 4 12 4C7.03 4 3 8.03 3 13C3 "
        "17.63 6.5 21.44 11 21.94V19.92C7.61 19.43 5 16.53 5 13M13 "
        "19.96V22H15.04L21.17 15.88L19.13 13.83L13 19.96M22.85 13.47L21.53 "
        "12.15C21.33 11.95 21 11.95 20.81 12.15L19.83 13.13L21.87 15.17L22.85 "
        "14.19C23.05 14 23.05 13.67 22.85 13.47Z"
    ),
    "updated": (
        "M11 8H13V14H11V8M15 1H9V3H15V1M12 20C8.13 20 5 16.87 5 13S8.13 6 "
        "12 6 19 9.13 19 13C19.7 13 20.36 13.13 21 13.35C21 13.23 21 13.12 21 "
        "13C21 10.88 20.26 8.93 19.03 7.39L20.45 5.97C20 5.46 19.55 5 19.04 "
        "4.56L17.62 6C16.07 4.74 14.12 4 12 4C7.03 4 3 8.03 3 13S7.03 22 "
        "12 22C12.59 22 13.16 21.94 13.71 21.83C13.4 21.25 13.18 20.6 13.08 "
        "19.91C12.72 19.96 12.37 20 12 20M20 18V15H18V18H15V20H18V23H20V20H23V18H20Z"
    ),
}


class DocumentDatesTreeprocessor(Treeprocessor):
    def __init__(
        self,
        md: Markdown,
        *,
        docs_dir: str,
        date_format: str,
        tooltip_format: str,
        created_label: str,
        updated_label: str,
        exclude: list[str],
        show_created: bool,
        show_updated: bool,
    ):
        super().__init__(md)
        self.docs_dir = Path(docs_dir)
        self.date_format = date_format
        self.tooltip_format = tooltip_format
        self.created_label = created_label
        self.updated_label = updated_label
        self.exclude = tuple(exclude)
        self.show_created = show_created
        self.show_updated = show_updated

    def run(self, root: etree.Element) -> etree.Element:
        context = _zensical_context(self.md)
        if context is None:
            return root

        docs_dir = self.docs_dir
        if not docs_dir.is_absolute():
            root_dir = context.config.get("root_dir")
            if root_dir:
                docs_dir = Path(root_dir) / docs_dir
        docs_dir = docs_dir.resolve()

        relative_path = normalize_page_path(context.page.path, docs_dir)
        if relative_path is None or any(
            fnmatch.fnmatchcase(relative_path, pattern) for pattern in self.exclude
        ):
            return root

        meta = context.page.meta
        show_created = self.show_created and meta.get("show_created") is not False
        show_updated = self.show_updated and meta.get("show_updated") is not False
        if not show_created and not show_updated:
            return root

        dates = resolve_document_dates(docs_dir, relative_path, meta)
        if dates is None:
            return root

        information = self._build_information(dates, show_created, show_updated)
        children = list(root)
        for index, child in enumerate(children):
            if child.tag == "h1":
                root.insert(index + 1, information)
                break
        else:
            root.insert(0, information)
        return root

    def _build_information(
        self,
        dates: DocumentDates,
        show_created: bool,
        show_updated: bool,
    ) -> etree.Element:
        information = etree.Element(
            "div",
            {
                "class": "document-dates",
                "aria-label": "文档日期",
            },
        )
        if show_created:
            self._add_date(information, "created", self.created_label, dates.created)
        if show_updated:
            self._add_date(information, "updated", self.updated_label, dates.updated)
        return information

    def _add_date(
        self,
        parent: etree.Element,
        kind: str,
        label: str,
        value: datetime,
    ) -> None:
        tooltip = f"{label} {value.strftime(self.tooltip_format)}"
        item = etree.SubElement(
            parent,
            "span",
            {
                "class": f"document-dates__item document-dates__item--{kind}",
                "tabindex": "0",
                "aria-label": tooltip,
                "data-tooltip": tooltip,
            },
        )
        icon = etree.SubElement(
            item,
            "svg",
            {
                "class": "document-dates__icon",
                "viewBox": "0 0 24 24",
                "aria-hidden": "true",
                "focusable": "false",
            },
        )
        etree.SubElement(icon, "path", {"d": _ICON_PATHS[kind]})
        time_element = etree.SubElement(
            item,
            "time",
            {
                "datetime": value.isoformat(),
                "class": "document-dates__time",
            },
        )
        time_element.text = value.strftime(self.date_format)


class DocumentDatesExtension(Extension):
    config = {
        "docs_dir": ["docs", "Directory containing Markdown documents"],
        "date_format": ["%Y-%m-%d", "strftime format used for visible dates"],
        "tooltip_format": [
            "%Y-%m-%d %H:%M:%S %Z",
            "strftime format used for detailed date tooltips",
        ],
        "created_label": ["Created", "Accessible label for the creation date"],
        "updated_label": ["Modified", "Accessible label for the modification date"],
        "exclude": [[], "Document paths excluded from date rendering"],
        "show_created": [True, "Show document creation dates"],
        "show_updated": [True, "Show document update dates"],
    }

    def __init__(self, **kwargs: Any):
        self.config = {
            key: [default.copy() if isinstance(default, (dict, list)) else default, description]
            for key, (default, description) in type(self).config.items()
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        processor = DocumentDatesTreeprocessor(
            md,
            docs_dir=self.getConfig("docs_dir"),
            date_format=self.getConfig("date_format"),
            tooltip_format=self.getConfig("tooltip_format"),
            created_label=self.getConfig("created_label"),
            updated_label=self.getConfig("updated_label"),
            exclude=self.getConfig("exclude"),
            show_created=self.getConfig("show_created"),
            show_updated=self.getConfig("show_updated"),
        )
        md.treeprocessors.register(processor, "zensical_document_dates", 1)


def _zensical_context(md: Markdown) -> Any | None:
    try:
        from zensical.extensions.context import ContextPreprocessor
    except ImportError:
        return None
    return ContextPreprocessor.from_markdown(md)


def makeExtension(**kwargs: Any) -> DocumentDatesExtension:
    return DocumentDatesExtension(**kwargs)


__all__ = [
    "DocumentDatesExtension",
    "DocumentDatesTreeprocessor",
    "makeExtension",
]
