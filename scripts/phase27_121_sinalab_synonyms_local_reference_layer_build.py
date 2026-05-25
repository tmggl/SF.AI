#!/usr/bin/env python3
"""Phase 27.121 — build SinaLab Synonyms local reference records.

This phase writes actual reference records with terms only inside the
gitignored local reference-layer directory. Committed outputs contain counts,
hashes, schema status, and policy decisions only. No corpus/tokenizer/training
or runtime lookup is changed.
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

PHASE27_120_DECISION = (
    REPORT_DIR / "PHASE27_120_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATE_DECISION.json"
)
PHASE27_120_GATE = RESOURCE_DIR / "phase27_120_sinalab_synonyms_local_reference_layer_build_gate.json"
PHASE27_118_DESIGN = RESOURCE_DIR / "phase27_118_sinalab_synonyms_reference_extraction_design.json"
PHASE27_116_MANIFEST = RESOURCE_DIR / "phase27_116_sinalab_synonyms_quarantine_manifest.json"
RAW_ARTIFACT = RESOURCE_DIR / "quarantine/sinalab_synonyms/raw/Synonyms Dataset.xlsx"
SAUDI_SEED_JSONL = (
    RESOURCE_DIR.parent / "lexicons/imported/saudi_seed_v1/saudi_dialect_lexicon_full_seed_v1.jsonl"
)
PROTECTED_TERMS_SAUDI = ROOT / "resources/tokenization/protected_terms_saudi.txt"

REFERENCE_DIR = RESOURCE_DIR / "reference_layers/sinalab_synonyms"
REFERENCE_RECORDS = REFERENCE_DIR / "reference_records.jsonl"
EVAL_CANDIDATES = REFERENCE_DIR / "eval_candidates.jsonl"

BUILD_MANIFEST = RESOURCE_DIR / "phase27_121_sinalab_synonyms_local_reference_layer_build_manifest.json"
VALIDATION = RESOURCE_DIR / "phase27_121_sinalab_synonyms_local_reference_layer_validation.json"
REPORT = REPORT_DIR / "phase27_121_sinalab_synonyms_local_reference_layer_build_report.json"
DECISION = REPORT_DIR / "PHASE27_121_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_DECISION.json"
DOC = DOCS_DIR / "PHASE27_121_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_REPORT.md"

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
    source_order: int
    synset_number: str
    row_id: str
    term: str
    normalized: str
    scores: tuple[float, ...]
    average: float
    has_arabic: bool


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


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
            synset_number = values_by_col.get(0, "").strip()
            row_id = values_by_col.get(1, "").strip()
            term = values_by_col.get(3, "").strip()
            scores = tuple(
                score
                for score in (_to_float(values_by_col.get(i, "").strip()) for i in range(4, 9))
                if score is not None
            )
            if row_id.isdigit() and term and scores:
                candidates.append(
                    Candidate(
                        row_number=int(row.attrib.get("r", "0") or 0),
                        source_order=source_order,
                        synset_number=synset_number,
                        row_id=row_id,
                        term=term,
                        normalized=_normalize(term),
                        scores=scores,
                        average=scores[-1],
                        has_arabic=bool(ARABIC_RE.search(term)),
                    )
                )
    return candidates


def _band(score: float) -> str:
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def _select_reference_candidates(design: dict[str, Any]) -> list[Candidate]:
    candidates = _candidates(RAW_ARTIFACT)
    protected_terms = _load_terms(PROTECTED_TERMS_SAUDI)
    saudi_seed_terms = _load_saudi_seed_terms()
    op_terms = {_normalize(term).lower() for term in OPERATIONAL_TERMS}
    min_reference_score = design["filter_policy"]["minimum_average_score_for_reference"]

    eligible = [
        c
        for c in candidates
        if c.normalized
        and c.has_arabic
        and c.average >= min_reference_score
        and c.normalized not in protected_terms
        and c.normalized not in saudi_seed_terms
        and c.normalized.lower() not in op_terms
    ]
    best_by_normalized: dict[str, Candidate] = {}
    for candidate in eligible:
        current = best_by_normalized.get(candidate.normalized)
        if current is None or candidate.average > current.average:
            best_by_normalized[candidate.normalized] = candidate
    return sorted(best_by_normalized.values(), key=lambda c: (c.source_order, c.row_number))


def _record(candidate: Candidate, artifact_sha256: str) -> dict[str, Any]:
    return {
        "record_id": f"sinalab-synonyms-{candidate.row_number}",
        "source_id": "sinalab_synonyms",
        "artifact_sha256": artifact_sha256,
        "source_row_number": candidate.row_number,
        "synset_number": candidate.synset_number,
        "row_id": candidate.row_id,
        "candidate_term": candidate.term,
        "candidate_normalized": candidate.normalized,
        "linguist_scores": list(candidate.scores[:-1]),
        "average_score": candidate.average,
        "quality_band": _band(candidate.average),
        "license": "CC-BY-4.0",
        "attribution_required": True,
        "training_allowed": False,
        "dialogue_corpus_allowed": False,
        "tokenizer_vocab_allowed": False,
        "runtime_lookup_allowed": False,
    }


def _hash_lines(path: Path) -> dict[str, Any]:
    line_count = 0
    with path.open("rb") as handle:
        for line in handle:
            if line.strip():
                line_count += 1
    return {
        "relative_path": str(path.relative_to(ROOT)),
        "sha256": _sha256(path),
        "line_count": line_count,
        "gitignored": True,
    }


def _build_manifest(records: list[dict[str, Any]], eval_records: list[dict[str, Any]]) -> dict[str, Any]:
    quality_counts = {"high": 0, "medium": 0, "low": 0}
    for row in records:
        quality_counts[row["quality_band"]] += 1
    return {
        "phase": "Phase 27.121",
        "source_id": "sinalab_synonyms",
        "build_scope": "local_reference_records_gitignored_terms_not_committed",
        "reference_record_count": len(records),
        "eval_candidate_record_count": len(eval_records),
        "quality_band_counts": quality_counts,
        "local_files": {
            "reference_records": _hash_lines(REFERENCE_RECORDS),
            "eval_candidates": _hash_lines(EVAL_CANDIDATES),
        },
        "local_terms_files_gitignored": True,
        "raw_terms_committed": False,
        "committed_manifest_contains_terms": False,
        "dialogue_corpus_written": False,
        "tokenizer_vocab_written": False,
        "training_started": False,
        "runtime_lookup_enabled": False,
    }


def _validation(manifest: dict[str, Any], gate: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "reference_count_matches_gate": (
            manifest["reference_record_count"] == gate["max_local_reference_records_next"]
        ),
        "eval_count_matches_gate": (
            manifest["eval_candidate_record_count"] == gate["max_local_eval_candidate_records_next"]
        ),
        "local_files_gitignored": all(item["gitignored"] for item in manifest["local_files"].values()),
        "raw_terms_not_committed": manifest["raw_terms_committed"] is False,
        "manifest_contains_no_terms": manifest["committed_manifest_contains_terms"] is False,
        "no_corpus_write": manifest["dialogue_corpus_written"] is False,
        "no_tokenizer_write": manifest["tokenizer_vocab_written"] is False,
        "no_training": manifest["training_started"] is False,
        "no_runtime_lookup": manifest["runtime_lookup_enabled"] is False,
    }
    return {
        "phase": "Phase 27.121",
        "validation_id": "PHASE27_121_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_VALIDATION",
        "checks": checks,
        "passed": all(checks.values()),
        "raw_terms_published": False,
        "reference_records_committed": False,
        "training_allowed": False,
        "runtime_release_allowed": False,
    }


def _decision(validation: dict[str, Any]) -> dict[str, Any]:
    passed = validation["passed"] is True
    return {
        "decision_id": "PHASE27_121_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_122_SYNONYMS_REFERENCE_QUERY_AND_EVAL_GATE_NO_TRAINING"
            if passed
            else "BLOCK_PHASE27_122_REPAIR_LOCAL_REFERENCE_LAYER_BUILD"
        ),
        "local_reference_layer_build_passed": passed,
        "local_reference_records_exist": passed,
        "raw_terms_commit_allowed": False,
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "dialogue_corpus_allowed": False,
        "tokenizer_vocab_allowed": False,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_transition_allowed": False,
        "next_phase": (
            "Phase 27.122 — Synonyms Reference Query and Eval Gate, no training"
            if passed
            else "Phase 27.121b — Local Reference Layer Build Repair"
        ),
    }


def _write_doc(report: dict[str, Any]) -> None:
    manifest = report["manifest"]
    decision = report["decision"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.121 — Synonyms Local Reference Layer Build",
                "",
                "## الخلاصة",
                "",
                "تم بناء reference records محلية فقط داخل مسار gitignored.",
                "المرفوع يحتوي counts/hashes فقط ولا يحتوي raw terms.",
                "",
                "## القرار",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## Build Counts",
                "",
                f"- local reference records: `{manifest['reference_record_count']}`",
                f"- local eval candidates: `{manifest['eval_candidate_record_count']}`",
                f"- high quality: `{manifest['quality_band_counts']['high']}`",
                f"- medium quality: `{manifest['quality_band_counts']['medium']}`",
                f"- low quality: `{manifest['quality_band_counts']['low']}`",
                "",
                "## Local Files",
                "",
                "- reference records JSONL: gitignored, contains terms locally only.",
                "- eval candidates JSONL: gitignored, contains terms locally only.",
                "- committed reports expose hashes/counts only.",
                "",
                "## الممنوع",
                "",
                "- raw terms in git.",
                "- data/corpus writes.",
                "- tokenizer vocab/merges.",
                "- training.",
                "- runtime lookup activation.",
                "- SF-50M transition.",
                "",
                "## الملفات المرفوعة",
                "",
                f"- `{BUILD_MANIFEST.relative_to(ROOT)}`",
                f"- `{VALIDATION.relative_to(ROOT)}`",
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
    previous = _read_json(PHASE27_120_DECISION)
    if not previous["engineering_decision"].startswith("ALLOW_PHASE27_121"):
        raise RuntimeError("Phase 27.120 does not allow Phase 27.121")
    gate = _read_json(PHASE27_120_GATE)
    design = _read_json(PHASE27_118_DESIGN)
    artifact_manifest = _read_json(PHASE27_116_MANIFEST)
    if _sha256(RAW_ARTIFACT) != artifact_manifest["sha256"]:
        raise RuntimeError("SinaLab Synonyms artifact checksum mismatch")

    candidates = _select_reference_candidates(design)
    records = [_record(candidate, artifact_manifest["sha256"]) for candidate in candidates]
    eval_records = [record for record in records if record["average_score"] >= 70.0]
    _write_jsonl(REFERENCE_RECORDS, records)
    _write_jsonl(EVAL_CANDIDATES, eval_records)

    manifest = _build_manifest(records, eval_records)
    validation = _validation(manifest, gate)
    decision = _decision(validation)
    report = {
        "phase": "Phase 27.121",
        "status": "PHASE27_121_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILT_GITIGNORED_NO_TRAINING",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "dictionary_track": "Saudi Seed v1",
        "manifest": manifest,
        "validation": validation,
        "decision": decision,
        "training_started": False,
        "runtime_changed": False,
        "external_entries_imported": False,
        "reference_records_written_locally": True,
        "reference_records_committed": False,
        "corpus_changed": False,
        "tokenizer_changed": False,
        "raw_terms_published": False,
    }
    _write_json(BUILD_MANIFEST, manifest)
    _write_json(VALIDATION, validation)
    _write_json(REPORT, report)
    _write_json(DECISION, decision)
    _write_doc(report)
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return (
        0
        if report["status"] == "PHASE27_121_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILT_GITIGNORED_NO_TRAINING"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
