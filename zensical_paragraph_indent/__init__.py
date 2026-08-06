from __future__ import annotations

import re
from typing import Any
from xml.etree import ElementTree

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


_DEFAULT_SKIP_ANCESTOR_TAGS = frozenset(
    {"blockquote", "code", "details", "li", "pre", "td", "th"}
)


class ParagraphIndentTreeprocessor(Treeprocessor):
    """Mark body paragraphs for CSS-based first-line indentation."""

    def __init__(
        self,
        md,
        *,
        class_name: str,
        skip_classes: frozenset[str],
    ):
        super().__init__(md)
        self.class_name = class_name
        self.skip_classes = skip_classes

    def run(self, root: ElementTree.Element) -> ElementTree.Element:
        self._visit(root, ())
        return root

    def _visit(
        self,
        element: ElementTree.Element,
        ancestors: tuple[ElementTree.Element, ...],
    ) -> None:
        if element.tag == "p" and self._should_indent(element, ancestors):
            classes = element.get("class", "").split()
            if self.class_name not in classes:
                classes.append(self.class_name)
                element.set("class", " ".join(classes))
            _indent_hardbreak_lines(element)

        next_ancestors = ancestors + (element,)
        for child in element:
            self._visit(child, next_ancestors)

    def _should_indent(
        self,
        paragraph: ElementTree.Element,
        ancestors: tuple[ElementTree.Element, ...],
    ) -> bool:
        if self._has_skipped_ancestor(ancestors):
            return False
        if _contains_code_placeholder(paragraph):
            return False
        if any(child.tag == "pre" for child in paragraph.iter()):
            return False
        return _contains_visible_text(paragraph)

    def _has_skipped_ancestor(
        self,
        ancestors: tuple[ElementTree.Element, ...],
    ) -> bool:
        for ancestor in ancestors:
            if ancestor.tag in _DEFAULT_SKIP_ANCESTOR_TAGS:
                return True
            classes = set(ancestor.get("class", "").split())
            if classes & self.skip_classes or "admonition" in classes:
                return True
        return False


class ParagraphIndentExtension(Extension):
    config = {
        "class_name": [
            "zensical-paragraph-indent",
            "CSS class added to body paragraphs",
        ],
        "skip_classes": [
            [],
            "Ancestor classes whose paragraphs should not be indented",
        ],
    }

    def __init__(self, **kwargs: Any):
        self.config = {
            key: [default.copy() if isinstance(default, list) else default, description]
            for key, (default, description) in type(self).config.items()
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md) -> None:
        class_name = _class_name(self.getConfig("class_name"))
        skip_classes = _class_names(self.getConfig("skip_classes"))
        md.registerExtension(self)
        md.treeprocessors.register(
            ParagraphIndentTreeprocessor(
                md,
                class_name=class_name,
                skip_classes=skip_classes,
            ),
            "zensical_paragraph_indent",
            -100,
        )


def _indent_hardbreak_lines(paragraph: ElementTree.Element) -> None:
    """Add a leading indent to text following hardbreak elements."""
    for element in paragraph.iter():
        if element.tag == "br" and element.tail:
            element.tail = _indent_text(element.tail)


def _indent_text(value: str) -> str:
    leading = value[: len(value) - len(value.lstrip("\n"))]
    if not leading:
        return value
    return leading + "  " + value[len(leading) :]


def _contains_visible_text(element: ElementTree.Element) -> bool:
    """Return whether an element contains text, excluding image-only content."""
    if _is_visible_text(element.text):
        return True

    for child in element:
        if child.tag not in {"img", "br"} and _contains_visible_text(child):
            return True
        if _is_visible_text(child.tail):
            return True
    return False


def _contains_code_placeholder(element: ElementTree.Element) -> bool:
    return any(
        _CODE_PLACEHOLDER_PATTERN.search(value)
        for value in _text_values(element)
    )


def _text_values(element: ElementTree.Element):
    if element.text:
        yield element.text
    for child in element:
        yield from _text_values(child)
        if child.tail:
            yield child.tail


_CODE_PLACEHOLDER_PATTERN = re.compile(r"[\x02\x03]")


def _is_visible_text(value: str | None) -> bool:
    return bool(value and value.strip())


def _class_name(value: Any) -> str:
    if not isinstance(value, str) or not value.strip() or any(
        character.isspace() for character in value
    ):
        raise ValueError("class_name must be one non-empty CSS class name")
    return value


def _class_names(value: Any) -> frozenset[str]:
    if not isinstance(value, list):
        raise ValueError("skip_classes must be a list of CSS class names")
    result: set[str] = set()
    for item in value:
        if not isinstance(item, str) or not item.strip() or any(
            character.isspace() for character in item
        ):
            raise ValueError(
                "skip_classes must contain non-empty CSS class names without whitespace"
            )
        result.add(item)
    return frozenset(result)


def makeExtension(**kwargs: Any) -> ParagraphIndentExtension:
    return ParagraphIndentExtension(**kwargs)


__all__ = [
    "ParagraphIndentExtension",
    "ParagraphIndentTreeprocessor",
    "makeExtension",
]
