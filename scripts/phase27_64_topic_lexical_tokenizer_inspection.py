#!/usr/bin/env python3
"""Phase 27.64 topic lexical/tokenizer inspection.

No training. No runtime switch.

Phase 27.63 reached 26/30 on the broader canary, but the remaining failures
clustered around topic terms, especially `التعاون` and `الاحترام`. This phase
turns that observation into an auditable tokenizer-v8 decision:

- compare topic term piece counts across existing sovereign tokenizers;
- inspect Phase 27.63 failed rows;
- verify the new Phase 27.64 protected phrase pack;
- decide whether tokenizer v8 is required before any more LM training.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.models.tokenizer import BPETokenizer  # noqa: E402
from sf_ai.models.tokenizer.policy_audit import load_plain_terms  # noqa: E402


TOKENIZER_PATHS: tuple[tuple[str, Path], ...] = (
    ("v1", ROOT / "artifacts/tokenizers/sf_bpe/v1"),
    ("v2", ROOT / "artifacts/tokenizers/sf_bpe/v2"),
    ("v3", ROOT / "artifacts/tokenizers/sf_bpe/v3"),
    ("v4_min_lexical", ROOT / "artifacts/tokenizers/sf_bpe/v4_min_lexical"),
    ("v5_topic_terms", ROOT / "artifacts/tokenizers/sf_bpe/v5_topic_terms"),
    ("v6_weak_lane_terms", ROOT / "artifacts/tokenizers/sf_bpe/v6_weak_lane_terms"),
    ("v7_phase27_58", ROOT / "artifacts/tokenizers/sf_bpe/v7_phase27_58"),
)
TOPIC_TERMS: tuple[str, ...] = (
    "التعاون",
    "الاحترام",
    "الصبر",
    "الوفاء",
    "الصداقة",
    "الشجاعة",
    "الصدق",
    "الهدوء",
)
CRITICAL_TERMS: tuple[str, ...] = ("التعاون", "الاحترام")

DEFAULT_PHASE27_63_REPORT = ROOT / "artifacts/reports/phase27_63_interleaved_family_curriculum_report.json"
DEFAULT_PROTECTED_PACK = ROOT / "resources/tokenization/protected_phrases_phase27_64.txt"
DEFAULT_RESPONSE_FAMILIES = ROOT / "resources/dialogue_format/response_families_phase27_57.json"
DEFAULT_SEMANTIC_RULES = ROOT / "resources/evaluation/semantic_alignment_phase27_57.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_64_topic_lexical_tokenizer_inspection_report.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_64_TOPIC_LEXICAL_TOKENIZER_INSPECTION_REPORT.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 27.64 topic lexical/tokenizer inspection")
    parser.add_argument("--phase27-63-report", type=Path, default=DEFAULT_PHASE27_63_REPORT)
    parser.add_argument("--protected-pack", type=Path, default=DEFAULT_PROTECTED_PACK)
    parser.add_argument("--response-families", type=Path, default=DEFAULT_RESPONSE_FAMILIES)
    parser.add_argument("--semantic-rules", type=Path, default=DEFAULT_SEMANTIC_RULES)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser.parse_args()


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _tokenizer_row(label: str, path: Path, term: str) -> dict[str, Any]:
    tokenizer = BPETokenizer.load(path)
    ids = tokenizer.encode(term)
    meta = _load_json(path / "meta.json")
    protected = set(str(x) for x in meta.get("protected_terms", ()))
    return {
        "tokenizer": label,
        "path": _rel(path),
        "term": term,
        "piece_count": len(ids),
        "ids": ids,
        "decoded": tokenizer.decode(ids),
        "roundtrip_ok": tokenizer.decode(ids) == term,
        "protected_in_meta": term in protected,
    }


def _piece_history() -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for term in TOPIC_TERMS:
        rows: list[dict[str, Any]] = []
        for label, path in TOKENIZER_PATHS:
            if (path / "meta.json").exists():
                rows.append(_tokenizer_row(label, path, term))
        out[term] = rows
    return out


def _latest_rows(history: dict[str, list[dict[str, Any]]]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for term, items in history.items():
        for item in items:
            if item["tokenizer"] == "v7_phase27_58":
                rows[term] = item
                break
    return rows


def _failed_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "id": row["id"],
            "family": row["family"],
            "prompt": row["prompt"],
            "expected_any": row["expected_any"],
            "response": row["response"],
            "reason": row["reason"],
        }
        for row in report.get("rows", ())
        if not row.get("passed")
    ]


def _marker_coverage(path: Path) -> dict[str, Any]:
    raw = _load_json(path)
    topic_markers = set(raw["families"]["topic"]["markers"])
    return {
        "topic_markers": sorted(topic_markers),
        "critical_terms_covered": {term: term in topic_markers for term in CRITICAL_TERMS},
        "all_topic_terms_covered": {term: term in topic_markers for term in TOPIC_TERMS},
    }


def _semantic_coverage(path: Path) -> dict[str, Any]:
    raw = _load_json(path)
    topic_terms = set(raw["categories"]["topic"]["required_any"])
    followup_terms = set(raw["categories"]["followup"]["required_any"])
    return {
        "topic_required_any": sorted(topic_terms),
        "critical_terms_covered": {term: term in topic_terms for term in CRITICAL_TERMS},
        "followup_abst_covered": {"أبسط": "أبسط" in followup_terms, "ابسط": "ابسط" in followup_terms},
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    p2763 = _load_json(args.phase27_63_report)
    history = _piece_history()
    latest = _latest_rows(history)
    protected_terms = load_plain_terms(args.protected_pack)
    protected_set = set(protected_terms)
    failed = _failed_rows(p2763)
    critical_latest = {term: latest[term] for term in CRITICAL_TERMS}
    critical_split = {
        term: row["piece_count"] > 1 or not row["protected_in_meta"]
        for term, row in critical_latest.items()
    }
    v6_was_single = {
        term: any(item["tokenizer"] == "v6_weak_lane_terms" and item["piece_count"] == 1 for item in history[term])
        for term in CRITICAL_TERMS
    }
    v7_regressed_from_v6 = {
        term: bool(v6_was_single[term] and latest[term]["piece_count"] > 1)
        for term in CRITICAL_TERMS
    }
    protected_pack_ready = all(term in protected_set for term in CRITICAL_TERMS)
    tokenizer_v8_required = any(critical_split.values()) or any(v7_regressed_from_v6.values())
    status = (
        "COMPLETED_TOPIC_LEXICAL_INSPECTION_TOKENIZER_V8_REQUIRED_RUNTIME_BLOCKED"
        if tokenizer_v8_required and protected_pack_ready
        else "INCOMPLETE_TOPIC_LEXICAL_INSPECTION"
    )
    return {
        "phase": "Phase 27.64",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_switch_allowed": False,
        "inputs": {
            "phase27_63_report": _rel(args.phase27_63_report),
            "protected_pack": _rel(args.protected_pack),
            "response_families": _rel(args.response_families),
            "semantic_rules": _rel(args.semantic_rules),
        },
        "phase27_63_summary": p2763["summary"],
        "phase27_63_failed_rows": failed,
        "topic_piece_history": history,
        "latest_v7_topic_rows": latest,
        "critical_terms": list(CRITICAL_TERMS),
        "critical_latest_rows": critical_latest,
        "critical_split_or_unprotected": critical_split,
        "v7_regressed_from_v6": v7_regressed_from_v6,
        "protected_pack_terms": protected_terms,
        "protected_pack_ready_for_v8": protected_pack_ready,
        "response_family_marker_coverage": _marker_coverage(args.response_families),
        "semantic_rule_coverage": _semantic_coverage(args.semantic_rules),
        "decisions": {
            "tokenizer_v8_required": tokenizer_v8_required,
            "tokenizer_v8_probe_allowed_next": tokenizer_v8_required and protected_pack_ready,
            "lm_training_allowed_now": False,
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
        },
        "decision": (
            "Tokenizer v8 is required before another LM repair: v7 regressed critical topic terms that v6 protected as single pieces."
            if tokenizer_v8_required
            else "Tokenizer v8 is not required by this inspection."
        ),
        "next_phase": (
            "Phase 27.65 — train tokenizer v8 with Phase 27.64 protected topic pack and rerun bounded topic probe"
            if tokenizer_v8_required and protected_pack_ready
            else "Fix Phase 27.64 protected pack before any tokenizer retrain"
        ),
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    summary = report["phase27_63_summary"]
    critical = report["critical_latest_rows"]
    lines = [
        "# Phase 27.64 — Topic Lexical/Tokenizer Inspection",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة فحص فقط: لا تدريب، لا فتح واجهة، ولا تبديل runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- Phase 27.63 canary: `{summary['passed']}/{summary['total']}`",
        f"- tokenizer v8 required: `{report['decisions']['tokenizer_v8_required']}`",
        f"- next tokenizer probe allowed: `{report['decisions']['tokenizer_v8_probe_allowed_next']}`",
        "",
        "## المصطلحات الحرجة",
        "",
    ]
    for term, row in critical.items():
        lines.append(
            f"- `{term}` في tokenizer v7: `{row['piece_count']}` pieces, protected=`{row['protected_in_meta']}`"
        )
    lines.extend(
        [
            "",
            "## التشخيص",
            "",
            "- `التعاون` و`الاحترام` كانا single-piece في tokenizer v6، ثم تراجعا في tokenizer v7.",
            "- فشل Phase 27.63 المتبقي متركز في topic وليس في open_social/planning/support.",
            "- إضافة تدريب LM جديد قبل إصلاح tokenizer ستكرر نفس الانهيار اللفظي.",
            "",
            "## القرار",
            "",
            report["decision"],
            "",
            "## التالي",
            "",
            report["next_phase"],
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    report = build_report(args)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_doc(report, args.doc)
    print("SF.AI — Phase 27.64 topic lexical/tokenizer inspection")
    print(f"  status       : {report['status']}")
    print(f"  phase27.63   : {report['phase27_63_summary']['passed']}/{report['phase27_63_summary']['total']}")
    print(f"  v8 required  : {report['decisions']['tokenizer_v8_required']}")
    print(f"  next allowed : {report['decisions']['tokenizer_v8_probe_allowed_next']}")
    print(f"  report       : {_rel(args.report)}")
    print(f"  doc          : {_rel(args.doc)}")
    return 0 if report["status"].startswith("COMPLETED") else 2


if __name__ == "__main__":
    raise SystemExit(main())
