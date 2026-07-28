from markdown.extensions import Extension
from markdown.inlinepatterns import SubstituteTagInlineProcessor


class HardBreakExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            SubstituteTagInlineProcessor(r"(?<!\n)\n(?!\n)", "br"),
            "zensical_hardbreak",
            15,
        )


def makeExtension(**kwargs):
    return HardBreakExtension(**kwargs)
