from dataclasses import dataclass, replace
from pathlib import Path, PurePosixPath
from typing import Any, Mapping


class NavConfigError(ValueError):
    pass


@dataclass(frozen=True)
class NavOptions:
    recursive: bool = True
    include_index: bool = True
    allow_empty: bool = False


_ALLOWED_DEFAULTS = {"recursive", "include_index", "allow_empty"}
_ALLOWED_AUTO = {"path", *_ALLOWED_DEFAULTS}


def parse_defaults(value: Any) -> NavOptions:
    if value is None:
        return NavOptions()
    if not isinstance(value, Mapping):
        raise NavConfigError("zensical_nav must be a mapping")
    _reject_unknown(value, _ALLOWED_DEFAULTS, "zensical_nav")
    return _apply_options(NavOptions(), value, "zensical_nav")


def parse_auto(value: Any, defaults: NavOptions, location: str) -> tuple[PurePosixPath, NavOptions]:
    if isinstance(value, str):
        raw_path = value
        options = defaults
    elif isinstance(value, Mapping):
        _reject_unknown(value, _ALLOWED_AUTO, location)
        if "path" not in value:
            raise NavConfigError(f"{location}.path is required")
        raw_path = value["path"]
        options = _apply_options(defaults, value, location)
    else:
        raise NavConfigError(f"{location} must be a path string or mapping")

    if not isinstance(raw_path, str) or not raw_path.strip():
        raise NavConfigError(f"{location}.path must be a non-empty string")
    if "\\" in raw_path or "\x00" in raw_path:
        raise NavConfigError(f"{location}.path contains an invalid character")

    path = PurePosixPath(raw_path)
    if path.is_absolute() or ".." in path.parts:
        raise NavConfigError(f"{location}.path must stay inside docs_dir")
    normalized = PurePosixPath(*(part for part in path.parts if part not in ("", ".")))
    if not normalized.parts:
        raise NavConfigError(f"{location}.path must identify a directory")
    return normalized, options


def resolve_auto_directory(docs_dir: Path, relative_path: PurePosixPath, location: str) -> Path:
    root = docs_dir.resolve()
    target = root.joinpath(*relative_path.parts).resolve()
    try:
        target.relative_to(root)
    except ValueError as error:
        raise NavConfigError(f"{location}.path must stay inside docs_dir") from error
    if not target.is_dir():
        raise NavConfigError(f"{location}.path does not exist or is not a directory: {relative_path}")
    return target


def _apply_options(base: NavOptions, values: Mapping[str, Any], location: str) -> NavOptions:
    updates = {}
    for key in _ALLOWED_DEFAULTS:
        if key not in values:
            continue
        value = values[key]
        if not isinstance(value, bool):
            raise NavConfigError(f"{location}.{key} must be a boolean")
        updates[key] = value
    return replace(base, **updates)


def _reject_unknown(values: Mapping[str, Any], allowed: set[str], location: str) -> None:
    unknown = sorted(str(key) for key in values if key not in allowed)
    if unknown:
        raise NavConfigError(f"{location} contains unknown option(s): {', '.join(unknown)}")
