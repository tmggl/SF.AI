#!/usr/bin/env python3
"""Phase 27.116 — SinaLab Synonyms quarantine checksum + schema dry-run.

Downloads the public Synonyms XLSX artifact into a git-ignored quarantine
folder, records checksum/license/schema metadata, and blocks import/training.
It never writes raw rows into data/corpus, tokenizer vocab, or runtime stores.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.request
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"
DOCS_DIR = ROOT / "docs"

PHASE27_115_DECISION = (
    REPORT_DIR / "PHASE27_115_ARABIC_ONTOLOGY_SYNONYMS_ARTIFACT_GATE_DECISION.json"
)

QUARANTINE_DIR = RESOURCE_DIR / "quarantine/sinalab_synonyms"
RAW_DIR = QUARANTINE_DIR / "raw"
RAW_ARTIFACT = RAW_DIR / "Synonyms Dataset.xlsx"
ARTIFACT_URL = (
    "https://raw.githubusercontent.com/SinaLab/Synonyms/main/Synonyms%20Dataset.xlsx"
)
REPO_URL = "https://github.com/SinaLab/Synonyms"

MANIFEST = RESOURCE_DIR / "phase27_116_sinalab_synonyms_quarantine_manifest.json"
SCHEMA = RESOURCE_DIR / "phase27_116_sinalab_synonyms_schema_dry_run.json"
ATTRIBUTION = RESOURCE_DIR / "phase27_116_sinalab_synonyms_attribution.json"
REPORT = REPORT_DIR / "phase27_116_sinalab_synonyms_quarantine_schema_report.json"
DECISION = REPORT_DIR / "PHASE27_116_SINALAB_SYNONYMS_QUARANTINE_SCHEMA_DECISION.json"
DOC = DOCS_DIR / "PHASE27_116_SINALAB_SYNONYMS_QUARANTINE_SCHEMA_REPORT.md"

NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "office": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _download_artifact() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        ARTIFACT_URL,
        headers={"User-Agent": "SF.AI Phase27.116 quarantine checksum dry-run"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = response.read()
    RAW_ARTIFACT.write_bytes(payload)


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
    strings: list[str] = []
    for item in root.findall("main:si", NS):
        parts = [node.text or "" for node in item.findall(".//main:t", NS)]
        strings.append("".join(parts))
    return strings


def _col_index(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha()).upper()
    value = 0
    for ch in letters:
        value = value * 26 + (ord(ch) - ord("A") + 1)
    return max(value - 1, 0)


def _row_number(cell_ref: str) -> int:
    digits = "".join(ch for ch in cell_ref if ch.isdigit())
    return int(digits or "0")


def _cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    value_node = cell.find("main:v", NS)
    inline_node = cell.find("main:is/main:t", NS)
    if inline_node is not None:
        return inline_node.text or ""
    if value_node is None or value_node.text is None:
        return ""
    value = value_node.text
    if cell_type == "s":
        try:
            return shared_strings[int(value)]
        except (IndexError, ValueError):
            return ""
    return value


def _dimension_rows_cols(ref: str) -> tuple[int | None, int | None]:
    if not ref or ":" not in ref:
        return None, None
    start, end = ref.split(":", 1)
    rows = _row_number(end) - _row_number(start) + 1
    cols = _col_index(end) - _col_index(start) + 1
    return rows if rows > 0 else None, cols if cols > 0 else None


def _safe_header(text: str) -> str:
    # Keep column labels only. If a header is suspiciously long, summarize it
    # structurally so the report cannot leak lexical data rows.
    normalized = re.sub(r"\s+", " ", text.strip())
    if len(normalized) > 80:
        return f"<long_header_len:{len(normalized)}>"
    return normalized


def _workbook_sheets(zf: zipfile.ZipFile) -> list[dict[str, str]]:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_by_id = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall("rel:Relationship", NS)
        if "Id" in rel.attrib and "Target" in rel.attrib
    }
    sheets: list[dict[str, str]] = []
    for sheet in workbook.findall("main:sheets/main:sheet", NS):
        rel_id = sheet.attrib.get(f"{{{NS['office']}}}id", "")
        target = rel_by_id.get(rel_id, "")
        path = f"xl/{target}" if not target.startswith("xl/") else target
        sheets.append(
            {
                "name": sheet.attrib.get("name", ""),
                "sheet_id": sheet.attrib.get("sheetId", ""),
                "xlsx_path": path,
            }
        )
    return sheets


def _schema_dry_run(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as zf:
        shared_strings = _xlsx_shared_strings(zf)
        sheets = _workbook_sheets(zf)
        sheet_summaries: list[dict[str, Any]] = []
        for sheet in sheets:
            root = ET.fromstring(zf.read(sheet["xlsx_path"]))
            dimension = root.find("main:dimension", NS)
            dimension_ref = dimension.attrib.get("ref", "") if dimension is not None else ""
            rows, cols = _dimension_rows_cols(dimension_ref)
            first_row = root.find("main:sheetData/main:row", NS)
            headers: list[str] = []
            if first_row is not None:
                values_by_col: dict[int, str] = {}
                for cell in first_row.findall("main:c", NS):
                    ref = cell.attrib.get("r", "")
                    values_by_col[_col_index(ref)] = _safe_header(_cell_value(cell, shared_strings))
                if values_by_col:
                    max_col = max(values_by_col)
                    headers = [values_by_col.get(idx, "") for idx in range(max_col + 1)]
            sheet_summaries.append(
                {
                    "name": sheet["name"],
                    "sheet_id": sheet["sheet_id"],
                    "dimension_ref": dimension_ref,
                    "estimated_rows": rows,
                    "estimated_columns": cols,
                    "header_columns": headers,
                    "raw_rows_exported": False,
                }
            )
    return {
        "phase": "Phase 27.116",
        "artifact": "Synonyms Dataset.xlsx",
        "parser": "stdlib_zip_xml_metadata_only",
        "sheets": sheet_summaries,
        "raw_row_values_saved": False,
        "dialogue_corpus_written": False,
        "tokenizer_vocab_written": False,
    }


def _manifest(checksum: str, size_bytes: int) -> dict[str, Any]:
    return {
        "phase": "Phase 27.116",
        "source_id": "sinalab_synonyms",
        "source_name": "SinaLab Arabic Synonyms Dataset",
        "artifact_name": "Synonyms Dataset.xlsx",
        "artifact_url": ARTIFACT_URL,
        "repository_url": REPO_URL,
        "local_quarantine_path": str(RAW_ARTIFACT.relative_to(ROOT)),
        "raw_artifact_git_ignored": True,
        "sha256": checksum,
        "size_bytes": size_bytes,
        "license": "CC-BY-4.0",
        "license_evidence": [
            "Repository LICENSE: Creative Commons Attribution 4.0 International",
            "Repository README: License: CC-BY-4.0",
            "SinaLab resources page: Synonyms (CC-BY-4.0)",
        ],
        "allowed_now": {
            "quarantine_download": True,
            "checksum_record": True,
            "schema_dry_run": True,
            "raw_entry_import": False,
            "training_text_import": False,
            "dialogue_corpus_write": False,
            "tokenizer_vocab_import": False,
            "runtime_lookup": False,
            "training": False,
        },
    }


def _attribution(checksum: str) -> dict[str, Any]:
    return {
        "phase": "Phase 27.116",
        "source_id": "sinalab_synonyms",
        "title": "Synonyms Dataset",
        "authors": [
            "Sana Ghanem",
            "Mustafa Jarrar",
            "Radi Jarrar",
            "Ibrahim Bounhas",
        ],
        "citation": (
            "A Benchmark and Scoring Algorithm for Enriching Arabic Synonyms, "
            "Global WordNet Conference 2023"
        ),
        "repository_url": REPO_URL,
        "artifact_url": ARTIFACT_URL,
        "license": "CC-BY-4.0",
        "artifact_sha256": checksum,
        "sf_ai_usage_now": "quarantine checksum and schema dry-run only",
        "training_allowed": False,
        "tokenizer_vocab_allowed": False,
        "dialogue_corpus_allowed": False,
    }


def _decision(manifest: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    sheets_present = len(schema["sheets"]) >= 1
    checksum_present = len(manifest["sha256"]) == 64
    blocked = (
        manifest["allowed_now"]["raw_entry_import"] is False
        and manifest["allowed_now"]["training"] is False
        and schema["raw_row_values_saved"] is False
    )
    passed = sheets_present and checksum_present and blocked
    return {
        "decision_id": "PHASE27_116_SINALAB_SYNONYMS_QUARANTINE_SCHEMA_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_117_SYNONYMS_SAMPLE_QUALITY_AND_DEDUPE_REVIEW_NO_TRAINING"
            if passed
            else "BLOCK_PHASE27_117_REPAIR_QUARANTINE_SCHEMA"
        ),
        "quarantine_checksum_recorded": checksum_present,
        "schema_dry_run_passed": sheets_present,
        "raw_entry_import_allowed": False,
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_transition_allowed": False,
        "next_phase": (
            "Phase 27.117 — Synonyms Sample Quality and Dedupe Review, no training"
            if passed
            else "Phase 27.116b — Quarantine Schema Repair"
        ),
    }


def _write_doc(report: dict[str, Any]) -> None:
    manifest = report["manifest"]
    schema = report["schema_dry_run"]
    decision = report["decision"]
    first_sheet = schema["sheets"][0] if schema["sheets"] else {}
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.116 — Synonyms Quarantine Checksum and Schema Dry-Run",
                "",
                "## الخلاصة",
                "",
                "تم تنزيل artifact في quarantine محلي git-ignored، وحُسب checksum، وفُحص schema فقط.",
                "لم يتم نقل raw rows إلى corpus، ولم يبدأ tokenizer أو training.",
                "",
                "## القرار",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## Artifact",
                "",
                f"- المصدر: `{manifest['repository_url']}`",
                f"- الملف: `{manifest['artifact_name']}`",
                f"- الحجم: `{manifest['size_bytes']}` bytes",
                f"- sha256: `{manifest['sha256']}`",
                f"- quarantine path: `{manifest['local_quarantine_path']}` (غير مرفوع إلى git)",
                "",
                "## Schema Dry-Run",
                "",
                f"- sheets: `{len(schema['sheets'])}`",
                f"- first sheet: `{first_sheet.get('name', '')}`",
                f"- dimension: `{first_sheet.get('dimension_ref', '')}`",
                f"- estimated rows: `{first_sheet.get('estimated_rows', '')}`",
                f"- estimated columns: `{first_sheet.get('estimated_columns', '')}`",
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
                f"- `{MANIFEST.relative_to(ROOT)}`",
                f"- `{SCHEMA.relative_to(ROOT)}`",
                f"- `{ATTRIBUTION.relative_to(ROOT)}`",
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
    previous = _read_json(PHASE27_115_DECISION)
    if not previous["engineering_decision"].startswith("ALLOW_PHASE27_116"):
        raise RuntimeError("Phase 27.115 does not allow Phase 27.116")
    _download_artifact()
    checksum = _sha256(RAW_ARTIFACT)
    manifest = _manifest(checksum, RAW_ARTIFACT.stat().st_size)
    schema = _schema_dry_run(RAW_ARTIFACT)
    attribution = _attribution(checksum)
    decision = _decision(manifest, schema)
    report = {
        "phase": "Phase 27.116",
        "status": "PHASE27_116_SYNONYMS_QUARANTINE_SCHEMA_READY_NO_IMPORT",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "dictionary_track": "Saudi Seed v1",
        "manifest": manifest,
        "schema_dry_run": schema,
        "attribution": attribution,
        "decision": decision,
        "training_started": False,
        "runtime_changed": False,
        "external_entries_imported": False,
        "corpus_changed": False,
        "tokenizer_changed": False,
    }
    _write_json(MANIFEST, manifest)
    _write_json(SCHEMA, schema)
    _write_json(ATTRIBUTION, attribution)
    _write_json(REPORT, report)
    _write_json(DECISION, decision)
    _write_doc(report)
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return (
        0
        if report["status"] == "PHASE27_116_SYNONYMS_QUARANTINE_SCHEMA_READY_NO_IMPORT"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
