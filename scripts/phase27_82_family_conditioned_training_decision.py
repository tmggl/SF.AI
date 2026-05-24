#!/usr/bin/env python3
"""Phase 27.82 — Family-conditioned SF-10M repair training decision.

This is a decision/config phase only. It does not train. It checks that:

- Phase 27.80 gates passed after the balanced family view.
- Phase 27.81 authored the balanced pack.
- corpus audit is clean.
- tokenizer/checkpoint are sovereign local artifacts.

If all gates pass, it allows Phase 27.83 bounded SF-10M repair training.
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

from sf_ai.datasets.corpus_governance import audit_jsonl_directory_for_training  # noqa: E402


DEFAULT_GATE_REPORT = ROOT / "artifacts/reports/phase27_80_repair_gate_validation_report.json"
DEFAULT_PACK_REPORT = ROOT / "artifacts/reports/phase27_81_balanced_family_pack_report.json"
DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v9_phase27_76"
DEFAULT_INIT_CHECKPOINTS = ROOT / "artifacts/eval/phase27_77_v9_bounded_open_social_lm_repair/checkpoints"
DEFAULT_INIT_CHECKPOINT_NAME = "sf-10m-step6200"
DEFAULT_PLAN_DIR = ROOT / "artifacts/reports/phase27_82_family_conditioned_training_decision"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_82_family_conditioned_training_decision_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_82_FAMILY_CONDITIONED_TRAINING_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_82_FAMILY_CONDITIONED_TRAINING_DECISION.md"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.82 SF-10M training decision")
    p.add_argument("--gate-report", type=Path, default=DEFAULT_GATE_REPORT)
    p.add_argument("--pack-report", type=Path, default=DEFAULT_PACK_REPORT)
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--init-checkpoints", type=Path, default=DEFAULT_INIT_CHECKPOINTS)
    p.add_argument("--init-checkpoint-name", default=DEFAULT_INIT_CHECKPOINT_NAME)
    p.add_argument("--plan-dir", type=Path, default=DEFAULT_PLAN_DIR)
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


def _tokenizer_ok(path: Path) -> dict[str, Any]:
    meta_path = path / "meta.json"
    meta = _load_json(meta_path)
    required = ("vocab.json", "merges.txt", "meta.json")
    present = [name for name in required if (path / name).exists()]
    return {
        "path": _rel(path),
        "present": present,
        "sf_origin": meta.get("sf_origin") is True,
        "vocab_size": meta.get("vocab_size"),
        "ready": len(present) == len(required) and meta.get("sf_origin") is True,
    }


def _checkpoint_ok(root: Path, name: str) -> dict[str, Any]:
    ckpt = root / name
    meta_path = ckpt / "meta.json"
    state_path = ckpt / "state.pt"
    meta = _load_json(meta_path)
    return {
        "root": _rel(root),
        "name": name,
        "state_exists": state_path.exists(),
        "sf_origin": meta.get("sf_origin") is True,
        "model_name": meta.get("model_name"),
        "ready": state_path.exists() and meta.get("sf_origin") is True,
    }


def _write_plan(path: Path, plan: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    gate = _load_json(args.gate_report)
    pack = _load_json(args.pack_report)
    corpus = audit_jsonl_directory_for_training(ROOT / "data/corpus/chat/jsonl")
    tokenizer = _tokenizer_ok(args.tokenizer)
    checkpoint = _checkpoint_ok(args.init_checkpoints, args.init_checkpoint_name)

    gate_passed = gate.get("decision", {}).get("all_gates_passed") is True
    pack_ready = pack.get("total_records") == 2500 and pack.get("training_started") is False
    corpus_ready = corpus.error_count == 0 and corpus.training_ready == 8443
    can_train_next = gate_passed and pack_ready and corpus_ready and tokenizer["ready"] and checkpoint["ready"]

    training_plan = {
        "phase": "Phase 27.83",
        "name": "Family-conditioned SF-10M bounded repair training",
        "allowed_by": "PHASE27_82_FAMILY_CONDITIONED_TRAINING_DECISION",
        "training_command": [
            "make",
            "train-lm",
            (
                "ARGS=\"--tokenizer artifacts/tokenizers/sf_bpe/v9_phase27_76 "
                "--corpus data/corpus/chat/jsonl --size sf-10m --seq-len 96 "
                "--batch-size 1 --steps 1800 --epochs 24 --lr 2e-4 --warmup 120 "
                "--save-every 600 --stream-format dialogue --loss-scope assistant "
                "--packing-mode sample_isolated --split-manifest data/corpus/chat/splits/dialogue_split_v1.json "
                "--split-name train --init-checkpoints artifacts/eval/phase27_77_v9_bounded_open_social_lm_repair/checkpoints "
                "--init-checkpoint-name sf-10m-step6200 --checkpoints artifacts/eval/phase27_83_family_conditioned_repair/checkpoints "
                "--checkpoint-name sf-10m-step0 --seed 20260706\""
            ),
        ],
        "tokenizer": _rel(args.tokenizer),
        "init_checkpoint": f"{_rel(args.init_checkpoints)}/{args.init_checkpoint_name}",
        "output_checkpoints": "artifacts/eval/phase27_83_family_conditioned_repair/checkpoints",
        "objective": "assistant_answer_only_with_family_conditioned_records",
        "curriculum": {
            "view": "explicit_balanced_family_view",
            "families": {
                "open_social": 500,
                "followup": 500,
                "planning": 500,
                "support": 500,
                "topic": 500,
            },
            "dialect_per_family": {"msa": 250, "saudi": 250},
        },
        "decoding_required_after_training": "semantic_guarded_decoding_v1",
        "release_rules": {
            "runtime_release_allowed_by_training": False,
            "must_pass_after_training": [
                "held-out dialogue quality",
                "fresh shadow canary",
                "family stability",
                "clean-stop",
                "open_social naturalness",
                "followup continuity",
                "no template masking",
            ],
        },
    }
    plan_path = args.plan_dir / "phase27_83_training_plan.json"
    _write_plan(plan_path, training_plan)

    decision = {
        "decision_id": "PHASE27_82_FAMILY_CONDITIONED_TRAINING_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_83_BOUNDED_SF10M_REPAIR_TRAINING"
            if can_train_next
            else "BLOCK_PHASE27_83_TRAINING_FIX_PREREQUISITES"
        ),
        "new_training_allowed": can_train_next,
        "training_allowed_phase": "Phase 27.83" if can_train_next else None,
        "tokenizer_retrain_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_justified_transition": False,
        "why": (
            "Phase 27.80 gates passed after Phase 27.81 balanced family pack; "
            "next training is bounded SF-10M repair only, not runtime release."
            if can_train_next
            else "One or more prerequisites failed."
        ),
        "next_phase": "Phase 27.83 — Family-conditioned SF-10M bounded repair training",
    }

    return {
        "phase": "Phase 27.82",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_82_ALLOW_PHASE27_83_BOUNDED_TRAINING"
            if can_train_next
            else "PHASE27_82_BLOCK_TRAINING"
        ),
        "training_started": False,
        "tokenizer_training_started": False,
        "runtime_changed": False,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "prerequisites": {
            "phase27_80_gates_passed": gate_passed,
            "phase27_81_pack_ready": pack_ready,
            "corpus_ready": corpus_ready,
            "tokenizer_ready": tokenizer["ready"],
            "init_checkpoint_ready": checkpoint["ready"],
        },
        "corpus": {
            "training_ready": corpus.training_ready,
            "issues": corpus.error_count,
            "dialects": dict(corpus.dialect_counts),
            "quality": dict(corpus.quality_counts),
        },
        "tokenizer": tokenizer,
        "init_checkpoint": checkpoint,
        "training_plan": training_plan,
        "artifacts": {"training_plan": _rel(plan_path)},
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.82 — Family-conditioned SF-10M Repair Training Decision",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة قرار فقط. لم يبدأ تدريب، ولم يتغير runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- new training allowed: `{decision['new_training_allowed']}`",
        f"- runtime release allowed: `{decision['runtime_release_allowed']}`",
        f"- SF-50M transition: `{decision['sf50m_justified_transition']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## Prerequisites",
        "",
    ]
    for key, value in report["prerequisites"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Training Plan",
            "",
            f"- tokenizer: `{report['training_plan']['tokenizer']}`",
            f"- init checkpoint: `{report['training_plan']['init_checkpoint']}`",
            f"- output: `{report['training_plan']['output_checkpoints']}`",
            "- objective: assistant-only, family-conditioned.",
            "- curriculum: explicit balanced family view.",
            "",
            "## Blocked",
            "",
            "- لا runtime release من هذه المرحلة.",
            "- لا SF-50M.",
            "- لا tokenizer retrain.",
            "- لا pretrained/open-weight.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        report = build_report(args)
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
    _write_doc(args.doc, report)

    print("SF.AI — Phase 27.82 family-conditioned training decision")
    print(f"status: {report['status']}")
    print(f"new_training_allowed: {report['decision']['new_training_allowed']}")
    print(f"report: {_rel(args.report)}")
    print(f"decision: {_rel(args.decision)}")
    print(f"doc: {_rel(args.doc)}")
    return 0 if report["decision"]["new_training_allowed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
