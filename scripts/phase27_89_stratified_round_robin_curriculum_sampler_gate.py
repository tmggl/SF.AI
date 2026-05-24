#!/usr/bin/env python3
"""Phase 27.89 — stratified round-robin curriculum sampler gate.

No training. No runtime release. This gate verifies that the new
family_round_robin split order fixes the sequential family blocks diagnosed in
Phase 27.88 before any bounded SF-10M repair is allowed.
"""

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

from sf_ai.datasets import ChatDataset  # noqa: E402
from sf_ai.datasets.chat_dataset import FAMILY_CONDITION_LABELS  # noqa: E402
from sf_ai.training.train_tiny_lm import _iter_training_texts  # noqa: E402

DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_88_family_conditioned_training_result_diagnosis_report.json"
DEFAULT_CORPUS = ROOT / "data/corpus/chat/jsonl"
DEFAULT_SPLIT = ROOT / "data/corpus/chat/splits/dialogue_split_v1.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_89_stratified_round_robin_curriculum_sampler_gate_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_89_STRATIFIED_ROUND_ROBIN_CURRICULUM_SAMPLER_GATE_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_89_STRATIFIED_ROUND_ROBIN_CURRICULUM_SAMPLER_GATE_REPORT.md"

WINDOW_SIZE = 600
LIMIT = 1800
FAMILY_KEYS = ("open_social", "followup", "planning", "support", "topic")
LABEL_TO_KEY = {label: key for key, label in FAMILY_CONDITION_LABELS.items()}
KEY_TO_LABEL = {key: label for key, label in FAMILY_CONDITION_LABELS.items()}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.89 round-robin sampler gate")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args(argv)


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _family_from_text(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("عائلة الحوار:"):
            label = line.split(":", 1)[1].strip()
            return LABEL_TO_KEY.get(label, "unknown")
    return "unknown"


def _stream_families(corpus: Path, split_manifest: Path, *, split_order: str, limit: int) -> list[str]:
    dataset = ChatDataset(corpus)
    families: list[str] = []
    for text in _iter_training_texts(
        dataset,
        stream_format="dialogue",
        split_manifest=split_manifest,
        split_name="train",
        split_order=split_order,
    ):
        families.append(_family_from_text(text))
        if len(families) >= limit:
            break
    return families


def _window_counts(families: list[str]) -> dict[str, dict[str, Any]]:
    windows: dict[str, dict[str, Any]] = {}
    for idx, start in enumerate(range(0, LIMIT, WINDOW_SIZE), start=1):
        end = start + WINDOW_SIZE
        chunk = families[start:end]
        counts = Counter(chunk)
        missing = [family for family in FAMILY_KEYS if counts.get(family, 0) == 0]
        dominant = counts.most_common(1)[0] if counts else ("none", 0)
        min_family_count = min((counts.get(family, 0) for family in FAMILY_KEYS), default=0)
        windows[f"window_{idx}"] = {
            "range": [start + 1, min(end, len(families))],
            "total": len(chunk),
            "counts": {family: counts.get(family, 0) for family in FAMILY_KEYS},
            "missing_families": missing,
            "dominant_family": dominant[0],
            "dominant_count": dominant[1],
            "dominant_share": round(dominant[1] / len(chunk), 4) if chunk else 0.0,
            "min_family_count": min_family_count,
        }
    return windows


def _assess_windows(windows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    min_per_family = 80
    max_dominant_share = 0.25
    failures: list[str] = []
    for name, window in windows.items():
        if window["total"] != WINDOW_SIZE:
            failures.append(f"{name}: expected {WINDOW_SIZE} samples, got {window['total']}")
        if window["missing_families"]:
            failures.append(f"{name}: missing {window['missing_families']}")
        if window["min_family_count"] < min_per_family:
            failures.append(
                f"{name}: min family count {window['min_family_count']} < {min_per_family}"
            )
        if window["dominant_share"] > max_dominant_share:
            failures.append(
                f"{name}: dominant share {window['dominant_share']} > {max_dominant_share}"
            )
    return {
        "passed": not failures,
        "criteria": {
            "window_size": WINDOW_SIZE,
            "required_families": list(FAMILY_KEYS),
            "min_per_family_per_window": min_per_family,
            "max_dominant_share_per_window": max_dominant_share,
        },
        "failures": failures,
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    source = _load_json(args.source)
    sequential = _stream_families(
        args.corpus,
        args.split_manifest,
        split_order="sequential",
        limit=LIMIT,
    )
    round_robin = _stream_families(
        args.corpus,
        args.split_manifest,
        split_order="family_round_robin",
        limit=LIMIT,
    )
    sequential_windows = _window_counts(sequential)
    round_robin_windows = _window_counts(round_robin)
    gate = _assess_windows(round_robin_windows)
    first_1800_counts = dict(Counter(round_robin))
    topic_count = int(first_1800_counts.get("topic", 0))
    topic_gate = topic_count >= 300
    passed = bool(gate["passed"] and topic_gate)

    decision = {
        "decision_id": "PHASE27_89_STRATIFIED_ROUND_ROBIN_CURRICULUM_SAMPLER_GATE_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_90_BOUNDED_SF10M_TRAINING_WITH_ROUND_ROBIN_SPLIT_ORDER"
            if passed
            else "BLOCK_TRAINING_AND_FIX_ROUND_ROBIN_SAMPLER"
        ),
        "new_training_allowed": passed,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "required_training_flag": "--split-order family_round_robin",
        "why": (
            "الترتيب الجديد يوزع عائلات الحوار داخل كل نافذة تدريبية بدل الكتل المتتابعة، "
            "لذلك يسمح فقط بتدريب SF-10M محدود في المرحلة التالية، مع استمرار حجب runtime."
            if passed
            else "فشل ترتيب family_round_robin في تحقيق توازن كاف داخل النوافذ التدريبية."
        ),
        "next_phase": (
            "Phase 27.90 — Bounded SF-10M Round-Robin Curriculum Repair Training"
            if passed
            else "Phase 27.89b — Round-Robin Sampler Repair"
        ),
    }
    return {
        "phase": "Phase 27.89",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_89_STRATIFIED_ROUND_ROBIN_SAMPLER_GATE_PASSED_TRAINING_ALLOWED_NEXT"
            if passed
            else "PHASE27_89_STRATIFIED_ROUND_ROBIN_SAMPLER_GATE_FAILED_TRAINING_BLOCKED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "source_phase27_88_status": source.get("status"),
        "corpus": _rel(args.corpus),
        "split_manifest": _rel(args.split_manifest),
        "split_orders_compared": ["sequential", "family_round_robin"],
        "sequential_first_1800_counts": dict(Counter(sequential)),
        "round_robin_first_1800_counts": first_1800_counts,
        "sequential_windows": sequential_windows,
        "round_robin_windows": round_robin_windows,
        "gate": {
            **gate,
            "topic_first_1800_min": 300,
            "topic_first_1800_count": topic_count,
            "topic_gate_passed": topic_gate,
        },
        "blocked_actions": [
            "runtime release",
            "UI generator release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
        ],
        "allowed_next_actions": [
            "one bounded SF-10M repair using --split-order family_round_robin",
            "save-window family-balance tracking",
            "held-out canary after training",
        ]
        if passed
        else ["repair sampler ordering only"],
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.89 — Stratified Round-Robin Curriculum Sampler Gate",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة بوابة فقط: لا تدريب، لا runtime، لا تغيير في الواجهة.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- training allowed next: `{decision['new_training_allowed']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- required training flag: `{decision['required_training_flag']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## المقارنة",
        "",
        f"- sequential first 1800: `{report['sequential_first_1800_counts']}`",
        f"- round-robin first 1800: `{report['round_robin_first_1800_counts']}`",
        "",
        "## نوافذ family_round_robin",
        "",
    ]
    for name, window in report["round_robin_windows"].items():
        labels = {
            KEY_TO_LABEL.get(family, family): count
            for family, count in window["counts"].items()
        }
        lines.append(
            f"- `{name}` range `{window['range']}` counts `{labels}` "
            f"dominant `{window['dominant_family']}` share `{window['dominant_share']}`"
        )
    lines.extend(
        [
            "",
            "## القرار",
            "",
            decision["why"],
            "",
            "## المحظور",
            "",
            *[f"- {item}" for item in report["blocked_actions"]],
            "",
            "## المسموح لاحقًا",
            "",
            *[f"- {item}" for item in report["allowed_next_actions"]],
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    report = build_report(args)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.decision.write_text(
        json.dumps(report["decision"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_doc(args.doc, report)
    print(json.dumps(report["decision"], ensure_ascii=False, indent=2))
    return 0 if report["gate"]["passed"] and report["gate"]["topic_gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
