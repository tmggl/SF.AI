"""Files domain skeleton — no document parsing yet."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class FilesModule(SkeletonDomainModule):
    domain = "files"
    limitations = (
        "does not open, parse, summarize, or transform files yet",
        "no PDF/Word/Excel runtime path through chat",
        "no storage side effects",
    )
