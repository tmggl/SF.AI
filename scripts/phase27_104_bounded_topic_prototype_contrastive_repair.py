#!/usr/bin/env python3
"""Phase 27.104 — Bounded Topic Prototype Contrastive Repair Training.

SF-native training only. No tokenizer work. No runtime release.

This phase consumes the Phase 27.103 curriculum pack through a scheduled
topic/dialect training view, starts from the best Phase 27.100 SF-10M
checkpoint, and evaluates:
- Phase 27.102 prototype canary (observed wrong-topic + copy-anchor);
- Phase 27.98 known/fresh topic canary;
- all-family fresh-shadow regression.
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
from scripts.phase27_58_tokenizer_bounded_alignment_probe import _surface
from scripts.phase27_87_bounded_family_conditioned_repair import _evaluate_checkpoint
from sf_ai.modules.chat.generation_guard import GenerationGuard
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run

DEFAULT_SOURCE = ROOT / "artifacts/reports/PHASE27_103_TOPIC_PROTOTYPE_CONTRASTIVE_CURRICULUM_PACK_DECISION.json"
DEFAULT_PACK = ROOT / "data/corpus/chat/jsonl/dialogue_batch_v12_topic_prototype_contrastive_012.jsonl"
DEFAULT_SCHEDULE = ROOT / "artifacts/reports/phase27_103_topic_prototype_contrastive_curriculum_schedule.json"
DEFAULT_PROTOTYPE_CANARY = ROOT / "eval/prompts/phase27_102_topic_prototype_contrastive_canary.json"
DEFAULT_TOPIC_CANARY = ROOT / "eval/prompts/phase27_98_topic_binding_contrastive_canary.json"
DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v9_phase27_76"
DEFAULT_INIT_ROOT = ROOT / "artifacts/eval/phase27_100_topic_binding_repair/checkpoints"
DEFAULT_INIT_NAME = "sf-10m-step1800"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_104_topic_prototype_contrastive_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_104_bounded_topic_prototype_contrastive_repair_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_104_BOUNDED_TOPIC_PROTOTYPE_CONTRASTIVE_REPAIR_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_104_BOUNDED_TOPIC_PROTOTYPE_CONTRASTIVE_REPAIR_REPORT.md"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_104_bounded_topic_prototype_contrastive_repair.md"

ALL_TOPIC_TERMS: tuple[str, ...] = (
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
    p = argparse.ArgumentParser(description="Run Phase 27.104 bounded topic prototype repair")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--pack", type=Path, default=DEFAULT_PACK)
    p.add_argument("--schedule", type=Path, default=DEFAULT_SCHEDULE)
    p.add_argument("--prototype-canary", type=Path, default=DEFAULT_PROTOTYPE_CANARY)
    p.add_argument("--topic-canary", type=Path, default=DEFAULT_TOPIC_CANARY)
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--init-checkpoints", type=Path, default=DEFAULT_INIT_ROOT)
    p.add_argument("--init-checkpoint-name", default=DEFAULT_INIT_NAME)
    p.add_argument("--steps", type=int, default=1200)
    p.add_argument("--epochs", type=int, default=8)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=96)
    p.add_argument("--lr", type=float, default=8e-5)
    p.add_argument("--warmup", type=int, default=80)
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


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(path)
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n",
        encoding="utf-8",
    )


def _check_prerequisites(args: argparse.Namespace) -> dict[str, Any]:
    decision = _load_json(args.source)
    if decision["engineering_decision"] != (
        "ALLOW_PHASE27_104_BOUNDED_TOPIC_PROTOTYPE_CONTRASTIVE_REPAIR_TRAINING"
    ):
        raise ValueError("Phase 27.103 did not allow Phase 27.104 bounded training")
    if decision.get("phase27_104_training_allowed") is not True:
        raise ValueError("Phase 27.104 training flag is not true")
    return decision


def _build_training_view(args: argparse.Namespace) -> dict[str, Any]:
    rows = _load_jsonl(args.pack)
    schedule = _load_json(args.schedule)
    ordered: list[dict[str, Any]] = []
    for item in schedule["first_32"]:
        # first_32 is only preview; use the full implied ordering from schedule fields below.
        if int(item["record_line"]) < 1:
            raise ValueError("invalid schedule record_line")

    # The schedule artifact stores full ordering compactly via first_32 only, so
    # reconstruct the same dialect-then-topic round-robin deterministically.
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in rows:
        provenance = row["provenance"]
        key = (str(provenance["topic_term"]), str(provenance["dialect"]))
        buckets.setdefault(key, []).append(row)

    topics = [
        "الوفاء",
        "التعاون",
        "الصبر",
        "الاحترام",
        "الهدوء",
        "الصدق",
        "الصداقة",
        "الشجاعة",
    ]
    dialects = ["msa", "saudi"]
    max_len = max(len(bucket) for bucket in buckets.values())
    for idx in range(max_len):
        for dialect in dialects:
            for topic in topics:
                bucket = buckets[(topic, dialect)]
                if idx < len(bucket):
                    ordered.append(bucket[idx])

    adjacent_same_topic = sum(
        1
        for left, right in zip(ordered, ordered[1:], strict=False)
        if left["provenance"]["topic_term"] == right["provenance"]["topic_term"]
    )
    view_root = args.work_dir / "curriculum_view" / "jsonl"
    view_file = view_root / "phase27_103_schedule_view.jsonl"
    _write_jsonl(view_file, ordered)
    return {
        "view_root": view_root,
        "view_file": view_file,
        "records": len(ordered),
        "adjacent_same_topic_count": adjacent_same_topic,
        "source_pack": _rel(args.pack),
        "source_schedule": _rel(args.schedule),
    }


def _topic_hits(text: str, terms: tuple[str, ...] = ALL_TOPIC_TERMS) -> list[str]:
    surface = _surface(text)
    return [term for term in terms if _surface(term) in surface]


def _observed_wrong_topics(text: str, required_topic: str) -> list[str]:
    return [term for term in _topic_hits(text) if term != required_topic]


def _copy_anchor_ok(text: str, topic: str, max_visible_arabic_chars: int = 12) -> bool:
    compact_text = "".join(_surface(text).split())
    compact_topic = "".join(_surface(topic).split())
    if not compact_topic:
        return False
    idx = compact_text.find(compact_topic)
    return idx != -1 and idx <= max_visible_arabic_chars


def _suite_rows(args: argparse.Namespace, checkpoint: str, suite_path: Path, *, canary_set: str | None) -> list[dict[str, Any]]:
    suite = _load_json(suite_path)
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=args.tokenizer,
            checkpoints_root=args.work_dir / "checkpoints",
            checkpoint_name=checkpoint,
            generator_name=f"sf_10m_phase27_104_{checkpoint}",
            model_size="sf-10m",
            seq_len=args.seq_len,
            max_new_tokens=24,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.16,
            device=args.device,
            dialogue_prompt=True,
            family_conditioning=True,
        )
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
                "forbidden_terms": list(item.get("forbidden_terms") or ()),
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
    observed_wrong = sum(len(row["observed_wrong_topics"]) for row in rows)
    copy_anchor_passed = sum(1 for row in rows if row["copy_anchor_ok"])
    required_passed = sum(1 for row in rows if row["required_ok"])
    return {
        "passed": passed,
        "total": len(rows),
        "pass_rate": round(passed / len(rows), 4) if rows else 0.0,
        "required_topic": f"{required_passed}/{len(rows)}",
        "copy_anchor": f"{copy_anchor_passed}/{len(rows)}",
        "observed_wrong_topic_count": observed_wrong,
        "observed_wrong_topic_substitutions": dict(
            Counter(term for row in rows for term in row["observed_wrong_topics"])
        ),
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
    prototype = _suite_rows(args, checkpoint, args.prototype_canary, canary_set="prototype_contrastive")
    known = _suite_rows(args, checkpoint, args.topic_canary, canary_set="known")
    fresh = _suite_rows(args, checkpoint, args.topic_canary, canary_set="fresh")
    return {
        "checkpoint": checkpoint,
        "prototype_rows": prototype,
        "prototype_summary": _summary(prototype),
        "known_topic_rows": known,
        "known_topic_summary": _summary(known),
        "fresh_topic_rows": fresh,
        "fresh_topic_summary": _summary(fresh),
        "all_family": all_family,
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    source = _check_prerequisites(args)
    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)
    training_view = _build_training_view(args)
    if training_view["records"] != 192 or training_view["adjacent_same_topic_count"] != 0:
        raise ValueError("Phase 27.104 training view failed schedule validation")

    checkpoints = args.work_dir / "checkpoints"
    train_args = [
        "--tokenizer",
        str(args.tokenizer),
        "--corpus",
        str(training_view["view_root"]),
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
        "400",
        "--seed",
        "20267104",
        "--checkpoints",
        str(checkpoints),
        "--device",
        args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        raise RuntimeError(f"training failed with exit code {train_code}")

    checkpoint_names = tuple(f"sf-10m-step{step}" for step in (400, 800, 1200))
    evaluations = [_evaluate_all(args, checkpoint) for checkpoint in checkpoint_names]
    best = max(
        evaluations,
        key=lambda row: (
            row["prototype_summary"]["passed"],
            -row["prototype_summary"]["observed_wrong_topic_count"],
            row["known_topic_summary"]["passed"],
            row["fresh_topic_summary"]["passed"],
            row["all_family"]["summary"]["passed"],
        ),
    )

    prototype_pass = int(best["prototype_summary"]["passed"])
    prototype_total = int(best["prototype_summary"]["total"])
    prototype_wrong = int(best["prototype_summary"]["observed_wrong_topic_count"])
    known_pass = int(best["known_topic_summary"]["passed"])
    known_total = int(best["known_topic_summary"]["total"])
    fresh_pass = int(best["fresh_topic_summary"]["passed"])
    fresh_total = int(best["fresh_topic_summary"]["total"])
    all_pass = int(best["all_family"]["summary"]["passed"])
    all_total = int(best["all_family"]["summary"]["total"])
    topic_family = best["all_family"]["summary"]["family_summary"].get("topic", {})
    topic_family_pass = int(topic_family.get("passed", 0))
    topic_family_total = int(topic_family.get("total", 0))

    prototype_gate = prototype_pass == prototype_total and prototype_wrong == 0
    known_gate = known_pass == known_total
    fresh_gate = fresh_pass >= 8
    topic_family_gate = topic_family_pass >= 8
    all_family_gate = all_pass >= 45
    heldout_gate_allowed = bool(
        prototype_gate and known_gate and fresh_gate and topic_family_gate and all_family_gate
    )

    decision = {
        "decision_id": "PHASE27_104_BOUNDED_TOPIC_PROTOTYPE_CONTRASTIVE_REPAIR_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_105_HELDOUT_TOPIC_PROTOTYPE_RUNTIME_GATE_NO_DIRECT_RUNTIME"
            if heldout_gate_allowed
            else "BLOCK_RUNTIME_DIAGNOSE_TOPIC_PROTOTYPE_REPAIR_RESULT"
        ),
        "training_completed": True,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "heldout_runtime_gate_allowed": heldout_gate_allowed,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "best_checkpoint": best["checkpoint"],
        "prototype_canary": f"{prototype_pass}/{prototype_total}",
        "prototype_observed_wrong_topic_count": prototype_wrong,
        "known_topic": f"{known_pass}/{known_total}",
        "fresh_topic": f"{fresh_pass}/{fresh_total}",
        "topic_family": f"{topic_family_pass}/{topic_family_total}",
        "all_family": f"{all_pass}/{all_total}",
        "required_gates": {
            "prototype_canary": "16/16",
            "prototype_observed_wrong_topic_count": 0,
            "known_topic": "16/16",
            "fresh_topic": "8/10",
            "topic_family": "8/10",
            "all_family": "45/50",
        },
        "why": (
            f"Best checkpoint {best['checkpoint']} scored prototype={prototype_pass}/{prototype_total} "
            f"with observed_wrong_topic={prototype_wrong}, known={known_pass}/{known_total}, "
            f"fresh={fresh_pass}/{fresh_total}, topic_family={topic_family_pass}/{topic_family_total}, "
            f"all_family={all_pass}/{all_total}. Runtime remains blocked."
        ),
        "next_phase": (
            "Phase 27.105 — Held-out Topic Prototype Runtime Gate"
            if heldout_gate_allowed
            else "Phase 27.105 — Topic Prototype Repair Result Diagnosis"
        ),
    }
    return {
        "phase": "Phase 27.104",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_104_TRAINED_HELDOUT_GATE_ALLOWED_RUNTIME_BLOCKED"
            if heldout_gate_allowed
            else "PHASE27_104_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_completed": True,
        "runtime_changed": False,
        "source_decision": source,
        "training_scope": "bounded SF-10M topic-prototype contrastive repair; no runtime; no SF-50M",
        "objective": "topic_prototype_contrastive_copy_anchor_repair_v1",
        "tokenizer": _rel(args.tokenizer),
        "init_checkpoint": f"{_rel(args.init_checkpoints)}/{args.init_checkpoint_name}",
        "checkpoint_root": _rel(checkpoints),
        "training_view": {
            **training_view,
            "view_root": _rel(training_view["view_root"]),
            "view_file": _rel(training_view["view_file"]),
        },
        "train_config": {
            "steps": args.steps,
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "seq_len": args.seq_len,
            "lr": args.lr,
            "warmup": args.warmup,
            "loss_scope": "assistant",
            "packing_mode": "sample_isolated",
            "curriculum_view": "phase27_103_topic_dialect_round_robin_schedule_v1",
        },
        "checkpoints": evaluations,
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.104 — Bounded Topic Prototype Contrastive Repair Training",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تدريب محدودة على SF-10M فقط. لا تفتح runtime أو الواجهة.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- best checkpoint: `{decision['best_checkpoint']}`",
        f"- prototype canary: `{decision['prototype_canary']}`",
        f"- prototype observed wrong-topic: `{decision['prototype_observed_wrong_topic_count']}`",
        f"- known topic: `{decision['known_topic']}`",
        f"- fresh topic: `{decision['fresh_topic']}`",
        f"- topic family: `{decision['topic_family']}`",
        f"- all family: `{decision['all_family']}`",
        f"- held-out gate allowed: `{decision['heldout_runtime_gate_allowed']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## Training View",
        "",
        f"- source pack: `{report['training_view']['source_pack']}`",
        f"- view file: `{report['training_view']['view_file']}`",
        f"- records: `{report['training_view']['records']}`",
        f"- adjacent same topic: `{report['training_view']['adjacent_same_topic_count']}`",
        "",
        "## Checkpoints",
        "",
    ]
    for row in report["checkpoints"]:
        lines.extend(
            [
                f"### {row['checkpoint']}",
                "",
                f"- prototype: `{row['prototype_summary']['passed']}/{row['prototype_summary']['total']}`",
                f"- prototype wrong-topic: `{row['prototype_summary']['observed_wrong_topic_count']}`",
                f"- known topic: `{row['known_topic_summary']['passed']}/{row['known_topic_summary']['total']}`",
                f"- fresh topic: `{row['fresh_topic_summary']['passed']}/{row['fresh_topic_summary']['total']}`",
                f"- all family: `{row['all_family']['summary']['passed']}/{row['all_family']['summary']['total']}`",
                f"- prototype reasons: `{row['prototype_summary']['reason_counts']}`",
                "",
            ]
        )
    lines.extend(["## القرار", "", decision["why"], ""])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_samples(path: Path, report: dict[str, Any]) -> None:
    lines = ["# Phase 27.104 Samples", ""]
    for checkpoint in report["checkpoints"]:
        lines.extend([f"## {checkpoint['checkpoint']}", ""])
        for group_name, rows in (
            ("Prototype Canary Failures", checkpoint["prototype_rows"]),
            ("Known Topic Failures", checkpoint["known_topic_rows"]),
            ("Fresh Topic Failures", checkpoint["fresh_topic_rows"]),
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
    print("SF.AI — Phase 27.104 bounded topic-prototype contrastive repair")
    print(f"status: {report['status']}")
    print(f"decision: {decision['engineering_decision']}")
    print(f"best: {decision['best_checkpoint']}")
    print(f"prototype_canary: {decision['prototype_canary']}")
    print(f"prototype_observed_wrong_topic_count: {decision['prototype_observed_wrong_topic_count']}")
    print(f"known_topic: {decision['known_topic']}")
    print(f"fresh_topic: {decision['fresh_topic']}")
    print(f"topic_family: {decision['topic_family']}")
    print(f"all_family: {decision['all_family']}")
    print(f"runtime: {'held-out gate only' if decision['heldout_runtime_gate_allowed'] else 'blocked'}")
    print(f"report: {_rel(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
