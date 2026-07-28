from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path, PurePosixPath
from urllib.parse import quote

from markdown import Markdown


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif"}


class ResolutionStatus(Enum):
    FOUND = "found"
    MISSING = "missing"
    AMBIGUOUS = "ambiguous"
    INVALID = "invalid"


@dataclass(frozen=True)
class Resolution:
    status: ResolutionStatus
    target: str
    path: Path | None = None
    url: str | None = None
    candidates: tuple[str, ...] = ()
    fragment: str | None = None


class DocsIndex:
    def __init__(self, docs_dir: str, base_url: str = "/"):
        self.docs_dir = Path(docs_dir).expanduser().resolve()
        self.base_url = self._normalize_base_url(base_url)
        self.pages = self._collect(lambda path: path.suffix.lower() == ".md")
        self.assets = self._collect(lambda path: path.suffix.lower() in IMAGE_SUFFIXES)

    def resolve_page(self, target: str, heading: str | None = None) -> Resolution:
        invalid = self._invalid_target(target)
        if invalid:
            return Resolution(ResolutionStatus.INVALID, target)

        candidates = self._page_candidates(target)
        resolution = self._resolve_candidates(target, candidates, self._page_url)
        if resolution.status is not ResolutionStatus.FOUND or heading is None:
            return resolution

        fragments = self._resolve_heading(resolution.path, heading)
        if not fragments:
            return Resolution(
                ResolutionStatus.MISSING,
                f"{target}#{heading}",
                candidates=(resolution.path.relative_to(self.docs_dir).as_posix(),),
            )
        if len(fragments) > 1:
            page = resolution.path.relative_to(self.docs_dir).as_posix()
            return Resolution(
                ResolutionStatus.AMBIGUOUS,
                f"{target}#{heading}",
                candidates=tuple(f"{page}#{fragment}" for fragment in fragments),
            )
        fragment = fragments[0]
        return Resolution(
            ResolutionStatus.FOUND,
            target,
            path=resolution.path,
            url=f"{resolution.url}#{quote(fragment, safe='-_~')}",
            fragment=fragment,
        )

    def resolve_image(self, target: str) -> Resolution:
        invalid = self._invalid_target(target)
        if invalid or PurePosixPath(target).suffix.lower() not in IMAGE_SUFFIXES:
            return Resolution(ResolutionStatus.INVALID, target)
        return self._resolve_candidates(target, self._asset_candidates(target), self._asset_url)

    def _collect(self, predicate) -> tuple[Path, ...]:
        if not self.docs_dir.is_dir():
            return ()
        return tuple(
            sorted(
                (path for path in self.docs_dir.rglob("*") if path.is_file() and predicate(path)),
                key=lambda path: path.relative_to(self.docs_dir).as_posix(),
            )
        )

    def _page_candidates(self, target: str) -> tuple[Path, ...]:
        normalized = target.replace("\\", "/").strip("/")
        requested = PurePosixPath(normalized)
        requested_no_suffix = requested.with_suffix("") if requested.suffix.lower() == ".md" else requested

        if len(requested.parts) > 1:
            exact = self.docs_dir.joinpath(*requested_no_suffix.parts).with_suffix(".md")
            index = self.docs_dir.joinpath(*requested_no_suffix.parts, "index.md")
            return self._existing((exact, index))

        root_exact = self.docs_dir.joinpath(*requested_no_suffix.parts).with_suffix(".md")
        if root_exact in self.pages:
            return (root_exact,)

        basename = requested_no_suffix.name.casefold()
        return tuple(
            path
            for path in self.pages
            if path.stem.casefold() == basename
            or (
                path.name.casefold() == "index.md"
                and path.parent.name.casefold() == basename
            )
        )

    def _asset_candidates(self, target: str) -> tuple[Path, ...]:
        normalized = target.replace("\\", "/").strip("/")
        requested = PurePosixPath(normalized)
        if len(requested.parts) > 1:
            return self._existing((self.docs_dir.joinpath(*requested.parts),))
        basename = requested.name.casefold()
        return tuple(path for path in self.assets if path.name.casefold() == basename)

    def _existing(self, paths) -> tuple[Path, ...]:
        return tuple(path for path in paths if path in self.pages or path in self.assets)

    def _resolve_candidates(self, target, candidates, url_builder) -> Resolution:
        paths = tuple(dict.fromkeys(candidates))
        names = tuple(path.relative_to(self.docs_dir).as_posix() for path in paths)
        if not paths:
            return Resolution(ResolutionStatus.MISSING, target)
        if len(paths) > 1:
            return Resolution(ResolutionStatus.AMBIGUOUS, target, candidates=names)
        path = paths[0]
        return Resolution(
            ResolutionStatus.FOUND,
            target,
            path=path,
            url=url_builder(path),
            candidates=names,
        )

    def _resolve_heading(self, path: Path, heading: str) -> tuple[str, ...]:
        md = Markdown(extensions=["toc"])
        md.convert(path.read_text(encoding="utf-8"))
        wanted = self._normalize_heading(heading)
        return tuple(
            token["id"]
            for token in self._flatten_toc(md.toc_tokens)
            if self._normalize_heading(token["name"]) == wanted
        )

    def _flatten_toc(self, tokens):
        for token in tokens:
            yield token
            yield from self._flatten_toc(token.get("children", ()))

    def _page_url(self, path: Path) -> str:
        relative = path.relative_to(self.docs_dir)
        if relative.name == "index.md":
            route = relative.parent.as_posix()
            if route == ".":
                route = ""
        else:
            route = relative.with_suffix("").as_posix()
        return self._url(route, trailing_slash=True)

    def _asset_url(self, path: Path) -> str:
        return self._url(path.relative_to(self.docs_dir).as_posix(), trailing_slash=False)

    def _url(self, route: str, trailing_slash: bool) -> str:
        encoded = quote(route, safe="/-._~")
        parts = [part.strip("/") for part in (self.base_url, encoded) if part.strip("/")]
        url = "/" + "/".join(parts)
        if trailing_slash and not url.endswith("/"):
            url += "/"
        return url

    @staticmethod
    def _invalid_target(target: str) -> bool:
        stripped = target.strip()
        if not stripped or "\x00" in stripped or "://" in stripped:
            return True
        path = PurePosixPath(stripped.replace("\\", "/"))
        return path.is_absolute() or ".." in path.parts

    @staticmethod
    def _normalize_base_url(base_url: str) -> str:
        stripped = str(base_url).strip()
        if not stripped or stripped == "/":
            return ""
        if "://" in stripped or ".." in PurePosixPath(stripped).parts:
            raise ValueError("base_url must be a site-relative URL path")
        return "/" + stripped.strip("/")

    @staticmethod
    def _normalize_heading(heading: str) -> str:
        return " ".join(str(heading).strip().casefold().split())
