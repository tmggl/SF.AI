#!/usr/bin/env python3
"""Phase 27.102 — Topic Prototype Contrastive Copy-Anchor Gate.

No training. No tokenizer work. No runtime release.

This phase turns the Phase 27.101 diagnosis into an executable gate:
- count observed wrong-topic substitutions from response text, not reason only;
- require copy-anchor and observed wrong-topic checks together;
- write a stricter canary/spec for the next no-training curriculum pack.
"""
# ruff: noqa: E402

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_26_heldout_objective_repair import _rel
from scripts.phase27_58_tokenizer_bounded_alignment_probe import _surface

DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_101_topic_binding_result_diagnosis_report.json"
DEFAULT_TRAINING_REPORT = ROOT / "artifacts/reports/phase27_100_bounded_topic_binding_repair_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_102_topic_prototype_contrastive_gate_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_102_TOPIC_PROTOTYPE_CONTRASTIVE_GATE_DECISION.json"
DEFAULT_SPEC = ROOT / "artifacts/reports/phase27_102_topic_prototype_contrastive_gate_spec.json"
DEFAULT_CANARY = ROOT / "eval/prompts/phase27_102_topic_prototype_contrastive_canary.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_102_TOPIC_PROTOTYPE_CONTRASTIVE_GATE_REPORT.md"

TARGET_TERMS: tuple[str, ...] = (
    "الوفاء",
    "التعاون",
    "الصبر",
    "الاحترام",
    "الهدوء",
    "الصدق",
    "الصداقة",
    "الشجاعة",
)
PROTOTYPE_DECOYS: tuple[str, ...] = ("الصداقة", "الامتنان")
ALL_TOPIC_TERMS: tuple[str, ...] = tuple(dict.fromkeys((*TARGET_TERMS, *PROTOTYPE_DECOYS)))
TARGET_DIALECTS: tuple[str, ...] = ("msa", "saudi")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.102 topic prototype contrastive gate")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--training-report", type=Path, default=DEFAULT_TRAINING_REPORT)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    p.add_argument("--canary", type=Path, default=DEFAULT_CANARY)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args(argv)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _best_checkpoint(training_report: dict[str, Any]) -> dict[str, Any]:
    name = training_report["decision"]["best_checkpoint"]
    return next(row for row in training_report["checkpoints"] if row["checkpoint"] == name)


def _topic_hits(text: str, terms: tuple[str, ...] = ALL_TOPIC_TERMS) -> list[str]:
    surface = _surface(text)
    return [term for term in terms if _surface(term) in surface]


def _observed_wrong_topics(row: dict[str, Any]) -> list[str]:
    required = str(row["topic"])
    return [term for term in _topic_hits(str(row["response"])) if term != required]


def _copy_anchor_ok(text: str, topic: str, max_visible_arabic_chars: int = 12) -> bool:
    compact_text = "".join(_surface(text).split())
    compact_topic = "".join(_surface(topic).split())
    if not compact_topic:
        return False
    idx = compact_text.find(compact_topic)
    return idx != -1 and idx <= max_visible_arabic_chars


def _evaluate_legacy_result(training_report: dict[str, Any]) -> dict[str, Any]:
    best = _best_checkpoint(training_report)
    topic_rows = [*best["known_topic_rows"], *best["fresh_topic_rows"]]
    observed_wrong_rows: list[dict[str, Any]] = []
    copy_anchor_failures: list[dict[str, Any]] = []
    wrong_counter: Counter[str] = Counter()

    for row in topic_rows:
        wrong = _observed_wrong_topics(row)
        wrong_counter.update(wrong)
        if wrong:
            observed_wrong_rows.append(
                {
                    "id": row["id"],
                    "set": row["set"],
                    "dialect": row["dialect"],
                    "required_topic": row["topic"],
                    "observed_wrong_topics": wrong,
                    "response": row["response"],
                    "legacy_reason": row["reason"],
                }
            )
        if not _copy_anchor_ok(str(row["response"]), str(row["topic"])):
            copy_anchor_failures.append(
                {
                    "id": row["id"],
                    "set": row["set"],
                    "dialect": row["dialect"],
                    "required_topic": row["topic"],
                    "response": row["response"],
                    "legacy_reason": row["reason"],
                }
            )

    reported_wrong = int(training_report["decision"]["wrong_topic_count"])
    observed_wrong = sum(wrong_counter.values())
    return {
        "best_checkpoint": best["checkpoint"],
        "topic_rows_total": len(topic_rows),
        "reported_wrong_topic_count": reported_wrong,
        "observed_wrong_topic_count": observed_wrong,
        "metric_blind_spot_detected": observed_wrong > reported_wrong,
        "observed_wrong_topic_substitutions": dict(wrong_counter),
        "observed_wrong_rows": observed_wrong_rows,
        "copy_anchor_passed": len(topic_rows) - len(copy_anchor_failures),
        "copy_anchor_total": len(topic_rows),
        "copy_anchor_failures": copy_anchor_failures,
        "known_topic": training_report["decision"]["known_topic"],
        "fresh_topic": training_report["decision"]["fresh_topic"],
        "topic_family": training_report["decision"]["topic_family"],
        "all_family": training_report["decision"]["all_family"],
    }


def _prototype_forbidden_terms(topic: str) -> list[str]:
    terms = [term for term in ALL_TOPIC_TERMS if term != topic]
    # Keep the prototype traps early in the list so reports stay readable.
    return sorted(terms, key=lambda item: (item not in PROTOTYPE_DECOYS, item))


def _build_canary() -> dict[str, Any]:
    prompts: list[dict[str, Any]] = []
    for topic in TARGET_TERMS:
        for dialect in TARGET_DIALECTS:
            is_saudi = dialect == "saudi"
            prompt_decoy = "الامتنان" if topic == "الصداقة" else "الصداقة"
            prompt = (
                f"وش يعني {topic} بجملة وحدة بدون ذكر {prompt_decoy}؟"
                if is_saudi
                else f"عرّف {topic} بجملة واحدة دون ذكر {prompt_decoy}."
            )
            prompts.append(
                {
                    "id": f"prototype_guard_{dialect}_{topic}",
                    "set": "prototype_contrastive",
                    "dialect": dialect,
                    "dialogue_family": "topic",
                    "message": prompt,
                    "requested_topic": topic,
                    "required_terms": [topic],
                    "forbidden_terms": _prototype_forbidden_terms(topic),
                    "prototype_decoys": list(PROTOTYPE_DECOYS),
                    "copy_anchor_required": True,
                    "copy_anchor_max_visible_arabic_chars": 12,
                    "observed_wrong_topic_max": 0,
                    "max_sentences": 1,
                }
            )
    return {
        "suite_id": "phase27_102_topic_prototype_contrastive_canary",
        "phase": "Phase 27.102",
        "objective": "topic_prototype_contrastive_copy_anchor_gate_v1",
        "language_track": ["msa", "saudi"],
        "target_terms": list(TARGET_TERMS),
        "prototype_decoys": list(PROTOTYPE_DECOYS),
        "thresholds": {
            "observed_wrong_topic_max": 0,
            "copy_anchor_min": "16/16",
            "topic_required_min": "16/16",
            "malformed_max": 0,
            "repeated_phrase_max": 0,
        },
        "coverage": {
            "prompt_count": len(prompts),
            "dialects": list(TARGET_DIALECTS),
            "terms_per_dialect": len(TARGET_TERMS),
            "all_terms_covered": True,
            "prototype_decoy_covered": True,
        },
        "prompts": prompts,
    }


def _build_spec() -> dict[str, Any]:
    return {
        "spec_id": "phase27_102_topic_prototype_contrastive_copy_anchor_gate_spec",
        "phase": "Phase 27.102",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "purpose": (
            "Make topic binding evaluation count observed wrong-topic substitutions from "
            "response text before any future topic repair training."
        ),
        "metric_rules": {
            "observed_wrong_topic_count": (
                "Count every topic/prototype term present in the assistant response except "
                "the requested topic, independent of the primary failure reason."
            ),
            "copy_anchor": "Requested topic must appear within the first 12 visible Arabic chars.",
            "reason_precedence": (
                "wrong_topic and copy_anchor are independent gates; required_topic_missing "
                "must not hide a wrong-topic substitution."
            ),
        },
        "thresholds": {
            "observed_wrong_topic_count": 0,
            "copy_anchor": "all",
            "topic_required": "all",
            "known_topic": "16/16",
            "fresh_topic": "8/10",
            "topic_family": "8/10",
            "all_family": "45/50",
        },
        "blocked_actions_until_gate_passes": [
            "new LM training",
            "runtime release",
            "UI generator release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
            "template masking",
        ],
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    source = _load_json(args.source)
    training_report = _load_json(args.training_report)
    decision_source = source["decision"]

    if decision_source["engineering_decision"] != (
        "DESIGN_TOPIC_PROTOTYPE_CONTRASTIVE_COPY_ANCHOR_GATE_BEFORE_ANY_TRAINING"
    ):
        raise ValueError("Phase 27.101 did not allow Phase 27.102 gate design")

    legacy = _evaluate_legacy_result(training_report)
    canary = _build_canary()
    spec = _build_spec()

    gate_encoded = (
        legacy["metric_blind_spot_detected"]
        and legacy["observed_wrong_topic_count"] == 8
        and legacy["copy_anchor_passed"] == 18
        and canary["coverage"]["prompt_count"] == 16
        and spec["thresholds"]["observed_wrong_topic_count"] == 0
    )
    decision = {
        "decision_id": "PHASE27_102_TOPIC_PROTOTYPE_CONTRASTIVE_GATE_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_103_TOPIC_PROTOTYPE_CONTRASTIVE_CURRICULUM_PACK_NO_TRAINING"
            if gate_encoded
            else "BLOCK_AND_REINSPECT_TOPIC_PROTOTYPE_GATE_ENCODING"
        ),
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "heldout_runtime_gate_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "curriculum_pack_allowed": gate_encoded,
        "why": (
            "The executable gate now catches the Phase 27.100 metric blind spot: reported "
            "wrong-topic was 0, but observed wrong-topic is 8. Future topic repair must pass "
            "observed wrong-topic=0 and copy-anchor gates before any runtime or scaling decision."
        ),
        "next_phase": "Phase 27.103 — Topic Prototype Contrastive Curriculum Pack",
    }
    return {
        "phase": "Phase 27.102",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_102_GATE_ENCODED_CURRICULUM_PACK_ALLOWED_NO_TRAINING"
            if gate_encoded
            else "PHASE27_102_GATE_ENCODING_BLOCKED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "source_report": _rel(args.source),
        "training_report": _rel(args.training_report),
        "legacy_result_probe": legacy,
        "gate_spec": spec,
        "canary": canary,
        "blocked_actions": spec["blocked_actions_until_gate_passes"],
        "allowed_next_actions": [
            "author a no-training topic prototype contrastive curriculum pack",
            "add rows that force requested-topic copy-anchor before prototype terms",
            "rerun gate before bounded training is allowed",
        ]
        if gate_encoded
        else ["manual gate evidence inspection only"],
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    legacy = report["legacy_result_probe"]
    lines = [
        "# Phase 27.102 — Topic Prototype Contrastive Copy-Anchor Gate",
        "",
        "## الخلاصة",
        "",
        "هذه بوابة ترميز/تصميم فقط. لا تدريب ولا runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- reported wrong-topic: `{legacy['reported_wrong_topic_count']}`",
        f"- observed wrong-topic: `{legacy['observed_wrong_topic_count']}`",
        f"- copy-anchor: `{legacy['copy_anchor_passed']}/{legacy['copy_anchor_total']}`",
        f"- canary prompts: `{report['canary']['coverage']['prompt_count']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- training allowed: `{decision['new_training_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## القرار",
        "",
        decision["why"],
        "",
        "## البوابة الجديدة",
        "",
        "- counted metric: `observed_wrong_topic_count` من نص الرد مباشرة.",
        "- threshold: `observed_wrong_topic_count == 0`.",
        "- copy-anchor: الموضوع المطلوب داخل أول 12 حرفًا عربيًا ظاهرًا.",
        "- لا يسمح `required_topic_missing` بإخفاء wrong-topic substitution.",
        "",
        "## بدائل الموضوع المرصودة في 27.100",
        "",
    ]
    for term, count in legacy["observed_wrong_topic_substitutions"].items():
        lines.append(f"- `{term}`: `{count}`")
    lines.extend(["", "## المحظور", ""])
    for item in report["blocked_actions"]:
        lines.append(f"- {item}")
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
    except (FileNotFoundError, json.JSONDecodeError, KeyError, StopIteration, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.decision.write_text(
        json.dumps(report["decision"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    args.spec.parent.mkdir(parents=True, exist_ok=True)
    args.spec.write_text(json.dumps(report["gate_spec"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.canary.parent.mkdir(parents=True, exist_ok=True)
    args.canary.write_text(json.dumps(report["canary"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_doc(args.doc, report)

    legacy = report["legacy_result_probe"]
    print(report["status"])
    print(report["decision"]["engineering_decision"])
    print(f"reported_wrong_topic={legacy['reported_wrong_topic_count']}")
    print(f"observed_wrong_topic={legacy['observed_wrong_topic_count']}")
    print(f"copy_anchor={legacy['copy_anchor_passed']}/{legacy['copy_anchor_total']}")
    print(f"canary_prompts={report['canary']['coverage']['prompt_count']}")
    print(f"report={_rel(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
