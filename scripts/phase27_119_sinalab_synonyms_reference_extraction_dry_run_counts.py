#!/usr/bin/env python3
"""Phase 27.119 — SinaLab Synonyms reference extraction dry-run counts.

Runs the Phase 27.118 filter policy over the quarantined XLSX and publishes
counts only. No raw terms, no reference records, no corpus/tokenizer writes,
and no training.
"""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"
DOCS_DIR = ROOT / "docs"

PHASE27_118_DECISION = (
    REPORT_DIR / "PHASE27_118_SINALAB_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_DECISION.json"
)
PHASE27_118_DESIGN = RESOURCE_DIR / "phase27_118_sinalab_synonyms_reference_extraction_design.json"
PHASE27_116_MANIFEST = RESOURCE_DIR / "phase27_116_sinalab_synonyms_quarantine_manifest.json"
RAW_ARTIFACT = RESOURCE_DIR / "quarantine/sinalab_synonyms/raw/Synonyms Dataset.xlsx"
SAUDI_SEED_JSONL = (
    RESOURCE_DIR.parent / "lexicons/imported/saudi_seed_v1/saudi_dialect_lexicon_full_seed_v1.jsonl"
)
PROTECTED_TERMS_SAUDI = ROOT / "resources/tokenization/protected_terms_saudi.txt"

COUNTS = RESOURCE_DIR / "phase27_119_sinalab_synonyms_reference_dry_run_counts.json"
FILTERS = RESOURCE_DIR / "phase27_119_sinalab_synonyms_filter_drop_counts.json"
REPORT = REPORT_DIR / "phase27_119_sinalab_synonyms_reference_dry_run_counts_report.json"
DECISION = REPORT_DIR / "PHASE27_119_SINALAB_SYNONYMS_REFERENCE_DRY_RUN_COUNTS_DECISION.json"
DOC = DOCS_DIR / "PHASE27_119_SINALAB_SYNONYMS_REFERENCE_DRY_RUN_COUNTS_REPORT.md"

NS = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
ARABIC_RE = re.compile(r"[\u0600-\u06ff]")
DIACRITICS_RE = re.compile(r"[\u064b-\u065f\u0670]")
TATWEEL_RE = re.compile("\u0640")
NON_LETTER_RE = re.compile(r"[^\u0600-\u06ffA-Za-z0-9]+")
OPERATIONAL_TERMS = {
    "phase",
    "corpus",
    "tokenizer",
    "pytest",
    "commit",
    "readiness",
    "gate",
    "gates",
    "training",
    "checkpoint",
    "runtime",
    "ارفع",
    "التالي",
    "اكمل",
}


@dataclass(frozen=True)
class Candidate:
    row_number: int
    normalized: str
    has_arabic: bool
    average: float
    source_order: int


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _xlsx_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    return [
        "".join(node.text or "" for node in item.findall(".//main:t", NS))
        for item in root.findall("main:si", NS)
    ]


def _col_index(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha()).upper()
    value = 0
    for ch in letters:
        value = value * 26 + (ord(ch) - ord("A") + 1)
    return max(value - 1, 0)


def _cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    value_node = cell.find("main:v", NS)
    inline_node = cell.find("main:is/main:t", NS)
    if inline_node is not None:
        return inline_node.text or ""
    if value_node is None or value_node.text is None:
        return ""
    value = value_node.text
    if cell.attrib.get("t") == "s":
        try:
            return shared_strings[int(value)]
        except (IndexError, ValueError):
            return ""
    return value


def _to_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def _normalize(text: str) -> str:
    text = text.strip()
    text = TATWEEL_RE.sub("", text)
    text = DIACRITICS_RE.sub("", text)
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = text.replace("ى", "ي").replace("ة", "ه")
    return NON_LETTER_RE.sub("", text)


def _load_terms(path: Path) -> set[str]:
    terms: set[str] = set()
    if not path.exists():
        return terms
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        normalized = _normalize(line)
        if normalized:
            terms.add(normalized)
    return terms


def _load_saudi_seed_terms() -> set[str]:
    terms: set[str] = set()
    if not SAUDI_SEED_JSONL.exists():
        return terms
    for line in SAUDI_SEED_JSONL.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        for value in row.values():
            if isinstance(value, str) and len(value) <= 40 and ARABIC_RE.search(value):
                normalized = _normalize(value)
                if normalized:
                    terms.add(normalized)
    return terms


def _candidates(path: Path) -> list[Candidate]:
    candidates: list[Candidate] = []
    with zipfile.ZipFile(path) as zf:
        shared_strings = _xlsx_shared_strings(zf)
        root = ET.fromstring(zf.read("xl/worksheets/sheet1.xml"))
        for source_order, row in enumerate(root.findall("main:sheetData/main:row", NS)[1:], start=1):
            values_by_col: dict[int, str] = {}
            for cell in row.findall("main:c", NS):
                values_by_col[_col_index(cell.attrib.get("r", ""))] = _cell_value(cell, shared_strings)
            row_id = values_by_col.get(1, "").strip()
            term = values_by_col.get(3, "").strip()
            average = _to_float(values_by_col.get(8, "").strip())
            if row_id.isdigit() and term and average is not None:
                candidates.append(
                    Candidate(
                        row_number=int(row.attrib.get("r", "0") or 0),
                        normalized=_normalize(term),
                        has_arabic=bool(ARABIC_RE.search(term)),
                        average=average,
                        source_order=source_order,
                    )
                )
    return candidates


def _band(score: float) -> str:
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def _band_counts(candidates: list[Candidate]) -> dict[str, int]:
    counts = {"high": 0, "medium": 0, "low": 0}
    for candidate in candidates:
        counts[_band(candidate.average)] += 1
    return counts


def _dry_run(design: dict[str, Any], manifest: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    candidates = _candidates(RAW_ARTIFACT)
    protected_terms = _load_terms(PROTECTED_TERMS_SAUDI)
    saudi_seed_terms = _load_saudi_seed_terms()
    op_terms = {_normalize(term).lower() for term in OPERATIONAL_TERMS}
    min_reference_score = design["filter_policy"]["minimum_average_score_for_reference"]
    min_eval_score = design["filter_policy"]["minimum_average_score_for_eval_candidate"]

    stage0 = candidates
    empty_normalized = [c for c in stage0 if not c.normalized]
    non_arabic = [c for c in stage0 if not c.has_arabic]
    score_below_reference = [c for c in stage0 if c.average < min_reference_score]
    protected_overlap = [c for c in stage0 if c.normalized in protected_terms]
    saudi_overlap = [c for c in stage0 if c.normalized in saudi_seed_terms]
    operator_overlap = [c for c in stage0 if c.normalized.lower() in op_terms]

    eligible = [
        c
        for c in stage0
        if c.normalized
        and c.has_arabic
        and c.average >= min_reference_score
        and c.normalized not in protected_terms
        and c.normalized not in saudi_seed_terms
        and c.normalized.lower() not in op_terms
    ]

    best_by_normalized: dict[str, Candidate] = {}
    duplicate_replaced = 0
    duplicate_dropped = 0
    for candidate in eligible:
        current = best_by_normalized.get(candidate.normalized)
        if current is None:
            best_by_normalized[candidate.normalized] = candidate
        elif candidate.average > current.average:
            best_by_normalized[candidate.normalized] = candidate
            duplicate_replaced += 1
        else:
            duplicate_dropped += 1

    reference_candidates = list(best_by_normalized.values())
    eval_candidates = [c for c in reference_candidates if c.average >= min_eval_score]
    counts = {
        "phase": "Phase 27.119",
        "source_id": "sinalab_synonyms",
        "artifact_sha256": manifest["sha256"],
        "artifact_sha256_verified": _sha256(RAW_ARTIFACT) == manifest["sha256"],
        "dry_run_scope": "counts_only_no_raw_terms_published",
        "input_candidate_rows": len(stage0),
        "quality_band_counts_input": _band_counts(stage0),
        "eligible_before_duplicate_collapse": len(eligible),
        "reference_candidate_count_after_filters": len(reference_candidates),
        "eval_candidate_count_after_filters": len(eval_candidates),
        "quality_band_counts_after_filters": _band_counts(reference_candidates),
        "raw_terms_published": False,
        "reference_records_written": False,
        "dialogue_corpus_written": False,
        "tokenizer_vocab_written": False,
        "training_started": False,
    }
    filters = {
        "phase": "Phase 27.119",
        "source_id": "sinalab_synonyms",
        "filter_scope": "drop_counts_only_no_terms",
        "empty_normalized_drop_count": len(empty_normalized),
        "non_arabic_drop_count": len(non_arabic),
        "score_below_reference_drop_count": len(score_below_reference),
        "protected_saudi_overlap_drop_count": len(protected_overlap),
        "saudi_seed_overlap_drop_count": len(saudi_overlap),
        "operator_workflow_overlap_drop_count": len(operator_overlap),
        "duplicate_dropped_after_filters": duplicate_dropped,
        "duplicate_replaced_by_higher_score": duplicate_replaced,
        "raw_terms_published": False,
        "overlap_terms_published": False,
    }
    return counts, filters


def _decision(counts: dict[str, Any], filters: dict[str, Any]) -> dict[str, Any]:
    passed = (
        counts["artifact_sha256_verified"] is True
        and counts["reference_candidate_count_after_filters"] > 0
        and counts["raw_terms_published"] is False
        and counts["reference_records_written"] is False
        and filters["raw_terms_published"] is False
    )
    return {
        "decision_id": "PHASE27_119_SINALAB_SYNONYMS_REFERENCE_DRY_RUN_COUNTS_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_120_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATED_NO_TRAINING"
            if passed
            else "BLOCK_PHASE27_120_REPAIR_REFERENCE_DRY_RUN_COUNTS"
        ),
        "dry_run_counts_passed": passed,
        "raw_entry_import_allowed": False,
        "reference_layer_build_allowed_next": passed,
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "raw_terms_publish_allowed": False,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_transition_allowed": False,
        "next_phase": (
            "Phase 27.120 — Synonyms Local Reference Layer Build Gate, no training"
            if passed
            else "Phase 27.119b — Reference Dry-Run Counts Repair"
        ),
    }


def _write_doc(report: dict[str, Any]) -> None:
    counts = report["counts"]
    filters = report["filter_drop_counts"]
    decision = report["decision"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.119 — Synonyms Reference Extraction Dry-Run Counts",
                "",
                "## الخلاصة",
                "",
                "تم تنفيذ dry-run counts فقط حسب تصميم 27.118. لا توجد raw terms أو reference records.",
                "",
                "## القرار",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## Counts",
                "",
                f"- input candidate rows: `{counts['input_candidate_rows']}`",
                f"- eligible before duplicate collapse: `{counts['eligible_before_duplicate_collapse']}`",
                f"- reference candidates after filters: `{counts['reference_candidate_count_after_filters']}`",
                f"- eval candidates after filters: `{counts['eval_candidate_count_after_filters']}`",
                "",
                "## Filter Drops",
                "",
                f"- score below reference: `{filters['score_below_reference_drop_count']}`",
                f"- Saudi Seed overlap: `{filters['saudi_seed_overlap_drop_count']}`",
                f"- protected Saudi overlap: `{filters['protected_saudi_overlap_drop_count']}`",
                f"- duplicate dropped after filters: `{filters['duplicate_dropped_after_filters']}`",
                "",
                "## الممنوع",
                "",
                "- raw terms in reports.",
                "- reference records written.",
                "- data/corpus writes.",
                "- tokenizer vocab/merges.",
                "- training.",
                "- runtime release.",
                "",
                "## الملفات",
                "",
                f"- `{COUNTS.relative_to(ROOT)}`",
                f"- `{FILTERS.relative_to(ROOT)}`",
                f"- `{REPORT.relative_to(ROOT)}`",
                f"- `{DECISION.relative_to(ROOT)}`",
                "",
                "## التالي",
                "",
                "```text",
                decision["next_phase"],
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def build_report() -> dict[str, Any]:
    previous = _read_json(PHASE27_118_DECISION)
    if not previous["engineering_decision"].startswith("ALLOW_PHASE27_119"):
        raise RuntimeError("Phase 27.118 does not allow Phase 27.119")
    design = _read_json(PHASE27_118_DESIGN)
    manifest = _read_json(PHASE27_116_MANIFEST)
    counts, filters = _dry_run(design, manifest)
    decision = _decision(counts, filters)
    report = {
        "phase": "Phase 27.119",
        "status": "PHASE27_119_SYNONYMS_REFERENCE_DRY_RUN_COUNTS_READY_NO_IMPORT",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "dictionary_track": "Saudi Seed v1",
        "counts": counts,
        "filter_drop_counts": filters,
        "decision": decision,
        "training_started": False,
        "runtime_changed": False,
        "external_entries_imported": False,
        "corpus_changed": False,
        "tokenizer_changed": False,
        "raw_terms_published": False,
    }
    _write_json(COUNTS, counts)
    _write_json(FILTERS, filters)
    _write_json(REPORT, report)
    _write_json(DECISION, decision)
    _write_doc(report)
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return (
        0
        if report["status"] == "PHASE27_119_SYNONYMS_REFERENCE_DRY_RUN_COUNTS_READY_NO_IMPORT"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
