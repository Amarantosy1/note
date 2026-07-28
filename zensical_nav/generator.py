from collections.abc import Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any

from .config import NavConfigError, NavOptions, parse_auto, parse_defaults, resolve_auto_directory
from .titles import page_title


def expand_nav(config: Mapping[str, Any], config_dir: Path | str = ".") -> list[Any]:
    nav = config.get("nav")
    if not isinstance(nav, list):
        raise NavConfigError("nav must be a list")

    project_dir = Path(config_dir).resolve()
    docs_setting = config.get("docs_dir", "docs")
    if not isinstance(docs_setting, str) or not docs_setting:
        raise NavConfigError("docs_dir must be a non-empty string")
    docs_dir = (project_dir / docs_setting).resolve()
    if not docs_dir.is_dir():
        raise NavConfigError(f"docs_dir does not exist or is not a directory: {docs_setting}")

    defaults = parse_defaults(config.get("zensical_nav"))
    manual_paths = _manual_page_paths(nav)
    return _expand_items(nav, docs_dir, defaults, manual_paths, "nav")


def _expand_items(
    items: Sequence[Any],
    docs_dir: Path,
    defaults: NavOptions,
    manual_paths: set[str],
    location: str,
) -> list[Any]:
    expanded: list[Any] = []
    for index, item in enumerate(items):
        item_location = f"{location}[{index}]"
        if isinstance(item, Mapping) and set(item) == {"auto"}:
            relative_path, options = parse_auto(item["auto"], defaults, f"{item_location}.auto")
            expanded.extend(_generate(relative_path, docs_dir, options, manual_paths, item_location))
            continue
        if isinstance(item, Mapping) and len(item) == 1:
            title, value = next(iter(item.items()))
            if isinstance(value, list):
                expanded.append(
                    {title: _expand_items(value, docs_dir, defaults, manual_paths, f"{item_location}.{title}")}
                )
                continue
        expanded.append(item)
    return expanded


def _generate(
    relative_path: PurePosixPath,
    docs_dir: Path,
    options: NavOptions,
    manual_paths: set[str],
    location: str,
) -> list[Any]:
    directory = resolve_auto_directory(docs_dir, relative_path, f"{location}.auto")
    generated = _directory_items(directory, docs_dir, options, manual_paths)
    if not generated and not options.allow_empty:
        raise NavConfigError(f"{location}.auto generated no pages; set allow_empty: true to permit this")
    return generated


def _directory_items(
    directory: Path,
    docs_dir: Path,
    options: NavOptions,
    manual_paths: set[str],
) -> list[Any]:
    pages = sorted(
        (
            path
            for path in directory.iterdir()
            if not path.is_symlink() and path.is_file() and path.suffix.casefold() == ".md"
        ),
        key=_sort_key,
    )
    index_pages = [path for path in pages if path.stem.casefold() == "index"]
    regular_pages = [path for path in pages if path.stem.casefold() != "index"]

    result: list[Any] = []
    if options.include_index:
        result.extend(_page_entry(path, docs_dir, manual_paths) for path in index_pages)
    result.extend(_page_entry(path, docs_dir, manual_paths) for path in regular_pages)
    result = [item for item in result if item is not None]

    if options.recursive:
        directories = sorted(
            (path for path in directory.iterdir() if not path.is_symlink() and path.is_dir()),
            key=_sort_key,
        )
        for child in directories:
            children = _directory_items(child, docs_dir, options, manual_paths)
            if children:
                result.append({child.name: children})
    return result


def _page_entry(path: Path, docs_dir: Path, manual_paths: set[str]) -> dict[str, str] | None:
    relative = path.relative_to(docs_dir).as_posix()
    if relative in manual_paths:
        return None
    title = page_title(path) if path.stem.casefold() == "index" else path.stem
    return {title: relative}


def _manual_page_paths(nav: Sequence[Any]) -> set[str]:
    paths: set[str] = set()

    def visit(value: Any) -> None:
        if isinstance(value, str):
            if value.casefold().endswith(".md"):
                paths.add(PurePosixPath(value).as_posix())
            return
        if isinstance(value, Mapping):
            if set(value) == {"auto"}:
                return
            for child in value.values():
                visit(child)
            return
        if isinstance(value, list):
            for child in value:
                visit(child)

    visit(nav)
    return paths


def _sort_key(path: Path) -> tuple[str, str]:
    return path.name.casefold(), path.name
