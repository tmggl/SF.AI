#!/usr/bin/env python3
"""Phase 27.101 — diagnose the Phase 27.100 topic-binding repair result.

No training. No tokenizer work. No runtime release.

Phase 27.100 removed wrong-topic leakage but still failed copy-anchor and
fresh-topic gates. This phase turns that evidence into an engineering
decision before any new training is allowed.
"""
# ruff: noqa: E402

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_26_heldout_objective_repair import _rel
from scripts.phase27_58_tokenizer_bounded_alignment_probe import _surface

DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_100_bounded_topic_binding_repair_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_101_topic_binding_result_diagnosis_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_101_TOPIC_BINDING_RESULT_DIAGNOSIS_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_101_TOPIC_BINDING_RESULT_DIAGNOSIS_REPORT.md"
DEFAULT_CORPUS = ROOT / "data/corpus/chat/jsonl"

TOPIC_TERMS: tuple[str, ...] = (
    "الوفاء",
    "التعاون",
    "الصبر",
    "الاحترام",
    "الهدوء",
    "الصدق",
    "الصداقة",
    "الشجاعة",
    "الامتنان",
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.101 topic-binding result diagnosis")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args(argv)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _best_checkpoint(source: dict[str, Any]) -> dict[str, Any]:
    name = source["decision"]["best_checkpoint"]
    return next(row for row in source["checkpoints"] if row["checkpoint"] == name)


def _topic_hits(text: str) -> list[str]:
    surface = _surface(text)
    return [term for term in TOPIC_TERMS if _surface(term) in surface]


def _topic_failure_rows(best: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for section in ("known_topic_rows", "fresh_topic_rows"):
        for row in best[section]:
            if row["passed"]:
                continue
            hits = _topic_hits(str(row["response"]))
            required = str(row["topic"])
            wrong_hits = [term for term in hits if term != required]
            rows.append(
                {
                    "section": section,
                    "id": row["id"],
                    "set": row["set"],
                    "dialect": row["dialect"],
                    "prompt": row["prompt"],
                    "required_topic": required,
                    "response": row["response"],
                    "reason": row["reason"],
                    "guard_allowed": row["guard_allowed"],
                    "topic_ok": row["topic_ok"],
                    "copy_anchor_ok": row["copy_anchor_ok"],
                    "topic_hits": hits,
                    "wrong_topic_hits": wrong_hits,
                }
            )
    return rows


def _all_family_failures(best: dict[str, Any]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for row in best["all_family"]["rows"]:
        if row["passed"]:
            continue
        failures.append(
            {
                "id": row["id"],
                "family": row["family"],
                "dialect": row["dialect"],
                "prompt": row["prompt"],
                "topic": row.get("topic", ""),
                "response": row["response"],
                "reason": row["reason"],
                "guard_allowed": row["guard_allowed"],
                "expected_ok": row["expected_ok"],
                "family_ok": row["family_ok"],
            }
        )
    return failures


def _topic_training_coverage(corpus: Path) -> dict[str, Any]:
    explicit: Counter[str] = Counter()
    dialects: dict[str, Counter[str]] = defaultdict(Counter)
    total_topic_family = 0

    for path in sorted(corpus.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            provenance = record.get("provenance", {})
            family_values = {
                provenance.get("dialogue_family"),
                provenance.get("prompt_family"),
                provenance.get("answer_family"),
            }
            if "topic" not in family_values:
                continue
            total_topic_family += 1
            dialect = provenance.get("dialect") or record.get("dialect") or "unknown"
            explicit_term = (provenance.get("topic_term") or "").strip()
            if explicit_term:
                explicit[explicit_term] += 1
                dialects[explicit_term][dialect] += 1

    return {
        "topic_family_records": total_topic_family,
        "explicit_topic_term_records": dict(explicit),
        "dialects_by_topic": {topic: dict(counts) for topic, counts in dialects.items()},
    }


def _all_family_summary(best: dict[str, Any]) -> dict[str, Any]:
    summary = best["all_family"]["summary"]
    return {
        "passed": summary["passed"],
        "total": summary["total"],
        "family_summary": summary["family_summary"],
        "reason_counts": summary["reason_counts"],
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    source = _load_json(args.source)
    best = _best_checkpoint(source)
    decision_source = source["decision"]
    topic_failures = _topic_failure_rows(best)
    all_family_failures = _all_family_failures(best)
    coverage = _topic_training_coverage(args.corpus)

    wrong_topic_counter: Counter[str] = Counter()
    required_failure_counter: Counter[str] = Counter()
    response_topic_counter: Counter[str] = Counter()
    reason_counter: Counter[str] = Counter()
    section_counter: Counter[str] = Counter()
    dialect_counter: Counter[str] = Counter()
    guard_blocked = 0
    for row in topic_failures:
        required_failure_counter[row["required_topic"]] += 1
        response_topic_counter.update(row["topic_hits"])
        wrong_topic_counter.update(row["wrong_topic_hits"])
        reason_counter[str(row["reason"])] += 1
        section_counter[str(row["section"])] += 1
        dialect_counter[str(row["dialect"])] += 1
        if not row["guard_allowed"]:
            guard_blocked += 1

    known_summary = best["known_topic_summary"]
    fresh_summary = best["fresh_topic_summary"]
    all_family = _all_family_summary(best)
    copy_anchor_total = len([*best["known_topic_rows"], *best["fresh_topic_rows"]])
    copy_anchor_pass = sum(
        1
        for row in [*best["known_topic_rows"], *best["fresh_topic_rows"]]
        if row["copy_anchor_ok"]
    )
    all_family_failure_counts = Counter(row["family"] for row in all_family_failures)

    known_gate_failed = known_summary["passed"] < 16
    fresh_gate_failed = fresh_summary["passed"] < 8
    copy_anchor_gate_failed = copy_anchor_pass < copy_anchor_total
    all_family_gate_failed = all_family["passed"] < 45
    observed_wrong_topic_count = sum(wrong_topic_counter.values())
    reported_wrong_topic_count = int(decision_source["wrong_topic_count"])
    wrong_topic_metric_blind_spot = observed_wrong_topic_count > reported_wrong_topic_count
    prototype_attraction = response_topic_counter.get("الصداقة", 0) >= 5
    fresh_generalization_gap = fresh_summary["passed"] <= 5
    topic_family_gap = all_family["family_summary"]["topic"]["passed"] < 8
    support_surface_gap = all_family["family_summary"]["support"]["passed"] < 8
    open_social_surface_gap = all_family["family_summary"]["open_social"]["passed"] < 8

    root_cause_weights = {
        "copy_anchor_objective_underpowered": 28,
        "topic_prototype_attraction": 20,
        "fresh_topic_generalization_gap": 16,
        "topic_curriculum_term_balance": 12,
        "assistant_target_prefix_format_weak": 9,
        "decoding_surface_artifacts": 6,
        "support_open_social_secondary_regression": 4,
        "tokenizer": 2,
        "model_capacity": 2,
        "semantic_routing": 1,
    }

    diagnosis_passed = bool(
        copy_anchor_gate_failed
        and fresh_gate_failed
        and prototype_attraction
        and topic_family_gap
        and all_family_gate_failed
    )
    decision = {
        "decision_id": "PHASE27_101_TOPIC_BINDING_RESULT_DIAGNOSIS_DECISION",
        "engineering_decision": (
            "DESIGN_TOPIC_PROTOTYPE_CONTRASTIVE_COPY_ANCHOR_GATE_BEFORE_ANY_TRAINING"
            if diagnosis_passed
            else "BLOCK_AND_REINSPECT_PHASE27_100_EVIDENCE"
        ),
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "heldout_runtime_gate_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "topic_prototype_contrastive_design_allowed": diagnosis_passed,
        "why": (
            "Phase 27.100 improved topic binding but did not truly eliminate wrong-topic behavior. "
            "The report counted wrong-topic as zero through reason precedence, while direct response "
            "inspection finds prototype substitutions, mostly الصداقة. The best checkpoint misses "
            "copy-anchor on 8/26 contrastive cases, fresh-topic generalization remains 5/10, and "
            "topic-family is 6/10. This is an objective/evaluation/curriculum binding weakness, "
            "not evidence for SF-50M yet."
        ),
        "next_phase": "Phase 27.102 — Topic Prototype Contrastive Copy-Anchor Gate",
    }

    return {
        "phase": "Phase 27.101",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_101_DIAGNOSED_COPY_ANCHOR_CURRICULUM_GAP_NO_TRAINING"
            if diagnosis_passed
            else "PHASE27_101_DIAGNOSIS_INCONCLUSIVE_TRAINING_BLOCKED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "source_report": _rel(args.source),
        "best_checkpoint": best["checkpoint"],
        "score_summary": {
            "known_topic": f"{known_summary['passed']}/{known_summary['total']}",
            "fresh_topic": f"{fresh_summary['passed']}/{fresh_summary['total']}",
            "copy_anchor": f"{copy_anchor_pass}/{copy_anchor_total}",
            "reported_wrong_topic_count": reported_wrong_topic_count,
            "observed_wrong_topic_count": observed_wrong_topic_count,
            "topic_family": decision_source["topic_family"],
            "all_family": f"{all_family['passed']}/{all_family['total']}",
            "required_gates": decision_source["required_gates"],
        },
        "diagnosis_signals": {
            "known_gate_failed": known_gate_failed,
            "fresh_gate_failed": fresh_gate_failed,
            "copy_anchor_gate_failed": copy_anchor_gate_failed,
            "wrong_topic_metric_blind_spot": wrong_topic_metric_blind_spot,
            "reported_wrong_topic_count": reported_wrong_topic_count,
            "observed_wrong_topic_count": observed_wrong_topic_count,
            "topic_prototype_attraction": prototype_attraction,
            "fresh_generalization_gap": fresh_generalization_gap,
            "topic_family_gap": topic_family_gap,
            "all_family_gate_failed": all_family_gate_failed,
            "support_surface_gap": support_surface_gap,
            "open_social_surface_gap": open_social_surface_gap,
            "guard_blocked_topic_failures": guard_blocked,
        },
        "topic_failure_counts": {
            "by_required_topic": dict(required_failure_counter),
            "response_topic_hits": dict(response_topic_counter),
            "wrong_topic_substitutions": dict(wrong_topic_counter),
            "by_reason": dict(reason_counter),
            "by_section": dict(section_counter),
            "by_dialect": dict(dialect_counter),
        },
        "topic_training_coverage": coverage,
        "all_family_summary": all_family,
        "all_family_failure_counts": dict(all_family_failure_counts),
        "representative_topic_failures": topic_failures,
        "representative_all_family_failures": all_family_failures,
        "root_cause_weights": root_cause_weights,
        "blocked_actions": [
            "new LM training",
            "runtime release",
            "UI generator release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
            "keyword/template masking",
        ],
        "allowed_next_actions": [
            "design topic-prototype contrastive copy-anchor gate",
            "fix wrong-topic metric precedence before any training",
            "require per-topic forced copy-anchor rows before training",
            "separate known/fresh topic curriculum thresholds",
            "preserve observed wrong-topic zero-leak as a non-regression gate",
            "add support/open_social secondary regression checks",
        ]
        if diagnosis_passed
        else ["manual evidence inspection only"],
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.101 — Topic Binding Repair Result Diagnosis",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تشخيص فقط. لم يبدأ تدريب جديد ولم يتغير runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- best checkpoint: `{report['best_checkpoint']}`",
        f"- known topic: `{report['score_summary']['known_topic']}`",
        f"- fresh topic: `{report['score_summary']['fresh_topic']}`",
        f"- copy-anchor: `{report['score_summary']['copy_anchor']}`",
        f"- reported wrong-topic count: `{report['score_summary']['reported_wrong_topic_count']}`",
        f"- observed wrong-topic count: `{report['score_summary']['observed_wrong_topic_count']}`",
        f"- topic-family: `{report['score_summary']['topic_family']}`",
        f"- all-family: `{report['score_summary']['all_family']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- training allowed: `{decision['new_training_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## التشخيص",
        "",
        decision["why"],
        "",
        "## إشارات التشخيص",
        "",
    ]
    for key, value in report["diagnosis_signals"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## أوزان السبب الجذري", ""])
    for key, value in report["root_cause_weights"].items():
        lines.append(f"- `{key}`: `{value}%`")
    lines.extend(["", "## إخفاقات الموضوع", ""])
    for key, value in report["topic_failure_counts"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## القرار", ""])
    for item in report["blocked_actions"]:
        lines.append(f"- ممنوع: {item}")
    lines.extend(["", "## المسموح تاليًا", ""])
    for item in report["allowed_next_actions"]:
        lines.append(f"- {item}")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        report = build_report(args)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, StopIteration) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.decision.write_text(
        json.dumps(report["decision"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_doc(args.doc, report)
    print(report["status"])
    print(report["decision"]["engineering_decision"])
    print(f"known_topic={report['score_summary']['known_topic']}")
    print(f"fresh_topic={report['score_summary']['fresh_topic']}")
    print(f"copy_anchor={report['score_summary']['copy_anchor']}")
    print(f"reported_wrong_topic_count={report['score_summary']['reported_wrong_topic_count']}")
    print(f"observed_wrong_topic_count={report['score_summary']['observed_wrong_topic_count']}")
    print(f"all_family={report['score_summary']['all_family']}")
    print(f"report={_rel(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
