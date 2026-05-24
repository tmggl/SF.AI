"""Deterministic corpus splits for SF.AI dialogue training/evaluation."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from sf_ai.datasets.cleaners import SampleCleaner
from sf_ai.datasets.schemas import SimpleSample, StructuredSample, parse_record

FAMILY_ORDER = ("open_social", "followup", "planning", "support", "topic")


@dataclass(frozen=True)
class SplitEntry:
    file: str
    line: int
    split: str
    sha256: str
    dialect: str = ""
    quality: str = ""
    dialogue_family: str = ""


def assign_split(raw_line: str, *, eval_ratio: float = 0.10, salt: str = "sf-ai-v1") -> str:
    """Return train/eval using a stable hash of the raw record line."""
    if not 0.0 < eval_ratio < 1.0:
        raise ValueError("eval_ratio must be between 0 and 1")
    digest = hashlib.sha256((salt + "\n" + raw_line.strip()).encode("utf-8")).hexdigest()
    bucket = int(digest[:8], 16) / 0xFFFFFFFF
    return "eval" if bucket < eval_ratio else "train"


def build_split_entries(
    corpus_root: str | Path,
    *,
    eval_ratio: float = 0.10,
    salt: str = "sf-ai-v1",
) -> tuple[SplitEntry, ...]:
    root = Path(corpus_root)
    entries: list[SplitEntry] = []
    for path in sorted(root.rglob("*.jsonl")):
        rel = path.relative_to(root).as_posix()
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                raw = json.loads(line)
                provenance = raw.get("provenance") if isinstance(raw, dict) else {}
                provenance = provenance if isinstance(provenance, dict) else {}
                digest = hashlib.sha256(line.strip().encode("utf-8")).hexdigest()
                entries.append(
                    SplitEntry(
                        file=rel,
                        line=line_no,
                        split=assign_split(line, eval_ratio=eval_ratio, salt=salt),
                        sha256=digest,
                        dialect=str(provenance.get("dialect", "")),
                        quality=str(provenance.get("quality", "")),
                        dialogue_family=str(_family_from_provenance(provenance)),
                    )
                )
    return tuple(entries)


def write_split_manifest(
    corpus_root: str | Path,
    out: str | Path,
    *,
    eval_ratio: float = 0.10,
    salt: str = "sf-ai-v1",
) -> dict[str, Any]:
    entries = build_split_entries(corpus_root, eval_ratio=eval_ratio, salt=salt)
    counts: dict[str, int] = {}
    dialects: dict[str, dict[str, int]] = {}
    qualities: dict[str, dict[str, int]] = {}
    for entry in entries:
        counts[entry.split] = counts.get(entry.split, 0) + 1
        if entry.dialect:
            dialects.setdefault(entry.split, {})
            dialects[entry.split][entry.dialect] = dialects[entry.split].get(entry.dialect, 0) + 1
        if entry.quality:
            qualities.setdefault(entry.split, {})
            qualities[entry.split][entry.quality] = qualities[entry.split].get(entry.quality, 0) + 1

    manifest = {
        "version": "dialogue_split_v1",
        "method": "sha256_bucket",
        "salt": salt,
        "eval_ratio": eval_ratio,
        "corpus_root": str(corpus_root),
        "total_records": len(entries),
        "counts": counts,
        "dialects": dialects,
        "qualities": qualities,
        "records": [asdict(entry) for entry in entries],
    }
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def load_split_entries(path: str | Path, *, split_name: str) -> set[tuple[str, int]]:
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    records = manifest.get("records")
    if not isinstance(records, list):
        raise ValueError("split manifest must contain a records list")
    selected: set[tuple[str, int]] = set()
    for raw in records:
        if not isinstance(raw, dict) or raw.get("split") != split_name:
            continue
        selected.add((str(raw["file"]), int(raw["line"])))
    return selected


def iter_split_samples(
    corpus_root: str | Path,
    manifest_path: str | Path,
    *,
    split_name: str,
    clean: bool = True,
    cleaner: SampleCleaner | None = None,
) -> Iterator[SimpleSample | StructuredSample]:
    root = Path(corpus_root)
    selected = load_split_entries(manifest_path, split_name=split_name)
    sample_cleaner = cleaner or SampleCleaner()
    for rel, line_no in sorted(selected):
        path = root / rel
        with path.open("r", encoding="utf-8") as handle:
            for idx, line in enumerate(handle, start=1):
                if idx != line_no:
                    continue
                sample = parse_record(json.loads(line))
                if clean:
                    sample = sample_cleaner.clean(sample)
                yield sample
                break


def iter_split_samples_round_robin_by_family(
    corpus_root: str | Path,
    manifest_path: str | Path,
    *,
    split_name: str,
    clean: bool = True,
    cleaner: SampleCleaner | None = None,
) -> Iterator[SimpleSample | StructuredSample]:
    """Yield split samples using a stratified round-robin family order.

    Phase 27.88 showed that sorted file/line order can unintentionally train
    on one dialogue family for hundreds of steps, then switch to another. This
    iterator keeps the same deterministic split membership, but interleaves
    dialogue families so each training window sees open_social/followup/
    planning/support/topic together.
    """
    buckets: dict[str, list[SimpleSample | StructuredSample]] = {
        family: [] for family in FAMILY_ORDER
    }
    buckets["unknown"] = []

    for sample in iter_split_samples(
        corpus_root,
        manifest_path,
        split_name=split_name,
        clean=clean,
        cleaner=cleaner,
    ):
        family = _family_for_sample(sample)
        if family not in buckets:
            family = "unknown"
        buckets[family].append(sample)

    ordered_families = [*FAMILY_ORDER]
    index = 0
    while True:
        emitted = False
        for family in ordered_families:
            bucket = buckets[family]
            if index < len(bucket):
                yield bucket[index]
                emitted = True
        if not emitted:
            break
        index += 1

    for sample in buckets["unknown"]:
        yield sample


def _family_from_provenance(provenance: dict[str, Any]) -> str:
    for key in ("dialogue_family", "answer_family", "prompt_family"):
        value = str(provenance.get(key, "") or "").strip().lower()
        if value:
            return value
    return ""


def _family_for_sample(sample: SimpleSample | StructuredSample) -> str:
    provenance = getattr(sample, "provenance", None)
    for attr in ("dialogue_family", "answer_family", "prompt_family"):
        value = (getattr(provenance, attr, "") or "").strip().lower()
        if value:
            return value
    return "unknown"
