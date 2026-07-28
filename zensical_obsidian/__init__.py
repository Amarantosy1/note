from .index import DocsIndex, Resolution, ResolutionStatus
from .processors import ObsidianImageProcessor, ObsidianWikiLinkProcessor

from markdown.extensions import Extension


class ObsidianWikiWarning(UserWarning):
    pass


class ObsidianWikiExtension(Extension):
    config = {
        "docs_dir": ["docs", "Directory containing Markdown pages and assets"],
        "base_url": ["/", "Site URL path prefix"],
        "strict": [False, "Raise an error for unresolved or unsupported targets"],
    }

    def extendMarkdown(self, md):
        index = DocsIndex(
            docs_dir=self.getConfig("docs_dir"),
            base_url=self.getConfig("base_url"),
        )
        strict = self.getConfig("strict")
        md.inlinePatterns.register(
            ObsidianImageProcessor(index, strict),
            "zensical_obsidian_image",
            175,
        )
        md.inlinePatterns.register(
            ObsidianWikiLinkProcessor(index, strict),
            "zensical_obsidian_link",
            174,
        )


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
