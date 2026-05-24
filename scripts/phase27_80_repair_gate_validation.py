#!/usr/bin/env python3
"""Phase 27.80 — Repair Gate Encoding and Dry-Run Validation.

No training happens here. This script turns the Phase 27.79 repair design into
executable gates and runs a dry validation against the current sovereign corpus
and historical canary reports.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_79_objective_curriculum_decoding_design_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_80_REPAIR_GATE_VALIDATION_DECISION.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_80_repair_gate_validation_report.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_80_REPAIR_GATE_VALIDATION.md"
DEFAULT_CORPUS = ROOT / "data/corpus/chat/jsonl"
DEFAULT_SPLIT = ROOT / "data/corpus/chat/splits/dialogue_split_v1.json"

FAMILIES = ("open_social", "followup", "planning", "support", "topic")
OPERATOR_TERMS = (
    "التالي",
    "اكمل",
    "ارفع",
    "phase",
    "gates",
    "corpus",
    "tokenizer",
    "pytest",
    "commit",
    "readiness",
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.80 repair gate validation")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--split", type=Path, default=DEFAULT_SPLIT)
    return p.parse_args()


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_source(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"missing Phase 27.79 report: {path}")
    report = _load_json(path)
    if report.get("phase") != "Phase 27.79":
        raise ValueError("Phase 27.80 expects Phase 27.79 source report")
    decision = report.get("decision", {})
    if decision.get("decision_id") != "PHASE27_79_REPAIR_DESIGN_DECISION":
        raise ValueError("missing PHASE27_79_REPAIR_DESIGN_DECISION")
    if decision.get("new_training_allowed") is not False:
        raise ValueError("Phase 27.80 requires Phase 27.79 to block training")
    return report


def validate_objective_spec(source: dict[str, Any]) -> dict[str, Any]:
    objective = source["objective_design"]
    required_controls = set(objective.get("required_controls", []))
    required = {
        "single_answer_boundary",
        "explicit_family_condition",
        "explicit_dialect_condition",
        "topic_or_none_condition",
        "assistant_eos_required",
        "no_cross_sample_packing",
    }
    missing = sorted(required - required_controls)
    passed = (
        objective.get("name") == "family_conditioned_prompt_to_answer_objective_v1"
        and objective.get("loss_scope") == "assistant_answer_only_with_eos"
        and not missing
        and any("<|dialogue_family:{family}|>" in item for item in objective.get("format", []))
    )
    return {
        "gate": "objective_spec_validator",
        "passed": passed,
        "missing_controls": missing,
        "objective": objective.get("name"),
        "loss_scope": objective.get("loss_scope"),
    }


def validate_decoding_policy(source: dict[str, Any]) -> dict[str, Any]:
    decoding = source["decoding_design"]
    controls = set(decoding.get("controls", []))
    required = {
        "stop_at_eos",
        "max_answer_tokens_by_family",
        "no_repeat_ngram",
        "repetition_penalty",
        "family_allowed_terms_floor",
        "family_blocked_terms_soft_guard",
        "malformed_fragment_guard",
    }
    forbidden = set(decoding.get("not_allowed", []))
    missing = sorted(required - controls)
    template_masking_blocked = "template replacement" in forbidden
    passed = not missing and template_masking_blocked
    return {
        "gate": "decoding_policy_config_validator",
        "passed": passed,
        "policy": decoding.get("name"),
        "missing_controls": missing,
        "template_masking_blocked": template_masking_blocked,
    }


def _iter_records(corpus: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(corpus.glob("*.jsonl")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            item = json.loads(line)
            item["_file"] = path.name
            item["_line"] = line_no
            records.append(item)
    return records


def _text(item: dict[str, Any], *, role: str | None = None) -> str:
    parts = []
    for message in item.get("messages", []):
        if role is None or message.get("role") == role:
            parts.append(str(message.get("content", "")))
    return " ".join(parts)


def record_family(item: dict[str, Any], *, role: str | None = None) -> str:
    provenance = item.get("provenance", {})
    family = provenance.get("dialogue_family")
    if isinstance(family, str) and family in FAMILIES:
        return family
    key = "prompt_family" if role == "user" else "answer_family"
    family = provenance.get(key)
    if isinstance(family, str) and family in FAMILIES:
        return family
    return classify_family(_text(item, role=role))


def classify_family(text: str) -> str:
    t = re.sub(r"\s+", " ", text.strip().lower())
    if any(k in t for k in ("نظم", "رتب", "مهام", "وقتي", "جدولي", "خطة", "ابدأ بالأهم")):
        return "planning"
    if any(k in t for k in ("متوتر", "قلق", "خائف", "زعلان", "تعبان", "أهدأ", "اهدأ", "نفس")):
        return "support"
    if any(k in t for k in ("ما معنى", "وش معنى", "اشرح", "الفرق", "الشجاعة", "الصداقة", "التعاون", "الصبر")):
        return "topic"
    if any(k in t for k in ("يعني", "كيف", "ليه", "لماذا", "وضح", "ما فهمت", "بعدين")):
        return "followup"
    return "open_social"


def validate_curriculum_and_family_matrix(
    records: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    explicit_records = [
        item
        for item in records
        if item.get("provenance", {}).get("dialogue_family") in FAMILIES
    ]
    explicit_counts = Counter(
        item.get("provenance", {}).get("dialogue_family") for item in explicit_records
    )
    use_explicit_balanced_view = all(explicit_counts[family] >= 500 for family in FAMILIES)
    view_records = explicit_records if use_explicit_balanced_view else records

    dialect_counts: Counter[str] = Counter()
    family_counts: Counter[str] = Counter()
    matrix: dict[str, dict[str, int]] = {f: {g: 0 for g in FAMILIES} for f in FAMILIES}

    for item in view_records:
        provenance = item.get("provenance", {})
        dialect = provenance.get("dialect", "unknown")
        dialect_counts[dialect] += 1
        prompt_family = record_family(item, role="user")
        answer_family = record_family(item, role="assistant")
        family_counts[prompt_family] += 1
        matrix[prompt_family][answer_family] += 1

    total = sum(family_counts.values())
    present = {family for family in FAMILIES if family_counts[family] > 0}
    min_family_count = min(family_counts[f] for f in FAMILIES)
    max_family_count = max(family_counts[f] for f in FAMILIES)
    family_ratio = round(max_family_count / max(1, min_family_count), 4)
    dialect_total = dialect_counts["msa"] + dialect_counts["saudi"]
    dialect_delta = abs(dialect_counts["msa"] - dialect_counts["saudi"]) / max(1, dialect_total)

    diagonal = sum(matrix[f][f] for f in FAMILIES)
    diagonal_rate = round(diagonal / max(1, total), 4)
    family_balance_passed = present == set(FAMILIES) and family_ratio <= 4.0
    dialect_balance_passed = dialect_total == total and dialect_delta <= 0.08
    matrix_passed = diagonal_rate >= 0.65

    curriculum = {
        "gate": "curriculum_family_balance_dry_run",
        "passed": family_balance_passed and dialect_balance_passed,
        "mode": "explicit_balanced_family_view" if use_explicit_balanced_view else "raw_corpus_view",
        "explicit_family_counts": {family: explicit_counts[family] for family in FAMILIES},
        "records": total,
        "family_counts": dict(family_counts),
        "family_ratio_max_to_min": family_ratio,
        "dialect_counts": dict(dialect_counts),
        "dialect_delta": round(dialect_delta, 4),
        "family_balance_passed": family_balance_passed,
        "dialect_balance_passed": dialect_balance_passed,
    }
    family_matrix = {
        "gate": "family_confusion_matrix_builder",
        "passed": matrix_passed,
        "mode": "explicit_balanced_family_view" if use_explicit_balanced_view else "raw_corpus_view",
        "matrix": matrix,
        "diagonal_rate": diagonal_rate,
        "interpretation": "heuristic corpus dry-run; not model evaluation",
    }
    return curriculum, family_matrix


def validate_heldout_shadow(split_path: Path) -> dict[str, Any]:
    if not split_path.exists():
        return {"gate": "heldout_shadow_canary_manifest_validator", "passed": False, "reason": "missing split"}
    split = _load_json(split_path)
    required_reports = [
        ROOT / "artifacts/reports/phase27_25_heldout_generation_canary_report.json",
        ROOT / "artifacts/reports/phase27_30_fresh_mixed_shadow_canary_report.json",
        ROOT / "artifacts/reports/phase27_60_broader_natural_dialogue_canary_report.json",
    ]
    existing = [_rel(p) for p in required_reports if p.exists()]
    passed = (
        split.get("method") == "sha256_bucket"
        and split.get("counts", {}).get("eval", 0) >= 100
        and {"msa", "saudi"} <= set(split.get("dialects", {}).get("eval", {}))
        and len(existing) == len(required_reports)
    )
    return {
        "gate": "heldout_shadow_canary_manifest_validator",
        "passed": passed,
        "split": _rel(split_path),
        "method": split.get("method"),
        "counts": split.get("counts", {}),
        "eval_dialects": split.get("dialects", {}).get("eval", {}),
        "canary_reports_present": existing,
    }


def validate_operator_contamination(records: list[dict[str, Any]]) -> dict[str, Any]:
    hits: list[dict[str, Any]] = []
    for item in records:
        text = _text(item)
        lowered = text.lower()
        matched = [term for term in OPERATOR_TERMS if term in lowered]
        if matched:
            hits.append({"file": item["_file"], "line": item["_line"], "terms": matched})
    return {
        "gate": "operator_contamination_regression_scan",
        "passed": len(hits) == 0,
        "hit_count": len(hits),
        "sample_hits": hits[:20],
        "blocked_terms": list(OPERATOR_TERMS),
    }


def build_report(source: dict[str, Any], records: list[dict[str, Any]], split_path: Path) -> dict[str, Any]:
    objective = validate_objective_spec(source)
    decoding = validate_decoding_policy(source)
    curriculum, family_matrix = validate_curriculum_and_family_matrix(records)
    heldout = validate_heldout_shadow(split_path)
    operator = validate_operator_contamination(records)
    gates = [objective, curriculum, decoding, heldout, family_matrix, operator]
    passed = all(g["passed"] for g in gates)

    decision = {
        "decision_id": "PHASE27_80_REPAIR_GATE_VALIDATION_DECISION",
        "engineering_decision": (
            "GATES_PASSED_REPAIR_IMPLEMENTATION_ALLOWED_NO_TRAINING"
            if passed
            else "GATES_FAILED_REPAIR_IMPLEMENTATION_BLOCKED"
        ),
        "all_gates_passed": passed,
        "new_training_allowed": False,
        "tokenizer_retrain_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_justified_transition": False,
        "next_phase": (
            "Phase 27.81 — SF-native Repair Implementation Plan"
            if passed
            else "Phase 27.80 remediation — fix failed gates"
        ),
        "why_no_training_yet": (
            "Phase 27.80 validates gates only. Training remains a separate decision after "
            "repair implementation artifacts are encoded."
        ),
    }
    return {
        "phase": "Phase 27.80",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_80_GATES_PASSED_NO_TRAINING"
            if passed
            else "PHASE27_80_GATES_FAILED_NO_TRAINING"
        ),
        "source_report": _rel(DEFAULT_SOURCE),
        "training_started": False,
        "tokenizer_training_started": False,
        "runtime_changed": False,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "gates": gates,
        "allowed_actions": [
            "write objective/curriculum/decoding config artifacts",
            "prepare repair implementation plan",
            "run additional dry-run validation",
        ],
        "blocked_actions": [
            "LM training",
            "tokenizer retraining",
            "runtime release",
            "SF-50M transition",
            "pretrained/open-weight model usage",
            "template masking",
        ],
        "decision": decision,
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.80 — Repair Gate Encoding and Dry-Run Validation",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة gates فقط. لم يبدأ تدريب، ولم يتغير runtime، ولا يوجد أي",
        "مسار pretrained/open-weight.",
        "",
        f"- status: `{report['status']}`",
        f"- sovereignty mode: `{report['sovereignty_mode']}`",
        f"- decision id: `{decision['decision_id']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- all gates passed: `{decision['all_gates_passed']}`",
        f"- next phase: `{decision['next_phase']}`",
        "",
        "## Gate Results",
        "",
    ]
    for gate in report["gates"]:
        lines.append(f"- `{gate['gate']}`: passed=`{gate['passed']}`")
    lines.extend(["", "## Corpus Dry-Run", ""])
    curriculum = next(g for g in report["gates"] if g["gate"] == "curriculum_family_balance_dry_run")
    lines.append(f"- records: `{curriculum['records']}`")
    lines.append(f"- dialect counts: `{curriculum['dialect_counts']}`")
    lines.append(f"- family counts: `{curriculum['family_counts']}`")
    lines.append(f"- family ratio max/min: `{curriculum['family_ratio_max_to_min']}`")
    matrix = next(g for g in report["gates"] if g["gate"] == "family_confusion_matrix_builder")
    lines.append(f"- family diagonal rate: `{matrix['diagonal_rate']}`")
    operator = next(g for g in report["gates"] if g["gate"] == "operator_contamination_regression_scan")
    lines.append(f"- operator contamination hits: `{operator['hit_count']}`")
    lines.extend(["", "## Blocked Actions", ""])
    for item in report["blocked_actions"]:
        lines.append(f"- {item}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        source = _load_source(args.source)
        records = _iter_records(args.corpus)
        if not records:
            raise ValueError("empty corpus dry-run input")
        report = build_report(source, records, args.split)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.write_text(
        json.dumps(report["decision"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_doc(args.doc, report)

    print("SF.AI — Phase 27.80 repair gate validation")
    print(f"status: {report['status']}")
    print(f"all_gates_passed: {report['decision']['all_gates_passed']}")
    print(f"report: {_rel(args.report)}")
    print(f"decision: {_rel(args.decision)}")
    print(f"doc: {_rel(args.doc)}")
    return 0 if report["decision"]["all_gates_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
