from __future__ import annotations

import re
import warnings
from xml.etree import ElementTree

from markdown.inlinepatterns import InlineProcessor
from markdown.util import AtomicString

from .index import DocsIndex, Resolution, ResolutionStatus


IMAGE_PATTERN = r"(?<!\\)!\[\[([^\]\n]+)\]\]"
LINK_PATTERN = r"(?<![!\\])\[\[([^\]\n]+)\]\]"


class ObsidianProcessor(InlineProcessor):
    def __init__(self, pattern: str, index: DocsIndex, strict: bool):
        super().__init__(pattern)
        self.index = index
        self.strict = strict

    def _inside_html_tag(self, data: str, start: int) -> bool:
        last_open = data.rfind("<", 0, start)
        last_close = data.rfind(">", 0, start)
        return last_open > last_close

    def _diagnostic(self, resolution: Resolution, label: str, kind: str = "link"):
        status = resolution.status.value
        candidates = ", ".join(resolution.candidates)
        message = f"Obsidian {kind} target {status}: {resolution.target!r}"
        if candidates:
            message += f"; candidates: {candidates}"
        if self.strict:
            raise ValueError(message)

        from . import ObsidianWikiWarning

        warnings.warn(message, ObsidianWikiWarning, stacklevel=4)
        element = ElementTree.Element("span")
        element.set("class", f"obsidian-wiki-link obsidian-wiki-link--{status}")
        element.set("data-target", resolution.target)
        if candidates:
            element.set("data-candidates", ";".join(resolution.candidates))
        element.text = AtomicString(label)
        return element

    def _unsupported(self, target: str, label: str, kind: str):
        resolution = Resolution(ResolutionStatus.INVALID, target)
        element = self._diagnostic(resolution, label, kind)
        element.set(
            "class",
            "obsidian-wiki-link obsidian-wiki-link--unsupported",
        )
        return element


class ObsidianWikiLinkProcessor(ObsidianProcessor):
    def __init__(self, index: DocsIndex, strict: bool):
        super().__init__(LINK_PATTERN, index, strict)

    def handleMatch(self, match, data):
        if self._inside_html_tag(data, match.start(0)):
            return None, match.start(0), match.end(0)
        raw = match.group(1).strip()
        destination, alias = self._split_alias(raw)
        page, heading = self._split_heading(destination)
        label = alias or (heading if not page and heading else PureLabel.page(page))

        if not page or "^" in destination:
            element = self._unsupported(raw, label or raw, "link")
        else:
            resolution = self.index.resolve_page(page, heading)
            if resolution.status is ResolutionStatus.FOUND:
                element = ElementTree.Element("a")
                element.set("class", "obsidian-wiki-link")
                element.set("href", resolution.url)
                element.text = AtomicString(label)
            else:
                element = self._diagnostic(resolution, label, "link")
        return element, match.start(0), match.end(0)

    @staticmethod
    def _split_alias(raw: str):
        destination, separator, alias = raw.partition("|")
        return destination.strip(), alias.strip() if separator else None

    @staticmethod
    def _split_heading(destination: str):
        page, separator, heading = destination.partition("#")
        return page.strip(), heading.strip() if separator else None


class ObsidianImageProcessor(ObsidianProcessor):
    def __init__(
        self,
        index: DocsIndex,
        strict: bool,
        *,
        max_width: int,
        max_height: int,
        center: bool,
        border_radius: str,
    ):
        super().__init__(IMAGE_PATTERN, index, strict)
        self.max_width = max_width
        self.max_height = max_height
        self.center = center
        self.border_radius = border_radius

    def handleMatch(self, match, data):
        if self._inside_html_tag(data, match.start(0)):
            return None, match.start(0), match.end(0)
        raw = match.group(1).strip()
        target, dimensions = self._split_dimensions(raw)
        label = f"Missing image: {target}"
        if dimensions is None or "#" in target or "^" in target:
            element = self._unsupported(raw, f"Unsupported embed: {raw}", "image")
        else:
            resolution = self.index.resolve_image(target)
            if resolution.status is ResolutionStatus.FOUND:
                width, height = dimensions
                classes = ["obsidian-wiki-image"]
                if self.center:
                    classes.append("obsidian-wiki-image--centered")
                style = (
                    f"--obsidian-image-max-width: {width or self.max_width}px; "
                    f"--obsidian-image-max-height: {height or self.max_height}px; "
                    f"--obsidian-image-border-radius: {self.border_radius};"
                )
                element = ElementTree.Element("img")
                element.set("class", " ".join(classes))
                element.set("src", resolution.url)
                element.set("alt", PureLabel.image(target))
                element.set("style", style)
            elif resolution.status is ResolutionStatus.INVALID and not re.search(
                r"\.(?:png|jpe?g|gif|svg|webp|avif)$", target, re.IGNORECASE
            ):
                element = self._unsupported(raw, f"Unsupported embed: {raw}", "image")
            else:
                element = self._diagnostic(resolution, label, "image")
                element.set(
                    "class",
                    f"{element.get('class')} obsidian-wiki-link--image",
                )
        return element, match.start(0), match.end(0)

    @staticmethod
    def _split_dimensions(raw: str) -> tuple[str, tuple[int | None, int | None] | None]:
        target, separator, size = raw.partition("|")
        target = target.strip()
        if not separator:
            return target, (None, None)
        if "|" in size:
            return target, None
        match = re.fullmatch(r"([1-9][0-9]*)(?:[xX]([1-9][0-9]*))?", size.strip())
        if match is None:
            return target, None
        try:
            width = int(match.group(1))
            height = int(match.group(2)) if match.group(2) else None
        except ValueError:
            return target, None
        return target, (width, height)


class PureLabel:
    @staticmethod
    def page(target: str) -> str:
        name = target.replace("\\", "/").rstrip("/").rsplit("/", 1)[-1]
        return name[:-3] if name.casefold().endswith(".md") else name

    @staticmethod
    def image(target: str) -> str:
        return target.replace("\\", "/").rsplit("/", 1)[-1]
