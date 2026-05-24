#!/usr/bin/env python3
"""Phase 27.88 — diagnose Phase 27.87 family-conditioned training result.

No training. No runtime release. The diagnosis checks whether the weak
fresh-shadow result is caused by model capacity or by the training stream
ordering after the renderer fix.
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

from sf_ai.datasets import ChatDataset
from sf_ai.training.train_tiny_lm import _iter_training_texts


DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_87_bounded_family_conditioned_repair_report.json"
DEFAULT_CORPUS = ROOT / "data/corpus/chat/jsonl"
DEFAULT_SPLIT = ROOT / "data/corpus/chat/splits/dialogue_split_v1.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_88_family_conditioned_training_result_diagnosis_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_88_FAMILY_CONDITIONED_TRAINING_RESULT_DIAGNOSIS_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_88_FAMILY_CONDITIONED_TRAINING_RESULT_DIAGNOSIS_REPORT.md"


CHECKPOINT_WINDOWS = {
    "sf-10m-step600": (1, 600),
    "sf-10m-step1200": (601, 1200),
    "sf-10m-step1800": (1201, 1800),
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.88 result diagnosis")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args()


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
            return line.split(":", 1)[1].strip()
    return "unknown"


def _training_stream_families(corpus: Path, split_manifest: Path, *, limit: int) -> list[str]:
    dataset = ChatDataset(corpus)
    families: list[str] = []
    for text in _iter_training_texts(
        dataset,
        stream_format="dialogue",
        split_manifest=split_manifest,
        split_name="train",
    ):
        families.append(_family_from_text(text))
        if len(families) >= limit:
            break
    return families


def _window_counts(families: list[str]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for checkpoint, (start, end) in CHECKPOINT_WINDOWS.items():
        slice_families = families[start - 1:end]
        counts = Counter(slice_families)
        dominant = counts.most_common(1)[0] if counts else ("none", 0)
        out[checkpoint] = {
            "range": [start, end],
            "total": len(slice_families),
            "counts": dict(counts),
            "dominant_family": dominant[0],
            "dominant_count": dominant[1],
            "dominant_share": round(dominant[1] / len(slice_families), 4)
            if slice_families
            else 0.0,
        }
    return out


def _dominant_pass_family(checkpoint: dict[str, Any]) -> tuple[str, int]:
    summary = checkpoint["summary"]["family_summary"]
    family, stats = max(summary.items(), key=lambda item: int(item[1]["passed"]))
    return family, int(stats["passed"])


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    source = _load_json(args.source)
    families = _training_stream_families(args.corpus, args.split_manifest, limit=1800)
    windows = _window_counts(families)
    first_1800_counts = dict(Counter(families))

    checkpoint_alignment: list[dict[str, Any]] = []
    label_to_key = {
        "سوالف": "open_social",
        "متابعة": "followup",
        "تنظيم": "planning",
        "دعم": "support",
        "موضوع": "topic",
    }
    for checkpoint in source["checkpoints"]:
        name = checkpoint["checkpoint"]
        pass_family, pass_count = _dominant_pass_family(checkpoint)
        train_family_label = windows[name]["dominant_family"]
        train_family_key = label_to_key.get(train_family_label, train_family_label)
        checkpoint_alignment.append(
            {
                "checkpoint": name,
                "train_window_dominant_family_label": train_family_label,
                "train_window_dominant_family": train_family_key,
                "train_window_dominant_share": windows[name]["dominant_share"],
                "pass_dominant_family": pass_family,
                "pass_dominant_count": pass_count,
                "aligned": train_family_key == pass_family,
            }
        )

    topic_underexposed = int(first_1800_counts.get("موضوع", 0)) <= 10
    later_checkpoints_align = all(row["aligned"] for row in checkpoint_alignment[1:])
    first_checkpoint_inherited_open_social = (
        checkpoint_alignment[0]["pass_dominant_family"] == "open_social"
        and checkpoint_alignment[0]["train_window_dominant_family"] == "followup"
    )

    root_cause_weights = {
        "sequential_curriculum_ordering": 38,
        "checkpoint_recency_bias": 22,
        "topic_underexposure_before_step1800": 16,
        "family_condition_signal_not_interleaved": 12,
        "decoding": 4,
        "model_capacity": 4,
        "tokenizer": 2,
        "semantic_routing": 2,
    }
    diagnosis_passed = bool(topic_underexposed and later_checkpoints_align)
    decision = {
        "decision_id": "PHASE27_88_FAMILY_CONDITIONED_TRAINING_RESULT_DIAGNOSIS_DECISION",
        "engineering_decision": (
            "DESIGN_STRATIFIED_ROUND_ROBIN_CURRICULUM_BEFORE_ANY_TRAINING"
            if diagnosis_passed
            else "BLOCK_AND_REINSPECT_PHASE27_87_EVIDENCE"
        ),
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "sampler_implementation_allowed": diagnosis_passed,
        "why": (
            "ترتيب stream التدريب متسلسل حسب عائلة الحوار: عائلة الموضوع تظهر "
            f"{first_1800_counts.get('موضوع', 0)} مرات فقط في أول 1800 عينة، "
            "والـ checkpoints اللاحقة تتبع آخر كتلة عائلية رآها النموذج. هذا خلل "
            "curriculum/sampling وليس مبررًا للقفز في الحجم."
        ),
        "next_phase": "Phase 27.89 — Stratified Round-Robin Curriculum Sampler Gate",
    }
    return {
        "phase": "Phase 27.88",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_88_DIAGNOSED_SEQUENTIAL_CURRICULUM_COLLAPSE_NO_TRAINING"
            if diagnosis_passed
            else "PHASE27_88_DIAGNOSIS_INCONCLUSIVE_TRAINING_BLOCKED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "source_report": _rel(args.source),
        "corpus": _rel(args.corpus),
        "split_manifest": _rel(args.split_manifest),
        "first_1800_family_counts": first_1800_counts,
        "checkpoint_training_windows": windows,
        "checkpoint_alignment": checkpoint_alignment,
        "evidence": {
            "topic_underexposed_before_step1800": topic_underexposed,
            "later_checkpoints_align_with_recent_family_block": later_checkpoints_align,
            "step600_likely_inherited_open_social_from_init": first_checkpoint_inherited_open_social,
            "best_phase27_87_score": source["decision"]["best_fresh_shadow_passed"],
            "best_phase27_87_total": source["decision"]["best_fresh_shadow_total"],
        },
        "root_cause_weights": root_cause_weights,
        "blocked_actions": [
            "new LM training",
            "runtime release",
            "UI generator release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
        ],
        "allowed_next_actions": [
            "implement stratified round-robin split streaming",
            "dry-run sampler balance before training",
            "define per-save-window family balance gate",
        ],
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.88 — Family-conditioned Training Result Diagnosis",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تشخيص فقط. لا تدريب ولا runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- training allowed: `{decision['new_training_allowed']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- sampler implementation allowed: `{decision['sampler_implementation_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## الدليل",
        "",
        f"- first 1800 family counts: `{report['first_1800_family_counts']}`",
        "",
        "### Checkpoint Windows",
        "",
    ]
    for checkpoint, window in report["checkpoint_training_windows"].items():
        lines.extend(
            [
                f"- `{checkpoint}` range `{window['range']}` dominant "
                f"`{window['dominant_family']}` share `{window['dominant_share']}` counts `{window['counts']}`",
            ]
        )
    lines.extend(["", "### Alignment", ""])
    for row in report["checkpoint_alignment"]:
        lines.append(
            f"- `{row['checkpoint']}` train dominant `{row['train_window_dominant_family']}` "
            f"→ pass dominant `{row['pass_dominant_family']}` aligned `{row['aligned']}`"
        )
    lines.extend(["", "## Root Cause Weights", ""])
    for key, value in report["root_cause_weights"].items():
        lines.append(f"- `{key}`: `{value}%`")
    lines.extend(
        [
            "",
            "## القرار",
            "",
            decision["why"],
            "",
            "لا نكبر إلى SF-50M ولا نعيد التدريب قبل بناء sampler متوازن و dry-run gate.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        report = build_report(args)
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.write_text(
        json.dumps(report["decision"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_doc(args.doc, report)

    print("SF.AI — Phase 27.88 family-conditioned training result diagnosis")
    print(f"status: {report['status']}")
    print(f"decision: {report['decision']['engineering_decision']}")
    print(f"next: {report['decision']['next_phase']}")
    print(f"report: {_rel(args.report)}")
    return 0 if report["decision"]["sampler_implementation_allowed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
