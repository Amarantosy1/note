from __future__ import annotations

import json
import re
from typing import Any
from xml.etree import ElementTree

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


_BOOLEAN_OPTIONS = frozenset({"touch_navigation", "loop", "zoomable", "draggable"})
_BUILT_IN_SKIP_CLASSES = frozenset({"emojione", "twemoji", "gemoji", "off-glb"})
_EFFECTS = frozenset({"zoom", "fade", "none"})
_SLIDE_EFFECTS = frozenset({"slide", "zoom", "fade", "none"})
_CLASS_NAME_PATTERN = re.compile(r"[^\s]+")


class GlightboxTreeprocessor(Treeprocessor):
    def __init__(
        self,
        md,
        *,
        options: dict[str, Any],
        skip_classes: frozenset[str],
    ):
        super().__init__(md)
        self.options = options
        self.serialized_options = json.dumps(options, ensure_ascii=True, separators=(",", ":"))
        self.skip_classes = _BUILT_IN_SKIP_CLASSES | skip_classes

    def run(self, root: ElementTree.Element) -> ElementTree.Element:
        self._wrap_images(root)
        return root

    def _wrap_images(self, parent: ElementTree.Element) -> None:
        for index, child in enumerate(list(parent)):
            if child.tag == "img":
                if parent.tag != "a" and not self._should_skip(child):
                    parent.remove(child)
                    anchor = ElementTree.Element(
                        "a",
                        {
                            "class": "glightbox",
                            "href": child.get("src", ""),
                            "data-type": "image",
                            "data-glightbox-options": self.serialized_options,
                        },
                    )
                    anchor.tail = child.tail
                    child.tail = None
                    anchor.append(child)
                    parent.insert(index, anchor)
                continue
            self._wrap_images(child)

    def _should_skip(self, image: ElementTree.Element) -> bool:
        source = image.get("src", "").strip()
        classes = frozenset(image.get("class", "").split())
        return not source or bool(classes & self.skip_classes)


class GlightboxExtension(Extension):
    config = {
        "touch_navigation": [True, "Enable touch navigation"],
        "loop": [False, "Loop slides after reaching the end"],
        "effect": ["zoom", "Open and close effect: zoom, fade, or none"],
        "slide_effect": ["slide", "Slide effect: slide, zoom, fade, or none"],
        "zoomable": [True, "Allow image zooming"],
        "draggable": [True, "Allow mouse dragging between slides"],
        "skip_classes": [[], "Additional image classes excluded from the lightbox"],
    }

    def __init__(self, **kwargs: Any):
        for name in _BOOLEAN_OPTIONS:
            if name in kwargs and not isinstance(kwargs[name], bool):
                raise ValueError(f"{name} must be a boolean")
        self.config = {
            key: [default.copy() if isinstance(default, list) else default, description]
            for key, (default, description) in type(self).config.items()
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md) -> None:
        touch_navigation = _boolean(self.getConfig("touch_navigation"), "touch_navigation")
        loop = _boolean(self.getConfig("loop"), "loop")
        zoomable = _boolean(self.getConfig("zoomable"), "zoomable")
        draggable = _boolean(self.getConfig("draggable"), "draggable")
        effect = _choice(self.getConfig("effect"), "effect", _EFFECTS)
        slide_effect = _choice(
            self.getConfig("slide_effect"),
            "slide_effect",
            _SLIDE_EFFECTS,
        )
        skip_classes = _class_names(self.getConfig("skip_classes"))
        options = {
            "touchNavigation": touch_navigation,
            "loop": loop,
            "zoomable": zoomable,
            "draggable": draggable,
            "openEffect": effect,
            "closeEffect": effect,
            "slideEffect": slide_effect,
        }
        md.registerExtension(self)
        md.treeprocessors.register(
            GlightboxTreeprocessor(
                md,
                options=options,
                skip_classes=skip_classes,
            ),
            "zensical_glightbox",
            5,
        )


def _boolean(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be a boolean")
    return value


def _choice(value: Any, name: str, allowed: frozenset[str]) -> str:
    if not isinstance(value, str) or value not in allowed:
        choices = ", ".join(sorted(allowed))
        raise ValueError(f"{name} must be one of: {choices}")
    return value


def _class_names(value: Any) -> frozenset[str]:
    if not isinstance(value, list):
        raise ValueError("skip_classes must be a list of CSS class names")
    result: set[str] = set()
    for item in value:
        if not isinstance(item, str) or not _CLASS_NAME_PATTERN.fullmatch(item):
            raise ValueError("skip_classes must contain non-empty CSS class names without whitespace")
        result.add(item)
    return frozenset(result)


def makeExtension(**kwargs: Any) -> GlightboxExtension:
    return GlightboxExtension(**kwargs)


__all__ = ["GlightboxExtension", "GlightboxTreeprocessor", "makeExtension"]
