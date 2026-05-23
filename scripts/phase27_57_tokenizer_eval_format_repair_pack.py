#!/usr/bin/env python3
"""Phase 27.57 tokenizer/eval/format repair pack.

No training and no runtime switch. This phase installs the repair policy that
must exist before the next model run:

- protected Saudi/social/follow-up phrases for the next tokenizer;
- semantic-alignment rules that replace brittle prompt-overlap checks;
- response-family rules to catch family collapse before runtime.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE27_56_REPORT = ROOT / "artifacts/reports/phase27_56_objective_format_tokenizer_diagnosis_report.json"
PROTECTED_PHRASES = ROOT / "resources/tokenization/protected_phrases_phase27_57.txt"
SEMANTIC_RULES = ROOT / "resources/evaluation/semantic_alignment_phase27_57.json"
RESPONSE_FAMILIES = ROOT / "resources/dialogue_format/response_families_phase27_57.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_57_tokenizer_eval_format_repair_pack_report.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_57_TOKENIZER_EVAL_FORMAT_REPAIR_PACK_REPORT.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 27.57 repair-pack report")
    parser.add_argument("--phase27-56-report", type=Path, default=PHASE27_56_REPORT)
    parser.add_argument("--protected-phrases", type=Path, default=PROTECTED_PHRASES)
    parser.add_argument("--semantic-rules", type=Path, default=SEMANTIC_RULES)
    parser.add_argument("--response-families", type=Path, default=RESPONSE_FAMILIES)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser.parse_args()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_terms(path: Path) -> list[str]:
    terms: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            terms.append(line)
    return terms


def build_report(
    *,
    phase27_56_report: Path,
    protected_phrases: Path,
    semantic_rules: Path,
    response_families: Path,
) -> dict[str, Any]:
    previous = _load_json(phase27_56_report)
    protected = _load_terms(protected_phrases)
    semantic = _load_json(semantic_rules)
    families = _load_json(response_families)

    critical_terms = [
        row["term"]
        for row in previous["tokenization_diagnosis"]["critical_aggressive_terms"]
    ]
    protected_set = set(protected)
    covered_critical = [term for term in critical_terms if term in protected_set]
    missing_critical = [term for term in critical_terms if term not in protected_set]

    categories = set(previous["model_diagnosis"]["sf-50m"]["response_family_confusion_examples"][i]["bucket"]
                     for i in range(len(previous["model_diagnosis"]["sf-50m"]["response_family_confusion_examples"])))
    categories.update({"followup", "open_social", "planning", "support", "topic"})
    semantic_categories = set((semantic.get("categories") or {}).keys())
    family_categories = set((families.get("families") or {}).keys())

    overlap_disabled = bool(
        (semantic.get("decision_rules") or {}).get("prompt_overlap_required") is False
    )
    cross_family_enabled = bool(
        (semantic.get("decision_rules") or {}).get("cross_family_blocking_enabled") is True
    )
    required_categories_covered = categories <= semantic_categories and categories <= family_categories
    forbidden_collapses = families.get("forbidden_collapses") or []

    ready = (
        not missing_critical
        and overlap_disabled
        and cross_family_enabled
        and required_categories_covered
        and len(forbidden_collapses) >= 5
    )

    return {
        "phase": "Phase 27.57",
        "status": (
            "COMPLETED_TOKENIZER_EVAL_FORMAT_REPAIR_PACK_READY_FOR_RETRAINING_GATE"
            if ready
            else "INCOMPLETE_TOKENIZER_EVAL_FORMAT_REPAIR_PACK"
        ),
        "training_started": False,
        "runtime_switch_allowed": False,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "source_phase": "Phase 27.56",
        "inputs": {
            "phase27_56_report": str(phase27_56_report.relative_to(ROOT)),
            "protected_phrases": str(protected_phrases.relative_to(ROOT)),
            "semantic_rules": str(semantic_rules.relative_to(ROOT)),
            "response_families": str(response_families.relative_to(ROOT)),
        },
        "protected_phrase_pack": {
            "total": len(protected),
            "critical_terms_from_27_56": critical_terms,
            "covered_critical_terms": covered_critical,
            "missing_critical_terms": missing_critical,
            "ready_for_next_tokenizer": not missing_critical,
        },
        "semantic_alignment_pack": {
            "categories": sorted(semantic_categories),
            "prompt_overlap_required": (semantic.get("decision_rules") or {}).get("prompt_overlap_required"),
            "cross_family_blocking_enabled": cross_family_enabled,
            "covered_required_categories": required_categories_covered,
            "ready_for_eval_replacement": overlap_disabled and cross_family_enabled and required_categories_covered,
        },
        "response_family_pack": {
            "families": sorted(family_categories),
            "forbidden_collapse_count": len(forbidden_collapses),
            "ready_for_format_probe": required_categories_covered and len(forbidden_collapses) >= 5,
        },
        "decisions": {
            "runtime_switch_allowed": False,
            "sf50m_full_training_allowed": False,
            "phase28_allowed": False,
            "next_training_allowed": ready,
            "training_scope_if_next": "bounded tokenizer/eval/format repair probe only",
        },
        "next_phase": (
            "Phase 27.58 — retrain tokenizer with Phase 27.57 protected phrases and run bounded format/alignment probe"
            if ready
            else "Fix Phase 27.57 repair-pack coverage before any retraining"
        ),
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    protected = report["protected_phrase_pack"]
    semantic = report["semantic_alignment_pack"]
    families = report["response_family_pack"]
    lines = [
        "# Phase 27.57 — Tokenizer/Eval/Format Repair Pack",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة إصلاح أدوات فقط. لا تدريب ولا فتح واجهة.",
        "",
        f"- protected phrases: `{protected['total']}`",
        f"- critical terms covered: `{len(protected['covered_critical_terms'])}/{len(protected['critical_terms_from_27_56'])}`",
        f"- semantic categories: `{len(semantic['categories'])}`",
        f"- prompt overlap required: `{semantic['prompt_overlap_required']}`",
        f"- forbidden family collapses: `{families['forbidden_collapse_count']}`",
        "",
        "## القرار",
        "",
        f"- next training allowed: `{str(report['decisions']['next_training_allowed']).lower()}`",
        "- runtime switch: `false`",
        "- full SF-50M: `false`",
        "- Phase 28: `false`",
        "",
        "## ما الذي تم إصلاحه",
        "",
        "- أضيفت عبارات سعودية/حواريّة محمية للـ tokenizer القادم.",
        "- أضيفت قواعد semantic alignment لا تعتمد على prompt-overlap.",
        "- أضيفت خريطة response families لاكتشاف خلط الردود قبل runtime.",
        "",
        "## المرحلة التالية",
        "",
        report["next_phase"],
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    report = build_report(
        phase27_56_report=args.phase27_56_report,
        protected_phrases=args.protected_phrases,
        semantic_rules=args.semantic_rules,
        response_families=args.response_families,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_doc(report, args.doc)
    print("SF.AI — Phase 27.57 tokenizer/eval/format repair pack")
    print(f"  status              : {report['status']}")
    print(f"  protected phrases   : {report['protected_phrase_pack']['total']}")
    print(f"  critical coverage   : {len(report['protected_phrase_pack']['covered_critical_terms'])}/{len(report['protected_phrase_pack']['critical_terms_from_27_56'])}")
    print(f"  overlap required    : {report['semantic_alignment_pack']['prompt_overlap_required']}")
    print(f"  family collapses    : {report['response_family_pack']['forbidden_collapse_count']}")
    print(f"  next training       : {report['decisions']['next_training_allowed']}")
    print(f"  report              : {args.report}")
    print(f"  doc                 : {args.doc}")
    return 0 if report["status"].startswith("COMPLETED") else 2


if __name__ == "__main__":
    raise SystemExit(main())
