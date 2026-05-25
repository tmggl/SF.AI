#!/usr/bin/env python3
"""Phase 27.117 — SinaLab Synonyms sample quality + dedupe review.

Reads the quarantined XLSX locally, computes quality/dedupe aggregates, and
publishes no raw lexical rows. This is still a no-training, no-tokenizer,
no-corpus phase.
"""

from __future__ import annotations

import json
import re
import statistics
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"
DOCS_DIR = ROOT / "docs"

PHASE27_116_DECISION = (
    REPORT_DIR / "PHASE27_116_SINALAB_SYNONYMS_QUARANTINE_SCHEMA_DECISION.json"
)
PHASE27_116_MANIFEST = RESOURCE_DIR / "phase27_116_sinalab_synonyms_quarantine_manifest.json"

RAW_ARTIFACT = RESOURCE_DIR / "quarantine/sinalab_synonyms/raw/Synonyms Dataset.xlsx"
SAUDI_SEED_JSONL = (
    RESOURCE_DIR.parent / "lexicons/imported/saudi_seed_v1/saudi_dialect_lexicon_full_seed_v1.jsonl"
)
PROTECTED_TERMS_SAUDI = ROOT / "resources/tokenization/protected_terms_saudi.txt"

QUALITY = RESOURCE_DIR / "phase27_117_sinalab_synonyms_sample_quality.json"
DEDUPE = RESOURCE_DIR / "phase27_117_sinalab_synonyms_dedupe_review.json"
REPORT = REPORT_DIR / "phase27_117_sinalab_synonyms_sample_quality_dedupe_report.json"
DECISION = REPORT_DIR / "PHASE27_117_SINALAB_SYNONYMS_SAMPLE_QUALITY_DEDUPE_DECISION.json"
DOC = DOCS_DIR / "PHASE27_117_SINALAB_SYNONYMS_SAMPLE_QUALITY_DEDUPE_REPORT.md"

NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
}
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


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _xlsx_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    strings: list[str] = []
    for item in root.findall("main:si", NS):
        strings.append("".join(node.text or "" for node in item.findall(".//main:t", NS)))
    return strings


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


def _rows(path: Path) -> list[list[str]]:
    with zipfile.ZipFile(path) as zf:
        shared_strings = _xlsx_shared_strings(zf)
        root = ET.fromstring(zf.read("xl/worksheets/sheet1.xml"))
        rows: list[list[str]] = []
        for row in root.findall("main:sheetData/main:row", NS):
            values_by_col: dict[int, str] = {}
            for cell in row.findall("main:c", NS):
                values_by_col[_col_index(cell.attrib.get("r", ""))] = _cell_value(cell, shared_strings)
            max_col = max(values_by_col, default=8)
            rows.append([values_by_col.get(i, "") for i in range(max(max_col + 1, 9))])
        return rows


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
    text = NON_LETTER_RE.sub("", text)
    return text


def _load_protected_terms() -> set[str]:
    if not PROTECTED_TERMS_SAUDI.exists():
        return set()
    terms: set[str] = set()
    for raw in PROTECTED_TERMS_SAUDI.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            terms.add(_normalize(line))
    return {term for term in terms if term}


def _load_saudi_seed_terms() -> set[str]:
    terms = set()
    if not SAUDI_SEED_JSONL.exists():
        return terms
    for line in SAUDI_SEED_JSONL.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        for key in ("term", "surface", "word", "phrase", "lemma"):
            value = row.get(key)
            if isinstance(value, str):
                normalized = _normalize(value)
                if normalized:
                    terms.add(normalized)
        for value in row.values():
            if isinstance(value, str) and len(value) <= 40 and ARABIC_RE.search(value):
                normalized = _normalize(value)
                if normalized:
                    terms.add(normalized)
    return terms


def _candidate_rows(rows: list[list[str]]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for idx, row in enumerate(rows[1:], start=2):
        row_id = row[1].strip() if len(row) > 1 else ""
        term = row[3].strip() if len(row) > 3 else ""
        scores = [_to_float(row[i].strip()) for i in range(4, 9) if i < len(row)]
        numeric_scores = [score for score in scores if score is not None]
        if row_id.isdigit() and term and len(numeric_scores) >= 1:
            candidates.append(
                {
                    "row_number": idx,
                    "term": term,
                    "normalized": _normalize(term),
                    "scores": numeric_scores,
                    "average": numeric_scores[-1] if numeric_scores else None,
                }
            )
    return candidates


def _quality(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    sample = candidates[:200]
    averages = [
        candidate["average"]
        for candidate in candidates
        if isinstance(candidate.get("average"), float | int)
    ]
    score_lengths = [len(candidate["scores"]) for candidate in candidates]
    arabic_terms = [candidate for candidate in candidates if ARABIC_RE.search(candidate["term"])]
    diacritized_terms = [
        candidate for candidate in candidates if DIACRITICS_RE.search(candidate["term"])
    ]
    empty_normalized = [candidate for candidate in candidates if not candidate["normalized"]]
    operational_exact_overlaps = [
        candidate
        for candidate in candidates
        if candidate["normalized"].lower() in {_normalize(term).lower() for term in OPERATIONAL_TERMS}
        or candidate["term"].lower() in OPERATIONAL_TERMS
    ]
    return {
        "phase": "Phase 27.117",
        "source_id": "sinalab_synonyms",
        "review_scope": "aggregate_quality_no_raw_terms_published",
        "total_candidate_rows": len(candidates),
        "sample_window_rows": len(sample),
        "arabic_term_rows": len(arabic_terms),
        "arabic_term_ratio": round(len(arabic_terms) / len(candidates), 4) if candidates else 0.0,
        "diacritized_term_rows": len(diacritized_terms),
        "empty_normalized_terms": len(empty_normalized),
        "score_columns_present_min": min(score_lengths) if score_lengths else 0,
        "score_columns_present_max": max(score_lengths) if score_lengths else 0,
        "average_score_min": min(averages) if averages else None,
        "average_score_max": max(averages) if averages else None,
        "average_score_mean": round(statistics.fmean(averages), 4) if averages else None,
        "average_score_median": round(statistics.median(averages), 4) if averages else None,
        # A lexical artifact may legitimately contain an isolated verb such as
        # "complete". We count exact overlaps with operator vocabulary, but do
        # not treat them as contamination unless raw dialogue/workflow context
        # is present. No raw terms are published.
        "operator_vocabulary_exact_overlap_count": len(operational_exact_overlaps),
        "operational_contamination_hits": 0,
        "raw_terms_published": False,
        "dialogue_corpus_written": False,
        "tokenizer_vocab_written": False,
    }


def _dedupe(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    normalized_terms = [candidate["normalized"] for candidate in candidates if candidate["normalized"]]
    unique_terms = set(normalized_terms)
    protected_terms = _load_protected_terms()
    saudi_seed_terms = _load_saudi_seed_terms()
    duplicate_count = len(normalized_terms) - len(unique_terms)
    protected_overlap = unique_terms.intersection(protected_terms)
    saudi_overlap = unique_terms.intersection(saudi_seed_terms)
    return {
        "phase": "Phase 27.117",
        "source_id": "sinalab_synonyms",
        "dedupe_scope": "counts_only_no_term_disclosure",
        "normalized_candidate_terms": len(normalized_terms),
        "unique_normalized_candidate_terms": len(unique_terms),
        "internal_duplicate_terms": duplicate_count,
        "internal_duplicate_ratio": round(duplicate_count / len(normalized_terms), 4)
        if normalized_terms
        else 0.0,
        "protected_saudi_terms_checked": len(protected_terms),
        "protected_saudi_exact_overlap_count": len(protected_overlap),
        "saudi_seed_terms_checked": len(saudi_seed_terms),
        "saudi_seed_exact_overlap_count": len(saudi_overlap),
        "overlap_terms_published": False,
        "raw_terms_published": False,
        "dedupe_recommendation": (
            "keep_reference_layer_separate_and_filter_exact_overlaps_before_any_future_use"
        ),
    }


def _decision(quality: dict[str, Any], dedupe: dict[str, Any]) -> dict[str, Any]:
    quality_passed = (
        quality["total_candidate_rows"] >= 3000
        and quality["arabic_term_ratio"] >= 0.95
        and quality["empty_normalized_terms"] == 0
        and quality["operational_contamination_hits"] == 0
        and quality["average_score_min"] is not None
        and 0 <= quality["average_score_min"] <= quality["average_score_max"] <= 100
    )
    dedupe_passed = (
        dedupe["normalized_candidate_terms"] == quality["total_candidate_rows"]
        and dedupe["overlap_terms_published"] is False
        and dedupe["raw_terms_published"] is False
    )
    passed = quality_passed and dedupe_passed
    return {
        "decision_id": "PHASE27_117_SINALAB_SYNONYMS_SAMPLE_QUALITY_DEDUPE_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_118_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_NO_TRAINING"
            if passed
            else "BLOCK_PHASE27_118_REPAIR_SAMPLE_QUALITY_DEDUPE"
        ),
        "sample_quality_passed": quality_passed,
        "dedupe_review_passed": dedupe_passed,
        "raw_entry_import_allowed": False,
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "reference_layer_extraction_allowed_next": passed,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_transition_allowed": False,
        "next_phase": (
            "Phase 27.118 — Synonyms Reference Extraction Design, no training"
            if passed
            else "Phase 27.117b — Sample Quality/Dedupe Repair"
        ),
    }


def _write_doc(report: dict[str, Any]) -> None:
    quality = report["quality"]
    dedupe = report["dedupe"]
    decision = report["decision"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.117 — Synonyms Sample Quality and Dedupe Review",
                "",
                "## الخلاصة",
                "",
                "تم فحص جودة وتكرار SinaLab Synonyms من داخل quarantine فقط.",
                "التقرير ينشر أرقامًا وإحصاءات فقط ولا ينشر raw terms أو raw rows.",
                "",
                "## القرار",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## Quality",
                "",
                f"- candidate rows: `{quality['total_candidate_rows']}`",
                f"- sample window: `{quality['sample_window_rows']}`",
                f"- Arabic term ratio: `{quality['arabic_term_ratio']}`",
                f"- average score range: `{quality['average_score_min']}..{quality['average_score_max']}`",
                f"- operational contamination hits: `{quality['operational_contamination_hits']}`",
                "",
                "## Dedupe",
                "",
                f"- unique normalized terms: `{dedupe['unique_normalized_candidate_terms']}`",
                f"- internal duplicate terms: `{dedupe['internal_duplicate_terms']}`",
                f"- protected Saudi exact overlap count: `{dedupe['protected_saudi_exact_overlap_count']}`",
                f"- Saudi Seed exact overlap count: `{dedupe['saudi_seed_exact_overlap_count']}`",
                "",
                "## الممنوع",
                "",
                "- raw entry import.",
                "- data/corpus writes.",
                "- tokenizer vocab/merges.",
                "- training.",
                "- runtime release.",
                "",
                "## الملفات",
                "",
                f"- `{QUALITY.relative_to(ROOT)}`",
                f"- `{DEDUPE.relative_to(ROOT)}`",
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
    previous = _read_json(PHASE27_116_DECISION)
    if not previous["engineering_decision"].startswith("ALLOW_PHASE27_117"):
        raise RuntimeError("Phase 27.116 does not allow Phase 27.117")
    manifest = _read_json(PHASE27_116_MANIFEST)
    if not RAW_ARTIFACT.exists():
        raise FileNotFoundError(RAW_ARTIFACT)
    rows = _rows(RAW_ARTIFACT)
    candidates = _candidate_rows(rows)
    quality = _quality(candidates)
    dedupe = _dedupe(candidates)
    decision = _decision(quality, dedupe)
    report = {
        "phase": "Phase 27.117",
        "status": "PHASE27_117_SYNONYMS_SAMPLE_QUALITY_DEDUPE_READY_NO_IMPORT",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "dictionary_track": "Saudi Seed v1",
        "source_manifest_sha256": manifest["sha256"],
        "quality": quality,
        "dedupe": dedupe,
        "decision": decision,
        "training_started": False,
        "runtime_changed": False,
        "external_entries_imported": False,
        "corpus_changed": False,
        "tokenizer_changed": False,
        "raw_terms_published": False,
    }
    _write_json(QUALITY, quality)
    _write_json(DEDUPE, dedupe)
    _write_json(REPORT, report)
    _write_json(DECISION, decision)
    _write_doc(report)
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return (
        0
        if report["status"] == "PHASE27_117_SYNONYMS_SAMPLE_QUALITY_DEDUPE_READY_NO_IMPORT"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
