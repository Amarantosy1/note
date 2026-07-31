from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any


@dataclass(frozen=True)
class DocumentDates:
    created: datetime
    updated: datetime


@dataclass(frozen=True)
class GitDates:
    created: dict[str, datetime]
    updated: dict[str, datetime]


def resolve_document_dates(
    docs_dir: str | Path,
    page_path: str,
    meta: dict[str, Any],
) -> DocumentDates | None:
    root = Path(docs_dir).resolve()
    relative_path = normalize_page_path(page_path, root)
    if relative_path is None:
        return None

    source = root.joinpath(*PurePosixPath(relative_path).parts)
    try:
        source.resolve().relative_to(root)
        stat = source.stat()
    except (OSError, ValueError):
        return None

    git_dates = load_git_dates(str(root))
    created = _meta_date(meta, ("created",), nested=("created",))
    if created is None:
        created = git_dates.created.get(relative_path)
    if created is None:
        created = _file_created_at(stat)

    updated = _meta_date(meta, ("updated", "modified"), nested=("updated", "modified"))
    if updated is None:
        updated = git_dates.updated.get(relative_path)
    if updated is None:
        updated = _timestamp_to_datetime(stat.st_mtime)

    return DocumentDates(created=created, updated=updated)


def normalize_page_path(page_path: str, docs_dir: Path) -> str | None:
    candidate = Path(page_path)
    if candidate.is_absolute():
        try:
            candidate = candidate.resolve().relative_to(docs_dir)
        except ValueError:
            return None

    parts = list(PurePosixPath(candidate.as_posix()).parts)
    while parts and parts[0] in ("", "."):
        parts.pop(0)
    if parts and parts[0] == docs_dir.name:
        parts.pop(0)
    if not parts or ".." in parts:
        return None
    return PurePosixPath(*parts).as_posix()


@lru_cache(maxsize=None)
def load_git_dates(docs_dir: str) -> GitDates:
    root = Path(docs_dir).resolve()
    try:
        repository = Path(
            subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            ).stdout.strip()
        ).resolve()
        relative_docs = root.relative_to(repository).as_posix()
        result = subprocess.run(
            [
                "git",
                "-c",
                "core.quotepath=false",
                "log",
                "--no-merges",
                "--format=@@ZENSICAL_DOCUMENT_DATE@@%aI",
                "--name-only",
                f"--relative={relative_docs}",
                "--",
                relative_docs,
            ],
            cwd=repository,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except (OSError, subprocess.CalledProcessError, ValueError):
        return GitDates(created={}, updated={})

    return parse_git_log(result.stdout)


def parse_git_log(output: str) -> GitDates:
    created: dict[str, datetime] = {}
    updated: dict[str, datetime] = {}
    current: datetime | None = None

    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("@@ZENSICAL_DOCUMENT_DATE@@"):
            current = parse_datetime(line.removeprefix("@@ZENSICAL_DOCUMENT_DATE@@"))
            continue
        if current is None:
            continue

        path = PurePosixPath(line).as_posix()
        if PurePosixPath(path).suffix.casefold() != ".md" or ".." in PurePosixPath(path).parts:
            continue
        updated.setdefault(path, current)
        created[path] = current

    return GitDates(created=created, updated=updated)


def parse_datetime(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, date):
        parsed = datetime.combine(value, time.min)
    elif isinstance(value, str):
        text = value.strip().strip("'\"")
        if not text:
            return None
        if text.endswith("Z"):
            text = f"{text[:-1]}+00:00"
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            try:
                parsed = datetime.strptime(text, "%Y-%m-%d")
            except ValueError:
                return None
    else:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.now().astimezone().tzinfo)
    return parsed


def _meta_date(
    meta: dict[str, Any],
    direct: tuple[str, ...],
    nested: tuple[str, ...],
) -> datetime | None:
    for field in direct:
        if parsed := parse_datetime(meta.get(field)):
            return parsed

    date_value = meta.get("date")
    if isinstance(date_value, dict):
        for field in nested:
            if parsed := parse_datetime(date_value.get(field)):
                return parsed
    elif direct == ("created",):
        return parse_datetime(date_value)
    return None


def _file_created_at(stat: os.stat_result) -> datetime:
    timestamp = getattr(stat, "st_birthtime", stat.st_mtime)
    return _timestamp_to_datetime(timestamp)


def _timestamp_to_datetime(timestamp: float) -> datetime:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone()
