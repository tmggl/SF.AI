#!/usr/bin/env python3
"""Phase 27.95 — Bounded Topic Objective Repair Training.

This is SF-native training only. It starts from the best Phase 27.90
round-robin checkpoint, uses the Phase 27.93 topic anchor renderer, and keeps
runtime blocked regardless of the offline result.
"""
# ruff: noqa: E402, I001

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_26_heldout_objective_repair import _rel
from scripts.phase27_58_tokenizer_bounded_alignment_probe import _expected_ok, _family_terms, _surface
from scripts.phase27_60_broader_natural_dialogue_canary import _FORBIDDEN_BY_FAMILY
from scripts.phase27_67_fresh_shadow_canary import FRESH_SHADOW_CASES
from scripts.phase27_87_bounded_family_conditioned_repair import _evaluate_checkpoint
from sf_ai.modules.chat.generation_guard import GenerationGuard
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run

DEFAULT_SOURCE = ROOT / "artifacts/reports/PHASE27_94_TOPIC_OBJECTIVE_DATA_PACK_DECISION.json"
DEFAULT_CANARY = ROOT / "eval/prompts/phase27_93_topic_objective_canary.json"
DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v9_phase27_76"
DEFAULT_CORPUS = ROOT / "data/corpus/chat/jsonl"
DEFAULT_SPLIT = ROOT / "data/corpus/chat/splits/dialogue_split_v1.json"
DEFAULT_INIT_ROOT = ROOT / "artifacts/eval/phase27_90_round_robin_curriculum_repair/checkpoints"
DEFAULT_INIT_NAME = "sf-10m-step1800"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_95_topic_objective_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_95_bounded_topic_objective_repair_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_95_BOUNDED_TOPIC_OBJECTIVE_REPAIR_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_95_BOUNDED_TOPIC_OBJECTIVE_REPAIR_REPORT.md"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_95_bounded_topic_objective_repair.md"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.95 bounded topic-objective repair")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--canary", type=Path, default=DEFAULT_CANARY)
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    p.add_argument("--init-checkpoints", type=Path, default=DEFAULT_INIT_ROOT)
    p.add_argument("--init-checkpoint-name", default=DEFAULT_INIT_NAME)
    p.add_argument("--steps", type=int, default=1800)
    p.add_argument("--epochs", type=int, default=1)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=96)
    p.add_argument("--lr", type=float, default=2e-4)
    p.add_argument("--warmup", type=int, default=120)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args(argv)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _family_ok(text: str, family: str, families: dict[str, tuple[str, ...]]) -> bool:
    surface = _surface(text)
    allowed = any(_surface(term) in surface for term in families.get(family, ()))
    forbidden = any(_surface(term) in surface for term in _FORBIDDEN_BY_FAMILY.get(family, ()))
    return allowed and not forbidden


def _topic_text_ok(text: str, required: tuple[str, ...], forbidden: tuple[str, ...]) -> tuple[bool, str]:
    surface = _surface(text)
    required_ok = all(_surface(term) in surface for term in required)
    forbidden_hits = [term for term in forbidden if _surface(term) in surface]
    if not required_ok:
        return False, "required_topic_missing"
    if forbidden_hits:
        return False, "wrong_topic_leak:" + ",".join(forbidden_hits)
    return True, "topic_ok"


def _known_topic_rows(args: argparse.Namespace, checkpoint: str) -> list[dict[str, Any]]:
    suite = _load_json(args.canary)
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=args.tokenizer,
            checkpoints_root=args.work_dir / "checkpoints",
            checkpoint_name=checkpoint,
            generator_name=f"sf_10m_phase27_95_{checkpoint}",
            model_size="sf-10m",
            seq_len=args.seq_len,
            max_new_tokens=22,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.14,
            device=args.device,
            dialogue_prompt=True,
            family_conditioning=True,
        )
    )
    guard = GenerationGuard(min_chars=4)
    rows: list[dict[str, Any]] = []
    for item in suite["prompts"]:
        topic = item["required_terms"][0]
        out = generator.generate(
            item["message"],
            dialect=item["dialect"],
            intent="topic",
            topic=topic,
            max_new_tokens=22,
            temperature=1.0,
            top_k=0,
        )
        verdict = guard.inspect(out.text)
        topic_ok, topic_reason = _topic_text_ok(
            out.text,
            tuple(item["required_terms"]),
            tuple(item["forbidden_terms"]),
        )
        passed = bool(out.used and verdict.allowed and topic_ok)
        if passed:
            reason = "passed"
        elif not out.used:
            reason = f"generator:{out.reason}"
        elif not verdict.allowed:
            reason = f"guard:{verdict.reason}"
        else:
            reason = topic_reason
        rows.append(
            {
                "id": item["id"],
                "dialect": item["dialect"],
                "prompt": item["message"],
                "topic": topic,
                "response": out.text,
                "generator_used": out.used,
                "guard_allowed": verdict.allowed,
                "guard_reason": verdict.reason,
                "topic_ok": topic_ok,
                "passed": passed,
                "reason": reason,
            }
        )
    return rows


def _fresh_topic_rows(args: argparse.Namespace, checkpoint: str) -> list[dict[str, Any]]:
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=args.tokenizer,
            checkpoints_root=args.work_dir / "checkpoints",
            checkpoint_name=checkpoint,
            generator_name=f"sf_10m_phase27_95_{checkpoint}",
            model_size="sf-10m",
            seq_len=args.seq_len,
            max_new_tokens=22,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.14,
            device=args.device,
            dialogue_prompt=True,
            family_conditioning=True,
        )
    )
    guard = GenerationGuard(min_chars=4)
    families = _family_terms()
    rows: list[dict[str, Any]] = []
    for case in FRESH_SHADOW_CASES:
        if case.family != "topic":
            continue
        out = generator.generate(
            case.prompt,
            dialect=case.dialect,
            intent=case.intent,
            topic=case.topic,
            max_new_tokens=22,
            temperature=1.0,
            top_k=0,
        )
        verdict = guard.inspect(out.text)
        expected = _expected_ok(out.text, case.expected_any)
        family = _family_ok(out.text, case.family, families)
        passed = bool(out.used and verdict.allowed and expected and family)
        if passed:
            reason = "passed"
        elif not out.used:
            reason = f"generator:{out.reason}"
        elif not verdict.allowed:
            reason = f"guard:{verdict.reason}"
        elif not expected:
            reason = "expected_terms_missing"
        else:
            reason = "response_family_mismatch"
        rows.append(
            {
                "id": case.id,
                "dialect": case.dialect,
                "prompt": case.prompt,
                "topic": case.topic,
                "expected_any": list(case.expected_any),
                "response": out.text,
                "generator_used": out.used,
                "guard_allowed": verdict.allowed,
                "guard_reason": verdict.reason,
                "expected_ok": expected,
                "family_ok": family,
                "passed": passed,
                "reason": reason,
            }
        )
    return rows


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(1 for row in rows if row["passed"])
    return {
        "passed": passed,
        "total": len(rows),
        "pass_rate": round(passed / len(rows), 4) if rows else 0.0,
        "reason_counts": dict(Counter(str(row["reason"]) for row in rows)),
    }


def _evaluate_all(args: argparse.Namespace, checkpoint: str) -> dict[str, Any]:
    eval_args = argparse.Namespace(
        tokenizer=args.tokenizer,
        checkpoints=args.work_dir / "checkpoints",
        checkpoint_name=checkpoint,
        device=args.device,
    )
    all_family = _evaluate_checkpoint(eval_args, checkpoint)
    known = _known_topic_rows(args, checkpoint)
    fresh = _fresh_topic_rows(args, checkpoint)
    return {
        "checkpoint": checkpoint,
        "known_topic_rows": known,
        "known_topic_summary": _summary(known),
        "fresh_topic_rows": fresh,
        "fresh_topic_summary": _summary(fresh),
        "all_family": all_family,
    }


def _check_prerequisites(args: argparse.Namespace) -> dict[str, Any]:
    decision = _load_json(args.source)
    if decision["engineering_decision"] != "ALLOW_PHASE27_95_BOUNDED_TOPIC_OBJECTIVE_REPAIR_TRAINING":
        raise ValueError("Phase 27.94 did not allow Phase 27.95 training")
    if decision.get("phase27_95_training_allowed") is not True:
        raise ValueError("Phase 27.95 training flag is not true")
    return decision


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    source = _check_prerequisites(args)
    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)
    checkpoints = args.work_dir / "checkpoints"
    train_args = [
        "--tokenizer",
        str(args.tokenizer),
        "--corpus",
        str(args.corpus),
        "--size",
        "sf-10m",
        "--steps",
        str(args.steps),
        "--epochs",
        str(args.epochs),
        "--batch-size",
        str(args.batch_size),
        "--seq-len",
        str(args.seq_len),
        "--stream-format",
        "dialogue",
        "--loss-scope",
        "assistant",
        "--packing-mode",
        "sample_isolated",
        "--split-manifest",
        str(args.split_manifest),
        "--split-name",
        "train",
        "--split-order",
        "family_round_robin",
        "--init-checkpoints",
        str(args.init_checkpoints),
        "--init-checkpoint-name",
        args.init_checkpoint_name,
        "--lr",
        str(args.lr),
        "--warmup",
        str(args.warmup),
        "--min-lr",
        "1e-5",
        "--save-every",
        "600",
        "--seed",
        "20260795",
        "--checkpoints",
        str(checkpoints),
        "--device",
        args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        raise RuntimeError(f"training failed with exit code {train_code}")

    checkpoint_names = tuple(f"sf-10m-step{step}" for step in (600, 1200, 1800))
    evaluations = [_evaluate_all(args, checkpoint) for checkpoint in checkpoint_names]
    best = max(
        evaluations,
        key=lambda row: (
            row["known_topic_summary"]["passed"],
            row["fresh_topic_summary"]["passed"],
            row["all_family"]["summary"]["passed"],
        ),
    )
    known_pass = int(best["known_topic_summary"]["passed"])
    known_total = int(best["known_topic_summary"]["total"])
    fresh_pass = int(best["fresh_topic_summary"]["passed"])
    fresh_total = int(best["fresh_topic_summary"]["total"])
    all_pass = int(best["all_family"]["summary"]["passed"])
    all_total = int(best["all_family"]["summary"]["total"])

    known_gate = known_pass == known_total
    fresh_gate = fresh_pass >= 8
    all_family_gate = all_pass >= 45
    runtime_gate_allowed = bool(known_gate and fresh_gate and all_family_gate)

    decision = {
        "decision_id": "PHASE27_95_BOUNDED_TOPIC_OBJECTIVE_REPAIR_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_96_HELDOUT_RUNTIME_GATE_NO_DIRECT_RUNTIME"
            if runtime_gate_allowed
            else "BLOCK_RUNTIME_DIAGNOSE_TOPIC_OBJECTIVE_REPAIR_RESULT"
        ),
        "training_completed": True,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "heldout_runtime_gate_allowed": runtime_gate_allowed,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "best_checkpoint": best["checkpoint"],
        "known_topic": f"{known_pass}/{known_total}",
        "fresh_topic": f"{fresh_pass}/{fresh_total}",
        "all_family": f"{all_pass}/{all_total}",
        "required_gates": {
            "known_topic": f"{known_total}/{known_total}",
            "fresh_topic": "8/10",
            "all_family": "45/50",
        },
        "why": (
            f"Best checkpoint {best['checkpoint']} scored known={known_pass}/{known_total}, "
            f"fresh_topic={fresh_pass}/{fresh_total}, all_family={all_pass}/{all_total}. "
            "Runtime remains blocked; a separate held-out gate is required if all gates pass."
        ),
        "next_phase": (
            "Phase 27.96 — Held-out Runtime Gate for Topic Objective Repair"
            if runtime_gate_allowed
            else "Phase 27.96 — Topic Objective Repair Result Diagnosis"
        ),
    }
    return {
        "phase": "Phase 27.95",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_95_TRAINED_HELDOUT_GATE_ALLOWED_RUNTIME_BLOCKED"
            if runtime_gate_allowed
            else "PHASE27_95_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_completed": True,
        "runtime_changed": False,
        "source_decision": source,
        "training_scope": "bounded SF-10M topic-objective repair; no runtime; no SF-50M",
        "objective": "topic_anchor_prompt_to_answer_objective_v1",
        "tokenizer": _rel(args.tokenizer),
        "corpus": _rel(args.corpus),
        "split_manifest": _rel(args.split_manifest),
        "init_checkpoint": f"{_rel(args.init_checkpoints)}/{args.init_checkpoint_name}",
        "checkpoint_root": _rel(checkpoints),
        "train_config": {
            "steps": args.steps,
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "seq_len": args.seq_len,
            "lr": args.lr,
            "warmup": args.warmup,
            "split_order": "family_round_robin",
            "loss_scope": "assistant",
            "packing_mode": "sample_isolated",
        },
        "prompt_alignment_fix": "NativeGenerator family_conditioning now emits الموضوع المطلوب for topic prompts.",
        "checkpoints": evaluations,
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.95 — Bounded Topic Objective Repair Training",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تدريب محدودة على SF-10M فقط. لا تفتح runtime أو الواجهة.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- best checkpoint: `{decision['best_checkpoint']}`",
        f"- known topic: `{decision['known_topic']}`",
        f"- fresh topic: `{decision['fresh_topic']}`",
        f"- all family: `{decision['all_family']}`",
        f"- held-out gate allowed: `{decision['heldout_runtime_gate_allowed']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## Checkpoints",
        "",
    ]
    for row in report["checkpoints"]:
        lines.extend(
            [
                f"### {row['checkpoint']}",
                "",
                f"- known topic: `{row['known_topic_summary']['passed']}/{row['known_topic_summary']['total']}`",
                f"- fresh topic: `{row['fresh_topic_summary']['passed']}/{row['fresh_topic_summary']['total']}`",
                f"- all family: `{row['all_family']['summary']['passed']}/{row['all_family']['summary']['total']}`",
                f"- known reasons: `{row['known_topic_summary']['reason_counts']}`",
                f"- fresh reasons: `{row['fresh_topic_summary']['reason_counts']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## القرار",
            "",
            decision["why"],
            "",
            "محظور من هذه المرحلة: runtime release, UI generator release, SF-50M, tokenizer retrain, pretrained/open-weight usage.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_samples(path: Path, report: dict[str, Any]) -> None:
    lines = ["# Phase 27.95 Samples", ""]
    for checkpoint in report["checkpoints"]:
        lines.extend([f"## {checkpoint['checkpoint']}", ""])
        for group_name, rows in (
            ("Known Topic", checkpoint["known_topic_rows"]),
            ("Fresh Topic", checkpoint["fresh_topic_rows"]),
            ("All Family Failures", [r for r in checkpoint["all_family"]["rows"] if not r["passed"]][:15]),
        ):
            lines.extend([f"### {group_name}", ""])
            for row in rows:
                if group_name != "All Family Failures" and row["passed"]:
                    continue
                lines.extend(
                    [
                        f"- id: `{row['id']}`",
                        f"  prompt: {row['prompt']}",
                        f"  response: {row['response']}",
                        f"  passed: {row['passed']}",
                        f"  reason: {row['reason']}",
                        "",
                    ]
                )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        report = build_report(args)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError, RuntimeError) as exc:
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
    _write_samples(args.samples, report)

    decision = report["decision"]
    print("SF.AI — Phase 27.95 bounded topic-objective repair")
    print(f"status: {report['status']}")
    print(f"decision: {decision['engineering_decision']}")
    print(f"best: {decision['best_checkpoint']}")
    print(f"known_topic: {decision['known_topic']}")
    print(f"fresh_topic: {decision['fresh_topic']}")
    print(f"all_family: {decision['all_family']}")
    print(f"runtime: {'held-out gate only' if decision['heldout_runtime_gate_allowed'] else 'blocked'}")
    print(f"report: {_rel(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
