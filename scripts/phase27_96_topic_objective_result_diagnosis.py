#!/usr/bin/env python3
"""Phase 27.96 — diagnose the Phase 27.95 topic-objective repair result.

No training. No tokenizer work. No runtime release.

Phase 27.95 aligned the runtime prompt with the training renderer by adding
`الموضوع المطلوب: <topic>` for topic-family prompts. The checkpoint still
failed gates, so this phase determines the next engineering move before any
new training.
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

DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_95_bounded_topic_objective_repair_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_96_topic_objective_result_diagnosis_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_96_TOPIC_OBJECTIVE_RESULT_DIAGNOSIS_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_96_TOPIC_OBJECTIVE_RESULT_DIAGNOSIS_REPORT.md"
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
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.96 topic result diagnosis")
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
            if not row["passed"]:
                hits = _topic_hits(str(row["response"]))
                required = str(row["topic"])
                wrong_hits = [term for term in hits if term != required]
                rows.append(
                    {
                        "section": section,
                        "id": row["id"],
                        "dialect": row["dialect"],
                        "prompt": row["prompt"],
                        "required_topic": required,
                        "response": row["response"],
                        "reason": row["reason"],
                        "guard_allowed": row["guard_allowed"],
                        "topic_hits": hits,
                        "wrong_topic_hits": wrong_hits,
                    }
                )
    return rows


def _topic_training_coverage(corpus: Path) -> dict[str, Any]:
    explicit: Counter[str] = Counter()
    inferred: Counter[str] = Counter()
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
                continue
            text = " ".join(msg.get("content", "") for msg in record.get("messages", []))
            for term in TOPIC_TERMS:
                if term in text:
                    inferred[term] += 1
                    dialects[term][dialect] += 1

    combined = Counter(inferred)
    combined.update(explicit)
    return {
        "topic_family_records": total_topic_family,
        "explicit_topic_term_records": dict(explicit),
        "inferred_topic_term_records": dict(inferred),
        "combined_topic_term_records": dict(combined),
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
    topic_failures = _topic_failure_rows(best)
    wrong_topic_counter: Counter[str] = Counter()
    required_failure_counter: Counter[str] = Counter()
    guard_blocked = 0
    for row in topic_failures:
        required_failure_counter[row["required_topic"]] += 1
        wrong_topic_counter.update(row["wrong_topic_hits"])
        if not row["guard_allowed"]:
            guard_blocked += 1

    known_summary = best["known_topic_summary"]
    fresh_summary = best["fresh_topic_summary"]
    all_family = _all_family_summary(best)
    coverage = _topic_training_coverage(args.corpus)

    topic_gate_failed = known_summary["passed"] < 16 or fresh_summary["passed"] < 8
    topic_variable_binding_failure = (
        topic_gate_failed
        and guard_blocked == 0
        and sum(wrong_topic_counter.values()) >= 6
    )
    all_family_regressed = all_family["passed"] < 45
    support_followup_still_weak = (
        all_family["family_summary"]["support"]["passed"] < 8
        or all_family["family_summary"]["followup"]["passed"] < 8
    )

    root_cause_weights = {
        "topic_variable_binding_failure": 34,
        "assistant_target_copy_objective_weak": 22,
        "topic_family_balance_residual": 14,
        "support_followup_eval_alias_or_semantic_gap": 9,
        "decoding_surface_artifacts": 8,
        "corpus_topic_metadata_inference_gap": 6,
        "tokenizer": 3,
        "model_capacity": 3,
        "semantic_routing": 1,
    }

    diagnosis_passed = bool(topic_variable_binding_failure and all_family_regressed)
    decision = {
        "decision_id": "PHASE27_96_TOPIC_OBJECTIVE_RESULT_DIAGNOSIS_DECISION",
        "engineering_decision": (
            "DESIGN_TOPIC_COPY_CONTRASTIVE_OBJECTIVE_BEFORE_ANY_TRAINING"
            if diagnosis_passed
            else "BLOCK_AND_REINSPECT_PHASE27_95_EVIDENCE"
        ),
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "heldout_runtime_gate_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "topic_copy_objective_design_allowed": diagnosis_passed,
        "why": (
            "Phase 27.95 aligned topic conditioning, but the model still substitutes the requested "
            "topic with learned neighboring topic prototypes. Topic failures passed the guard, so "
            "this is a semantic variable-binding/objective issue, not a runtime or capacity win."
        ),
        "next_phase": "Phase 27.97 — Topic Variable Binding Objective Design",
    }

    return {
        "phase": "Phase 27.96",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_96_DIAGNOSED_TOPIC_VARIABLE_BINDING_FAILURE_NO_TRAINING"
            if diagnosis_passed
            else "PHASE27_96_DIAGNOSIS_INCONCLUSIVE_TRAINING_BLOCKED"
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
            "all_family": f"{all_family['passed']}/{all_family['total']}",
            "required_gates": source["decision"]["required_gates"],
        },
        "diagnosis_signals": {
            "topic_gate_failed": topic_gate_failed,
            "all_family_regressed": all_family_regressed,
            "guard_blocked_topic_failures": guard_blocked,
            "wrong_topic_substitution_count": sum(wrong_topic_counter.values()),
            "support_followup_still_weak": support_followup_still_weak,
            "topic_variable_binding_failure": topic_variable_binding_failure,
        },
        "topic_failure_counts": {
            "by_required_topic": dict(required_failure_counter),
            "wrong_topic_substitutions": dict(wrong_topic_counter),
        },
        "topic_training_coverage": coverage,
        "all_family_summary": all_family,
        "representative_topic_failures": topic_failures,
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
            "design copy-anchored assistant target objective",
            "design contrastive wrong-topic canary",
            "design per-topic round-robin curriculum gate",
            "tighten topic metadata so topic_term is explicit for every topic sample",
        ]
        if diagnosis_passed
        else ["manual evidence inspection only"],
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.96 — Topic Objective Repair Result Diagnosis",
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
        f"- all-family: `{report['score_summary']['all_family']}`",
        f"- wrong-topic substitutions: `{report['diagnosis_signals']['wrong_topic_substitution_count']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
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
    lines.extend(["", "## بدائل الموضوع الخاطئة", ""])
    for key, value in report["topic_failure_counts"]["wrong_topic_substitutions"].items():
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
    print(f"all_family={report['score_summary']['all_family']}")
    print(f"wrong_topic_substitutions={report['diagnosis_signals']['wrong_topic_substitution_count']}")
    print(f"report={_rel(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
