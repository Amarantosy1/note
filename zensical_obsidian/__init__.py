from __future__ import annotations

import re
from typing import Any

from .index import DocsIndex, Resolution, ResolutionStatus
from .processors import ObsidianImageProcessor, ObsidianWikiLinkProcessor

from markdown.extensions import Extension


class ObsidianWikiWarning(UserWarning):
    pass


_CSS_LENGTH_PATTERN = re.compile(r"(?:0|(?:\d+(?:\.\d+)?|\.\d+)(?:px|rem|em|%))")


class ObsidianWikiExtension(Extension):
    config = {
        "docs_dir": ["docs", "Directory containing Markdown pages and assets"],
        "base_url": ["/", "Site URL path prefix"],
        "strict": [False, "Raise an error for unresolved or unsupported targets"],
        "image_max_width": [800, "Default maximum image width in pixels"],
        "image_max_height": [600, "Default maximum image height in pixels"],
        "image_center": [True, "Center images by default"],
        "image_border_radius": ["0.5rem", "Default image border radius"],
    }

    def __init__(self, **kwargs: Any):
        self.config = {
            key: [default, description]
            for key, (default, description) in type(self).config.items()
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        index = DocsIndex(
            docs_dir=self.getConfig("docs_dir"),
            base_url=self.getConfig("base_url"),
        )
        strict = self.getConfig("strict")
        image_max_width = _positive_integer(self.getConfig("image_max_width"), "image_max_width")
        image_max_height = _positive_integer(
            self.getConfig("image_max_height"),
            "image_max_height",
        )
        image_center = self.getConfig("image_center")
        if not isinstance(image_center, bool):
            raise ValueError("image_center must be a boolean")
        image_border_radius = _css_length(
            self.getConfig("image_border_radius"),
            "image_border_radius",
        )
        md.inlinePatterns.register(
            ObsidianImageProcessor(
                index,
                strict,
                max_width=image_max_width,
                max_height=image_max_height,
                center=image_center,
                border_radius=image_border_radius,
            ),
            "zensical_obsidian_image",
            175,
        )
        md.inlinePatterns.register(
            ObsidianWikiLinkProcessor(index, strict),
            "zensical_obsidian_link",
            174,
        )


def _positive_integer(value: Any, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a positive integer")
    if isinstance(value, int):
        result = value
    elif isinstance(value, str) and value.isascii() and value.isdecimal():
        try:
            result = int(value)
        except ValueError as error:
            raise ValueError(f"{name} must be a positive integer") from error
    else:
        raise ValueError(f"{name} must be a positive integer")
    if result <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return result


def _css_length(value: Any, name: str) -> str:
    if value == 0 and not isinstance(value, bool):
        return "0"
    if not isinstance(value, str) or not _CSS_LENGTH_PATTERN.fullmatch(value.strip()):
        raise ValueError(f"{name} must be a non-negative CSS length using px, rem, em, or %")
    return value.strip()


def makeExtension(**kwargs):
    return ObsidianWikiExtension(**kwargs)


__all__ = [
    "DocsIndex",
    "ObsidianWikiExtension",
    "ObsidianWikiWarning",
    "Resolution",
    "ResolutionStatus",
    "makeExtension",
]
