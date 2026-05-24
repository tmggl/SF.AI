#!/usr/bin/env python3
"""Phase 27.81 — execute bounded SF-10M family-conditioned repair training.

SF-native only. This script is intentionally a bounded repair run:
- consumes the Phase 27.80 gate decision;
- starts from the best Phase 27.104 sovereign SF-10M checkpoint;
- trains on the governed corpus split with family round-robin ordering;
- evaluates with guarded decoding, topic canaries, and all-family shadow;
- never opens runtime, never trains a tokenizer, never scales to SF-50M.
"""
# ruff: noqa: E402

from __future__ import annotations

import argparse
import csv
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
from scripts.phase27_58_tokenizer_bounded_alignment_probe import (
    _expected_ok,
    _family_terms,
    _surface,
)
from scripts.phase27_60_broader_natural_dialogue_canary import _FORBIDDEN_BY_FAMILY
from scripts.phase27_67_fresh_shadow_canary import FRESH_SHADOW_CASES
from scripts.phase27_104_bounded_topic_prototype_contrastive_repair import (
    _copy_anchor_ok,
    _load_json,
    _observed_wrong_topics,
)
from sf_ai.modules.chat.generation_guard import GenerationGuard
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run

DEFAULT_SOURCE = (
    ROOT
    / "artifacts/reports/PHASE27_80_BOUNDED_FAMILY_CONDITIONED_REPAIR_GATE_DECISION.json"
)
DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v9_phase27_76"
DEFAULT_CORPUS = ROOT / "data/corpus/chat/jsonl"
DEFAULT_SPLIT = ROOT / "data/corpus/chat/splits/dialogue_split_v1.json"
DEFAULT_INIT_ROOT = ROOT / "artifacts/eval/phase27_104_topic_prototype_contrastive_repair/checkpoints"
DEFAULT_INIT_NAME = "sf-10m-step1200"
DEFAULT_PROTOTYPE_CANARY = ROOT / "eval/prompts/phase27_102_topic_prototype_contrastive_canary.json"
DEFAULT_TOPIC_CANARY = ROOT / "eval/prompts/phase27_98_topic_binding_contrastive_canary.json"
DEFAULT_POLICY = ROOT / "artifacts/eval/phase27_80_family_conditioned_gate/decoding_policy_v2.json"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_81_bounded_family_conditioned_repair_training"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_81_bounded_family_conditioned_repair_training_report.json"
DEFAULT_DECISION = (
    ROOT / "artifacts/reports/PHASE27_81_BOUNDED_FAMILY_CONDITIONED_REPAIR_TRAINING_DECISION.json"
)
DEFAULT_DOC = ROOT / "docs/PHASE27_81_BOUNDED_FAMILY_CONDITIONED_REPAIR_TRAINING_REPORT.md"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_81_bounded_family_conditioned_repair_training.md"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.81 bounded SF-10M repair")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    p.add_argument("--init-checkpoints", type=Path, default=DEFAULT_INIT_ROOT)
    p.add_argument("--init-checkpoint-name", default=DEFAULT_INIT_NAME)
    p.add_argument("--prototype-canary", type=Path, default=DEFAULT_PROTOTYPE_CANARY)
    p.add_argument("--topic-canary", type=Path, default=DEFAULT_TOPIC_CANARY)
    p.add_argument("--decoding-policy", type=Path, default=DEFAULT_POLICY)
    p.add_argument("--steps", type=int, default=2000)
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=96)
    p.add_argument("--lr", type=float, default=6e-5)
    p.add_argument("--warmup", type=int, default=120)
    p.add_argument("--save-every", type=int, default=500)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args(argv)


def _check_source(path: Path) -> dict[str, Any]:
    decision = _load_json(path)
    if decision.get("decision_id") != "PHASE27_80_BOUNDED_FAMILY_CONDITIONED_REPAIR_GATE_DECISION":
        raise ValueError("Phase 27.80 decision id mismatch")
    if decision.get("bounded_training_allowed_next") is not True:
        raise ValueError("Phase 27.80 did not allow bounded training")
    if decision.get("runtime_release_allowed") is not False:
        raise ValueError("Phase 27.80 must keep runtime blocked")
    return decision


def _policy(path: Path) -> dict[str, Any]:
    policy = _load_json(path)
    if policy.get("template_masking_forbidden") is not True:
        raise ValueError("decoding policy must forbid template masking")
    if policy.get("stop_at_eos") is not True:
        raise ValueError("decoding policy must stop at EOS")
    return policy


def _checkpoint_names(steps: int, save_every: int) -> tuple[str, ...]:
    if steps < 1 or save_every < 1:
        raise ValueError("steps and save_every must be positive")
    checkpoints = [step for step in range(save_every, steps + 1, save_every)]
    if checkpoints[-1] != steps:
        checkpoints.append(steps)
    return tuple(f"sf-10m-step{step}" for step in checkpoints)


def _generator(
    args: argparse.Namespace,
    checkpoint: str,
    policy: dict[str, Any],
    *,
    generator_name: str,
    max_new_tokens: int = 28,
) -> NativeGenerator:
    return NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=args.tokenizer,
            checkpoints_root=args.work_dir / "checkpoints",
            checkpoint_name=checkpoint,
            generator_name=generator_name,
            model_size="sf-10m",
            seq_len=args.seq_len,
            max_new_tokens=max_new_tokens,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=int(policy["no_repeat_ngram_size"]),
            repetition_penalty=float(policy["repetition_penalty"]),
            device=args.device,
            dialogue_prompt=True,
            family_conditioning=True,
        )
    )


def _family_ok(text: str, family: str, families: dict[str, tuple[str, ...]]) -> bool:
    surface = _surface(text)
    allowed = any(_surface(term) in surface for term in families.get(family, ()))
    forbidden = any(_surface(term) in surface for term in _FORBIDDEN_BY_FAMILY.get(family, ()))
    return allowed and not forbidden


def _all_family_rows(
    args: argparse.Namespace,
    checkpoint: str,
    policy: dict[str, Any],
) -> list[dict[str, Any]]:
    generator = _generator(
        args,
        checkpoint,
        policy,
        generator_name=f"sf_10m_phase27_81_{checkpoint}",
    )
    guard = GenerationGuard(min_chars=4)
    families = _family_terms()
    rows: list[dict[str, Any]] = []
    for case in FRESH_SHADOW_CASES:
        out = generator.generate(
            case.prompt,
            dialect=case.dialect,
            intent=case.intent,
            topic=case.topic,
            max_new_tokens=28,
            temperature=1.0,
            top_k=0,
        )
        verdict = (
            guard.inspect(out.text)
            if case.family == "topic"
            else guard.inspect_for_prompt(case.prompt, out.text)
        )
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
                "intent": case.intent,
                "topic": case.topic,
                "family": case.family,
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


def _topic_suite_rows(
    args: argparse.Namespace,
    checkpoint: str,
    suite_path: Path,
    policy: dict[str, Any],
    *,
    canary_set: str | None,
) -> list[dict[str, Any]]:
    suite = _load_json(suite_path)
    generator = _generator(
        args,
        checkpoint,
        policy,
        generator_name=f"sf_10m_phase27_81_topic_{checkpoint}",
        max_new_tokens=24,
    )
    guard = GenerationGuard(min_chars=4)
    rows: list[dict[str, Any]] = []
    for item in suite["prompts"]:
        if canary_set is not None and str(item["set"]) != canary_set:
            continue
        topic = str(item["requested_topic"])
        out = generator.generate(
            str(item["message"]),
            dialect=str(item["dialect"]),
            intent="topic",
            topic=topic,
            max_new_tokens=24,
            temperature=1.0,
            top_k=0,
        )
        verdict = guard.inspect(out.text)
        required_ok = all(_surface(term) in _surface(out.text) for term in item["required_terms"])
        wrong = _observed_wrong_topics(out.text, topic)
        copy_anchor_ok = _copy_anchor_ok(
            out.text,
            topic,
            int(item.get("copy_anchor_max_visible_arabic_chars") or 12),
        )
        passed = bool(out.used and verdict.allowed and required_ok and not wrong and copy_anchor_ok)
        if passed:
            reason = "passed"
        elif not out.used:
            reason = f"generator:{out.reason}"
        elif not verdict.allowed:
            reason = f"guard:{verdict.reason}"
        elif not required_ok:
            reason = "required_topic_missing"
        elif wrong:
            reason = "observed_wrong_topic:" + ",".join(wrong)
        else:
            reason = "copy_anchor_missing_or_late"
        rows.append(
            {
                "id": item["id"],
                "set": item["set"],
                "dialect": item["dialect"],
                "prompt": item["message"],
                "topic": topic,
                "required_terms": list(item["required_terms"]),
                "response": out.text,
                "generator_used": out.used,
                "guard_allowed": verdict.allowed,
                "guard_reason": verdict.reason,
                "required_ok": required_ok,
                "copy_anchor_ok": copy_anchor_ok,
                "observed_wrong_topics": wrong,
                "passed": passed,
                "reason": reason,
            }
        )
    return rows


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(1 for row in rows if row["passed"])
    families = sorted({str(row.get("family", "")) for row in rows if row.get("family")})
    return {
        "passed": passed,
        "total": len(rows),
        "pass_rate": round(passed / len(rows), 4) if rows else 0.0,
        "family_summary": {
            family: {
                "passed": sum(1 for row in rows if row.get("family") == family and row["passed"]),
                "total": sum(1 for row in rows if row.get("family") == family),
            }
            for family in families
        },
        "observed_wrong_topic_count": sum(
            len(row.get("observed_wrong_topics", ())) for row in rows
        ),
        "reason_counts": dict(Counter(str(row["reason"]) for row in rows)),
    }


def _evaluate_checkpoint(
    args: argparse.Namespace,
    checkpoint: str,
    policy: dict[str, Any],
) -> dict[str, Any]:
    all_family_rows = _all_family_rows(args, checkpoint, policy)
    prototype = _topic_suite_rows(
        args,
        checkpoint,
        args.prototype_canary,
        policy,
        canary_set="prototype_contrastive",
    )
    known = _topic_suite_rows(args, checkpoint, args.topic_canary, policy, canary_set="known")
    fresh = _topic_suite_rows(args, checkpoint, args.topic_canary, policy, canary_set="fresh")
    return {
        "checkpoint": checkpoint,
        "all_family_rows": all_family_rows,
        "all_family_summary": _summary(all_family_rows),
        "prototype_rows": prototype,
        "prototype_summary": _summary(prototype),
        "known_topic_rows": known,
        "known_topic_summary": _summary(known),
        "fresh_topic_rows": fresh,
        "fresh_topic_summary": _summary(fresh),
    }


def _select_best(evaluations: list[dict[str, Any]]) -> dict[str, Any]:
    return max(
        evaluations,
        key=lambda row: (
            row["all_family_summary"]["passed"],
            row["prototype_summary"]["passed"],
            -row["prototype_summary"]["observed_wrong_topic_count"],
            row["known_topic_summary"]["passed"],
            row["fresh_topic_summary"]["passed"],
        ),
    )


def _write_metrics_csv(path: Path, evaluations: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "checkpoint",
                "all_family_passed",
                "all_family_total",
                "prototype_passed",
                "prototype_total",
                "known_topic_passed",
                "known_topic_total",
                "fresh_topic_passed",
                "fresh_topic_total",
                "observed_wrong_topic_count",
            ],
        )
        writer.writeheader()
        for row in evaluations:
            writer.writerow(
                {
                    "checkpoint": row["checkpoint"],
                    "all_family_passed": row["all_family_summary"]["passed"],
                    "all_family_total": row["all_family_summary"]["total"],
                    "prototype_passed": row["prototype_summary"]["passed"],
                    "prototype_total": row["prototype_summary"]["total"],
                    "known_topic_passed": row["known_topic_summary"]["passed"],
                    "known_topic_total": row["known_topic_summary"]["total"],
                    "fresh_topic_passed": row["fresh_topic_summary"]["passed"],
                    "fresh_topic_total": row["fresh_topic_summary"]["total"],
                    "observed_wrong_topic_count": row["prototype_summary"][
                        "observed_wrong_topic_count"
                    ],
                }
            )


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    source_decision = _check_source(args.source)
    policy = _policy(args.decoding_policy)
    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)

    checkpoints_root = args.work_dir / "checkpoints"
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
        str(args.save_every),
        "--seed",
        "20267081",
        "--checkpoints",
        str(checkpoints_root),
        "--device",
        args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        raise RuntimeError(f"training failed with exit code {train_code}")

    checkpoints = _checkpoint_names(args.steps, args.save_every)
    evaluations = [_evaluate_checkpoint(args, checkpoint, policy) for checkpoint in checkpoints]
    best = _select_best(evaluations)

    all_pass = int(best["all_family_summary"]["passed"])
    all_total = int(best["all_family_summary"]["total"])
    prototype_pass = int(best["prototype_summary"]["passed"])
    prototype_total = int(best["prototype_summary"]["total"])
    prototype_wrong = int(best["prototype_summary"]["observed_wrong_topic_count"])
    known_pass = int(best["known_topic_summary"]["passed"])
    known_total = int(best["known_topic_summary"]["total"])
    fresh_pass = int(best["fresh_topic_summary"]["passed"])
    fresh_total = int(best["fresh_topic_summary"]["total"])
    topic_family = best["all_family_summary"]["family_summary"].get("topic", {})
    topic_family_pass = int(topic_family.get("passed", 0))
    topic_family_total = int(topic_family.get("total", 0))

    required = {
        "all_family": "45/50",
        "prototype_canary": "16/16",
        "prototype_observed_wrong_topic_count": 0,
        "known_topic": "16/16",
        "fresh_topic": "8/10",
        "topic_family": "8/10",
    }
    heldout_gate_allowed = bool(
        all_pass >= 45
        and prototype_pass == prototype_total
        and prototype_wrong == 0
        and known_pass == known_total
        and fresh_pass >= 8
        and topic_family_pass >= 8
    )

    metrics_csv = args.work_dir / "logs" / "phase27_81_metrics.csv"
    _write_metrics_csv(metrics_csv, evaluations)

    decision = {
        "decision_id": "PHASE27_81_BOUNDED_FAMILY_CONDITIONED_REPAIR_TRAINING_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_82_HELDOUT_RUNTIME_RELEASE_GATE_NO_DIRECT_RUNTIME"
            if heldout_gate_allowed
            else "BLOCK_RUNTIME_DIAGNOSE_PHASE27_81_RESULT"
        ),
        "training_completed": True,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "heldout_runtime_gate_allowed": heldout_gate_allowed,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "best_checkpoint": best["checkpoint"],
        "all_family": f"{all_pass}/{all_total}",
        "prototype_canary": f"{prototype_pass}/{prototype_total}",
        "prototype_observed_wrong_topic_count": prototype_wrong,
        "known_topic": f"{known_pass}/{known_total}",
        "fresh_topic": f"{fresh_pass}/{fresh_total}",
        "topic_family": f"{topic_family_pass}/{topic_family_total}",
        "required_gates": required,
        "why": (
            f"Best checkpoint {best['checkpoint']} scored all-family={all_pass}/{all_total}, "
            f"prototype={prototype_pass}/{prototype_total}, known={known_pass}/{known_total}, "
            f"fresh={fresh_pass}/{fresh_total}. Runtime remains blocked."
        ),
        "next_phase": (
            "Phase 27.82 — Held-out Runtime Release Gate"
            if heldout_gate_allowed
            else "Phase 27.82 — Phase 27.81 Result Diagnosis"
        ),
    }
    return {
        "phase": "Phase 27.81",
        "phase_title": "Execute bounded SF-10M family-conditioned repair training",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_81_TRAINED_HELDOUT_GATE_ALLOWED_NO_RUNTIME"
            if heldout_gate_allowed
            else "PHASE27_81_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_completed": True,
        "runtime_changed": False,
        "source_decision": source_decision,
        "training_scope": "bounded SF-10M family-conditioned repair from Phase 27.80 gates",
        "objective": "family_conditioned_assistant_only_objective_v2",
        "tokenizer": _rel(args.tokenizer),
        "init_checkpoint": _rel(args.init_checkpoints / args.init_checkpoint_name),
        "checkpoint_root": _rel(checkpoints_root),
        "split_manifest": _rel(args.split_manifest),
        "split_order": "family_round_robin",
        "train_config": {
            "steps": args.steps,
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "seq_len": args.seq_len,
            "lr": args.lr,
            "warmup": args.warmup,
            "save_every": args.save_every,
            "loss_scope": "assistant",
            "packing_mode": "sample_isolated",
            "amp_enabled": False,
        },
        "decoding_policy": {
            "source": _rel(args.decoding_policy),
            "no_repeat_ngram_size": policy["no_repeat_ngram_size"],
            "repetition_penalty": policy["repetition_penalty"],
            "stop_at_eos": policy["stop_at_eos"],
            "template_masking_forbidden": policy["template_masking_forbidden"],
        },
        "local_logs": {"metrics_csv": _rel(metrics_csv)},
        "checkpoints": evaluations,
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.81 — Bounded Family-conditioned Repair Training",
        "",
        "## الخلاصة",
        "",
        "اكتمل تدريب مقيّد على SF-10M بعد نجاح بوابات Phase 27.80. لا يوجد runtime release.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- best checkpoint: `{decision['best_checkpoint']}`",
        f"- all-family: `{decision['all_family']}`",
        f"- prototype: `{decision['prototype_canary']}`",
        f"- known topic: `{decision['known_topic']}`",
        f"- fresh topic: `{decision['fresh_topic']}`",
        f"- topic family: `{decision['topic_family']}`",
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
                f"- all-family: `{row['all_family_summary']['passed']}/{row['all_family_summary']['total']}`",
                f"- prototype: `{row['prototype_summary']['passed']}/{row['prototype_summary']['total']}`",
                f"- known topic: `{row['known_topic_summary']['passed']}/{row['known_topic_summary']['total']}`",
                f"- fresh topic: `{row['fresh_topic_summary']['passed']}/{row['fresh_topic_summary']['total']}`",
                f"- reasons: `{row['all_family_summary']['reason_counts']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## القرار",
            "",
            "- لا تفعيل للواجهة من هذه المرحلة.",
            "- لا SF-50M.",
            "- لا tokenizer retrain.",
            "- لا قوالب تخفي فشل المولد.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_samples(path: Path, report: dict[str, Any]) -> None:
    best_name = report["decision"]["best_checkpoint"]
    best = next(row for row in report["checkpoints"] if row["checkpoint"] == best_name)
    lines = ["# Phase 27.81 Samples", "", f"Best checkpoint: `{best_name}`", ""]
    for row in best["all_family_rows"][:30]:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- family: {row['family']}",
                f"- prompt: {row['prompt']}",
                f"- response: {row['response']}",
                f"- reason: {row['reason']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = build_report(args)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, RuntimeError, ValueError) as exc:
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
    print("SF.AI — Phase 27.81 bounded family-conditioned repair training")
    print(f"status: {report['status']}")
    print(f"decision: {decision['engineering_decision']}")
    print(f"best: {decision['best_checkpoint']} all-family={decision['all_family']}")
    print(f"topic: prototype={decision['prototype_canary']} fresh={decision['fresh_topic']}")
    print(f"next: {decision['next_phase']}")
    print(f"report: {_rel(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
