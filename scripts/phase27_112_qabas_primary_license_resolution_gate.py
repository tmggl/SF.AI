#!/usr/bin/env python3
"""Phase 27.112 — Qabas primary license resolution gate, no import/training.

This gate resolves the Phase 27.111 conflict as conservatively as possible.
Primary SinaLab resources currently list Qabas as CC-BY-ND-4.0 while Masader
metadata lists Apache-1.0. Because "ND" blocks derivative/adapted lexicon
outputs, Qabas stays reference-only until the downloadable artifact license is
captured with stronger evidence.
"""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"

QABAS_SOURCE_CARD = RESOURCE_DIR / "qabas_source_card_phase27_111.json"
QABAS_METADATA = RESOURCE_DIR / "selected_masader_metadata/qabas.json"
EVIDENCE = RESOURCE_DIR / "phase27_112_qabas_license_evidence.json"
REPORT = REPORT_DIR / "phase27_112_qabas_primary_license_resolution_gate_report.json"
DECISION = REPORT_DIR / "PHASE27_112_QABAS_PRIMARY_LICENSE_RESOLUTION_GATE_DECISION.json"
DOC = ROOT / "docs/PHASE27_112_QABAS_PRIMARY_LICENSE_RESOLUTION_GATE_REPORT.md"

SINALAB_RESOURCES = "https://sina.birzeit.edu/resources/"
QABAS_PAGE = "https://sina.birzeit.edu/qabas"
QABAS_ABOUT = "https://sina.birzeit.edu/qabas/about"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "SF.AI local license gate"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def _strip_html(text: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _snippets(text: str, needles: tuple[str, ...]) -> list[str]:
    clean = _strip_html(text)
    out: list[str] = []
    lower = clean.lower()
    for needle in needles:
        idx = lower.find(needle.lower())
        if idx >= 0:
            start = max(0, idx - 140)
            end = min(len(clean), idx + len(needle) + 180)
            out.append(clean[start:end])
    return out


def _fetch_primary_evidence() -> dict[str, Any]:
    resources_html = _fetch_text(SINALAB_RESOURCES)
    qabas_html = _fetch_text(QABAS_PAGE)
    about_html = _fetch_text(QABAS_ABOUT)
    resources_clean = _strip_html(resources_html)
    return {
        "sources": [
            {
                "id": "sinalab_resources",
                "url": SINALAB_RESOURCES,
                "role": "primary_resources_listing",
                "observed_license": "CC-BY-ND-4.0" if "CC-BY-ND-4.0" in resources_clean else "not_found",
                "qabas_snippets": _snippets(resources_html, ("Qabas Lexicon", "CC-BY-ND-4.0")),
            },
            {
                "id": "qabas_page",
                "url": QABAS_PAGE,
                "role": "primary_qabas_page",
                "observed_license": "not_explicit_in_page",
                "qabas_snippets": _snippets(qabas_html, ("Most Commonly Used Words", "Qabas")),
            },
            {
                "id": "qabas_about",
                "url": QABAS_ABOUT,
                "role": "primary_qabas_about_page",
                "observed_license": "not_explicit_in_page",
                "qabas_snippets": _snippets(about_html, ("Qabas", "شمولية معجم قبس")),
            },
        ]
    }


def _build_decision(evidence: dict[str, Any], source_card: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    masader_license = source_card["masader_license"]
    primary_license = next(
        item["observed_license"]
        for item in evidence["sources"]
        if item["id"] == "sinalab_resources"
    )
    nd_detected = "ND" in primary_license.upper()
    conflict_unresolved = masader_license != primary_license
    import_allowed = bool(primary_license and not nd_detected and not conflict_unresolved)
    return {
        "decision_id": "PHASE27_112_QABAS_PRIMARY_LICENSE_RESOLUTION_GATE_DECISION",
        "engineering_decision": (
            "ALLOW_QABAS_IMPORT_AFTER_LICENSE_GATE"
            if import_allowed
            else "BLOCK_QABAS_IMPORT_REFERENCE_ONLY_OPEN_PHASE27_113_PERMISSIVE_LEXICAL_ALTERNATIVES"
        ),
        "masader_license": masader_license,
        "primary_license": primary_license,
        "license_conflict_unresolved": conflict_unresolved,
        "no_derivatives_detected": nd_detected,
        "qabas_downloadable_artifact_license_captured": False,
        "qabas_raw_entry_import_allowed": import_allowed,
        "qabas_reference_only_allowed": True,
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "metadata_volume": metadata.get("Volume"),
        "metadata_unit": metadata.get("Unit"),
        "next_phase": (
            "Phase 27.113 — Permissive Lexical Alternatives Intake Gate, no training"
            if not import_allowed
            else "Phase 27.113 — Qabas Candidate Terms Dry-Run, no training"
        ),
    }


def _write_doc(report: dict[str, Any]) -> None:
    decision = report["decision"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.112 — Qabas Primary License Resolution Gate",
                "",
                "## الخلاصة",
                "",
                "حُسمت البوابة بشكل محافظ: Qabas يبقى `reference-only` ولا يدخل",
                "كمداخل فعلية أو corpus أو tokenizer vocab.",
                "",
                "## القرار",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## الأدلة",
                "",
                f"- Masader metadata: `{decision['masader_license']}`.",
                f"- SinaLab resources primary page: `{decision['primary_license']}`.",
                "- صفحة Qabas/About لا تعرض رخصة artifact أو شروط استخدام قابلة للحسم.",
                "",
                "## لماذا حُجب الاستيراد؟",
                "",
                "- الترخيص الأساسي المرصود يحتوي `ND`، وهذا يمنع المشتقات.",
                "- يوجد تضارب مع Masader metadata.",
                "- لا توجد رخصة artifact قابلة للتحميل محفوظة محليًا تحسم النزاع.",
                "",
                "## المسموح",
                "",
                "- استخدام Qabas كمرجع metadata/source-discovery فقط.",
                "- الاستمرار في البحث عن مصادر lexical permissive بترخيص أوضح.",
                "",
                "## الممنوع",
                "",
                "- raw Qabas entries.",
                "- Qabas داخل `data/corpus`.",
                "- Qabas كـ tokenizer vocab أو merges.",
                "- تدريب أو runtime release.",
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
    source_card = _read_json(QABAS_SOURCE_CARD)
    metadata = _read_json(QABAS_METADATA)
    evidence = _fetch_primary_evidence()
    decision = _build_decision(evidence, source_card, metadata)
    report = {
        "phase": "Phase 27.112",
        "status": "PHASE27_112_QABAS_REFERENCE_ONLY_IMPORT_BLOCKED",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "source_id": "qabas",
        "evidence": evidence,
        "decision": decision,
        "training_started": False,
        "runtime_changed": False,
        "actual_qabas_entries_imported": False,
    }
    _write_json(EVIDENCE, evidence)
    _write_json(REPORT, report)
    _write_json(DECISION, decision)
    _write_doc(report)
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PHASE27_112_QABAS_REFERENCE_ONLY_IMPORT_BLOCKED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
