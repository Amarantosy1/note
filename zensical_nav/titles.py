import re
from pathlib import Path

from ruamel.yaml import YAML


_H1 = re.compile(r"^\s{0,3}#\s+(.+?)\s*#*\s*$")
_INLINE_CODE = re.compile(r"`([^`]*)`")


def page_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig")
    frontmatter_title = _frontmatter_title(text)
    if frontmatter_title:
        return frontmatter_title

    in_fence = False
    fence = ""
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = stripped[:3]
        if marker in ("```", "~~~"):
            if not in_fence:
                in_fence = True
                fence = marker
            elif marker == fence:
                in_fence = False
            continue
        if in_fence:
            continue
        match = _H1.match(line)
        if match:
            title = _INLINE_CODE.sub(r"\1", match.group(1)).strip()
            if title:
                return title

    return path.stem.replace("-", " ").replace("_", " ").strip()


def _frontmatter_title(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return None

    yaml = YAML(typ="safe")
    try:
        metadata = yaml.load("\n".join(lines[1:end]))
    except Exception:
        return None
    if not isinstance(metadata, dict):
        return None
    title = metadata.get("title")
    return title.strip() if isinstance(title, str) and title.strip() else None
