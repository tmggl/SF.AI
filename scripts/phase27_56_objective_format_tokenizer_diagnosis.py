#!/usr/bin/env python3
"""Phase 27.56 objective/format/tokenizer diagnosis.

Read-only diagnosis after Phase 27.55. No training, no runtime switch.

The goal is to separate four failure sources:
- capacity: already tested in 27.55;
- objective/format: wrong answer family for the prompt;
- tokenizer: Saudi/social/follow-up terms split too aggressively;
- eval: overlap rule rejecting reasonable answers.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from sf_ai.models.tokenizer import BPETokenizer


ROOT = Path(__file__).resolve().parents[1]
PHASE27_55_REPORT = ROOT / "artifacts/reports/phase27_55_sf50m_diagnostic_micro_probe_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_56_objective_format_tokenizer_diagnosis_report.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_56_OBJECTIVE_FORMAT_TOKENIZER_DIAGNOSIS_REPORT.md"
DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v6_weak_lane_terms"

_SURFACE_REPLACEMENTS = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ة": "ه"})

_CATEGORY_TERMS: dict[str, tuple[str, ...]] = {
    "followup": ("أقصد", "اقصد", "يعني", "بعدها", "نكمل", "وضح", "خطوة"),
    "open_social": ("نسولف", "سولف", "حديث", "موضوع", "يومك", "حياك"),
    "planning": ("ابدأ", "مهمة", "مهام", "رتب", "أولويات", "اولويات", "الأهمية", "الاهميه"),
    "support": ("اهدأ", "اهدا", "نفس", "تنفس", "راحة", "هون", "طمأن", "تستطيع"),
    "topic": ("الشجاعة", "الصداقة", "الصدق", "الهدوء", "الوفاء", "يعني"),
}

_CRITICAL_TERMS = (
    "نسولف",
    "سولف",
    "طمني",
    "توترت",
    "الي تحب",
    "كمل كلامك",
    "طيب ليه",
    "يعني كيف",
    "وش ودك",
    "هات موضوع",
    "يومي كان طويل",
    "حاس بضغط",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 27.56 diagnosis report")
    parser.add_argument("--phase27-55-report", type=Path, default=PHASE27_55_REPORT)
    parser.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser.parse_args()


def _surface(text: str) -> str:
    return " ".join((text or "").translate(_SURFACE_REPLACEMENTS).lower().split())


def _category_guess(text: str) -> str:
    surface = _surface(text)
    scores = {
        category: sum(1 for term in terms if _surface(term) in surface)
        for category, terms in _CATEGORY_TERMS.items()
    }
    best, score = max(scores.items(), key=lambda item: item[1])
    return best if score > 0 else "unknown"


def _relaxed_ok(row: dict[str, Any]) -> bool:
    return bool(
        row["generator_used"]
        and row["guard_allowed"]
        and row["expected_ok"]
        and row["forbidden_ok"]
        and not row["canned_phrase"]
    )


def _model_diagnosis(rows: list[dict[str, Any]]) -> dict[str, Any]:
    strict_passed = sum(1 for row in rows if row["passed"])
    relaxed_rows = [row for row in rows if _relaxed_ok(row)]
    overlap_false_negatives = [
        row["id"]
        for row in rows
        if _relaxed_ok(row) and not row["passed"] and str(row["reason"]).startswith("low_prompt_overlap")
    ]
    expected_missing = [row["id"] for row in rows if row["reason"] == "expected_terms_missing"]
    guard_blocks = [row["id"] for row in rows if str(row["reason"]).startswith("guard:")]
    response_counts = Counter(str(row["response"]) for row in rows if row["response"])

    confusion_rows: list[dict[str, str]] = []
    for row in rows:
        guessed = _category_guess(str(row["response"]))
        if guessed != "unknown" and guessed != row["bucket"]:
            confusion_rows.append(
                {
                    "id": str(row["id"]),
                    "bucket": str(row["bucket"]),
                    "response_category_guess": guessed,
                    "response": str(row["response"]),
                }
            )

    return {
        "strict_passed": strict_passed,
        "total": len(rows),
        "relaxed_semantic_passed": len(relaxed_rows),
        "relaxed_gain": len(relaxed_rows) - strict_passed,
        "overlap_false_negative_ids": overlap_false_negatives,
        "expected_terms_missing_count": len(expected_missing),
        "expected_terms_missing_ids": expected_missing,
        "guard_block_count": len(guard_blocks),
        "guard_block_ids": guard_blocks,
        "unique_responses": len(response_counts),
        "top_repeated_responses": [
            {"count": count, "response": response}
            for response, count in response_counts.most_common(5)
        ],
        "response_family_confusion_count": len(confusion_rows),
        "response_family_confusion_examples": confusion_rows[:10],
    }


def _tokenizer_audit(tokenizer_path: Path, report: dict[str, Any]) -> dict[str, Any]:
    tokenizer = BPETokenizer.load(tokenizer_path)
    terms: set[str] = set(_CRITICAL_TERMS)
    for rows in report["rows"].values():
        for row in rows:
            terms.update(str(term) for term in row.get("expected_terms", ()))
            terms.add(str(row["prompt"]))

    rows: list[dict[str, Any]] = []
    for term in sorted(term for term in terms if term.strip()):
        ids = tokenizer.encode(term)
        pieces = [tokenizer.decode([token_id]) for token_id in ids]
        rows.append(
            {
                "term": term,
                "pieces": len(ids),
                "tokens": pieces,
                "aggressive": len(ids) > 2,
            }
        )
    aggressive = [row for row in rows if row["aggressive"]]
    critical_aggressive = [row for row in aggressive if row["term"] in _CRITICAL_TERMS]
    return {
        "tokenizer": str(tokenizer_path.relative_to(ROOT)),
        "terms_total": len(rows),
        "aggressive_split_count": len(aggressive),
        "critical_aggressive_split_count": len(critical_aggressive),
        "critical_aggressive_terms": critical_aggressive,
        "worst_terms": sorted(rows, key=lambda row: int(row["pieces"]), reverse=True)[:12],
    }


def build_report(phase27_55_report: Path, tokenizer: Path) -> dict[str, Any]:
    previous = json.loads(phase27_55_report.read_text(encoding="utf-8"))
    model_reports = {
        model: _model_diagnosis(rows)
        for model, rows in previous["rows"].items()
    }
    tokenization = _tokenizer_audit(tokenizer, previous)
    sf10 = previous["comparison"]["sf-10m"]["passed"]
    sf50 = previous["comparison"]["sf-50m"]["passed"]
    capacity_delta = previous["comparison"]["delta_passed"]

    sf50_diag = model_reports["sf-50m"]
    eval_overlap_too_strict = sf50_diag["relaxed_gain"] >= 4
    objective_alignment_blocker = sf50_diag["expected_terms_missing_count"] >= 8
    response_family_collapse = sf50_diag["response_family_confusion_count"] >= 5
    tokenizer_blocker = tokenization["critical_aggressive_split_count"] >= 4

    return {
        "phase": "Phase 27.56",
        "status": "COMPLETED_OBJECTIVE_FORMAT_TOKENIZER_DIAGNOSIS_RUNTIME_BLOCKED",
        "training_started": False,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "source_phase": "Phase 27.55",
        "capacity_result": {
            "sf10m_passed": sf10,
            "sf50m_passed": sf50,
            "delta_passed": capacity_delta,
            "capacity_alone_failed": capacity_delta <= 1,
        },
        "model_diagnosis": model_reports,
        "tokenization_diagnosis": tokenization,
        "root_cause_assessment": {
            "capacity_is_primary_fix": False,
            "objective_alignment_blocker": objective_alignment_blocker,
            "response_family_collapse": response_family_collapse,
            "eval_overlap_rule_too_strict": eval_overlap_too_strict,
            "tokenizer_saudi_social_terms_need_repair": tokenizer_blocker,
            "format_conditioning_gap": True,
        },
        "decisions": {
            "runtime_switch_allowed": False,
            "sf50m_full_training_allowed": False,
            "phase28_allowed": False,
            "next_training_allowed": False,
            "next_phase_should_repair_tooling_first": True,
        },
        "next_phase": (
            "Phase 27.57 — tokenizer/eval/format repair pack: protect Saudi social/follow-up terms, "
            "replace prompt-overlap gate with semantic-alignment checks, and define a non-keyword format probe before retraining"
        ),
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    sf10 = report["model_diagnosis"]["sf-10m"]
    sf50 = report["model_diagnosis"]["sf-50m"]
    tok = report["tokenization_diagnosis"]
    lines = [
        "# Phase 27.56 — Objective/Format/Tokenizer Diagnosis",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تشخيص فقط. لم تبدأ تدريبًا ولم تغيّر الواجهة.",
        "",
        f"- capacity delta من 27.55: `{report['capacity_result']['delta_passed']}` فقط.",
        f"- `SF-50M` strict: `{sf50['strict_passed']}/{sf50['total']}`.",
        f"- `SF-50M` relaxed بدون شرط overlap: `{sf50['relaxed_semantic_passed']}/{sf50['total']}`.",
        f"- expected terms missing في `SF-50M`: `{sf50['expected_terms_missing_count']}`.",
        f"- response-family confusion في `SF-50M`: `{sf50['response_family_confusion_count']}`.",
        f"- critical tokenizer aggressive splits: `{tok['critical_aggressive_split_count']}`.",
        "",
        "## التشخيص",
        "",
        "- السعة ليست الإصلاح الأساسي الآن.",
        "- معيار `prompt_overlap` يرفض بعض الردود المقبولة طبيعيًا، لذلك يحتاج استبدالًا بقياس دلالي.",
        "- النموذج يخلط عائلات الردود: يرد بنصيحة تخطيطية على سؤال متابعة أو سوالف.",
        "- كلمات سعودية/حواريّة مهمة ما زالت تتكسر في tokenizer مثل `نسولف` و`طمني` و`الي تحب`.",
        "",
        "## القرار",
        "",
        "- لا runtime switch.",
        "- لا تدريب `SF-50M` كامل.",
        "- لا Phase 28.",
        "- لا تدريب جديد قبل إصلاح tokenizer/eval/format.",
        "",
        "## المرحلة التالية",
        "",
        report["next_phase"],
        "",
        "## أسوأ tokenization splits",
        "",
        "| term | pieces | tokens |",
        "|------|--------|--------|",
    ]
    for row in tok["worst_terms"][:10]:
        pieces = " + ".join(row["tokens"])
        lines.append(f"| `{row['term']}` | {row['pieces']} | `{pieces}` |")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    report = build_report(args.phase27_55_report, args.tokenizer)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_doc(report, args.doc)
    print("SF.AI — Phase 27.56 objective/format/tokenizer diagnosis")
    print(f"  status                 : {report['status']}")
    print(f"  capacity delta          : {report['capacity_result']['delta_passed']}")
    print(f"  sf50 strict             : {report['model_diagnosis']['sf-50m']['strict_passed']}/20")
    print(f"  sf50 relaxed            : {report['model_diagnosis']['sf-50m']['relaxed_semantic_passed']}/20")
    print(f"  expected missing        : {report['model_diagnosis']['sf-50m']['expected_terms_missing_count']}")
    print(f"  tokenizer critical split: {report['tokenization_diagnosis']['critical_aggressive_split_count']}")
    print(f"  report                  : {args.report}")
    print(f"  doc                     : {args.doc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
