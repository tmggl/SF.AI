"""Loaders — JSONL streamers for SF.AI dialogue datasets.

Both functions are generators so large corpora can be processed without
loading everything into memory. Empty / blank lines are skipped silently.
Lines that fail to parse are skipped by default; pass ``strict=True`` to
raise on the first error instead.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from sf_ai.datasets.schemas import SimpleSample, StructuredSample, parse_record


def iter_jsonl(path: str | Path, *, strict: bool = False) -> Iterator[dict[str, Any]]:
    """Yield raw dicts from a JSONL file."""
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                if strict:
                    raise ValueError(f"{p}:{idx} — JSON decode error: {e.msg}") from e
                continue


def iter_chat_samples(
    path: str | Path, *, strict: bool = False
) -> Iterator[SimpleSample | StructuredSample]:
    """Yield validated chat samples from a JSONL file.

    Records that fail validation are skipped (or raised when ``strict``).
    """
    p = Path(path)
    for idx, raw in enumerate(iter_jsonl(p, strict=strict), start=1):
        try:
            yield parse_record(raw)
        except (ValidationError, ValueError) as e:
            if strict:
                raise ValueError(f"{p}: invalid record #{idx}: {e}") from e
            continue
