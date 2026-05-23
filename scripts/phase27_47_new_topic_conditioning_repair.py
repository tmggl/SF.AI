#!/usr/bin/env python3
"""Phase 27.47 new-topic conditioning repair.

Phase 27.46 reached 14/16, with only "الوفاء" and "الشجاعة" failing. Root
cause: the inherited training record builder did not emit a topic condition
line for those two new topics, while evaluation/runtime prompts do. This phase
uses an extended conditioner so train and eval formats match.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import _latest_checkpoint_name  # noqa: E402
from scripts.phase27_19_hygiene_repair_probe import _write_probe_corpus  # noqa: E402
from scripts.phase27_26_heldout_objective_repair import RepairPair, _rel  # noqa: E402
from scripts.phase27_43_guarded_data_backed_expansion import (  # noqa: E402
    PROBE_CASES,
    _evaluate,
    _summary,
    _write_samples,
)
from scripts.phase27_46_core_dialogue_stabilization import CORE_DIALOGUE_REPAIR  # noqa: E402
from sf_ai.modules.chat.native_generator import _intent_label  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v6_weak_lane_terms"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_47_new_topic_conditioning_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_47_new_topic_conditioning_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_47_new_topic_conditioning_repair.md"


EXTRA_NEW_TOPIC_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("msa", "ما معنى الوفاء", "الوفاء أن تحفظ الود وتثبت مع من تثق به.", ("الوفاء",), "definition"),
    RepairPair("msa", "اشرح الوفاء", "الوفاء ثبات في الود وحفظ للعهد.", ("الوفاء",), "definition"),
    RepairPair("saudi", "الوفاء وش يعني", "الوفاء إنك تحفظ المعروف وتوقف مع اللي تثق فيه.", ("الوفاء",), "definition"),
    RepairPair("saudi", "وش معنى الوفاء", "الوفاء إنك تثبت مع الناس وقت الحاجة.", ("الوفاء",), "definition"),
    RepairPair("msa", "اشرح الشجاعة", "الشجاعة أن تفعل الصواب رغم الخوف.", ("الشجاعة",), "definition"),
    RepairPair("msa", "ما معنى الشجاعة", "الشجاعة ثبات على الصواب وقت الخوف.", ("الشجاعة",), "definition"),
    RepairPair("saudi", "الشجاعة وش تعني", "الشجاعة إنك تواجه الصح حتى لو كنت خايف.", ("الشجاعة",), "definition"),
    RepairPair("saudi", "وش معنى الشجاعة", "الشجاعة إنك تثبت على الصح وقت الخوف.", ("الشجاعة",), "definition"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.47 new-topic conditioning repair")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--steps", type=int, default=4600)
    p.add_argument("--epochs", type=int, default=460)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=5.5e-4)
    p.add_argument("--warmup", type=int, default=100)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _surface(text: str) -> str:
    return (
        (text or "")
        .replace("أ", "ا")
        .replace("إ", "ا")
        .replace("آ", "ا")
        .replace("ى", "ي")
        .replace("ة", "ه")
        .strip()
        .lower()
    )


def _topic_for_text(text: str) -> str:
    surface = _surface(text)
    topic_stems = {
        "التعاون": ("تعاون",),
        "الصبر": ("صبر",),
        "الاحترام": ("احترام",),
        "القراءة": ("قراء", "قراي"),
        "الصداقة": ("صداق",),
        "الصدق": ("صدق",),
        "التنظيم": ("تنظيم",),
        "الهدوء": ("هدوء",),
        "الوفاء": ("وفاء",),
        "الشجاعة": ("شجاع",),
    }
    for topic, stems in topic_stems.items():
        if any(stem in surface for stem in stems):
            return topic
    return ""


def _conditioned_record(pair: RepairPair, idx: int) -> dict[str, Any]:
    messages: list[dict[str, str]] = []
    label = _intent_label(pair.category)
    topic = _topic_for_text(pair.prompt)
    if label:
        messages.append({"role": "system", "content": f"النية: {label}"})
    if topic:
        messages.append({"role": "system", "content": f"المصطلح: {topic}"})
    messages.extend(
        [
            {"role": "user", "content": pair.prompt},
            {"role": "assistant", "content": pair.answer},
        ]
    )
    return {
        "id": f"phase27_47_{pair.dialect}_{idx:04d}",
        "messages": messages,
        "expected_terms": list(pair.expected_terms),
        "provenance": {
            "source": f"sf-ai-phase27-47-new-topic-conditioning-{pair.dialect}",
            "license": "owner-delegated-internal-sf-ai",
            "training_allowed": True,
            "quality": "gold",
            "dialect": pair.dialect,
            "owner_user_id": "sami-local",
            "created_by_user_id": "sf-ai-agent",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
            "synthetic_llm_data": False,
            "notes": "internal core dialogue conditioning repair; excludes operational/project-management dialogue",
        },
    }


def _records() -> list[dict[str, Any]]:
    core = [
        _conditioned_record(pair, 47000 + idx)
        for idx, pair in enumerate(CORE_DIALOGUE_REPAIR, start=1)
    ]
    new_topic = [
        _conditioned_record(pair, 48000 + idx)
        for idx, pair in enumerate(EXTRA_NEW_TOPIC_REPAIR, start=1)
    ]
    records: list[dict[str, Any]] = []
    for _ in range(150):
        records.extend(core)
    for _ in range(120):
        records.extend(new_topic)
    return records


def main() -> int:
    args = parse_args()
    if not (args.tokenizer / "meta.json").exists():
        print(f"error: missing tokenizer at {args.tokenizer}; run Phase 27.44 first", file=sys.stderr)
        return 1
    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)

    corpus_dir = args.work_dir / "corpus"
    checkpoints = args.work_dir / "checkpoints"
    records = _records()
    _write_probe_corpus(corpus_dir, records)

    train_args = [
        "--tokenizer", str(args.tokenizer),
        "--corpus", str(corpus_dir),
        "--size", "sf-10m",
        "--steps", str(args.steps),
        "--epochs", str(args.epochs),
        "--batch-size", str(args.batch_size),
        "--seq-len", str(args.seq_len),
        "--stream-format", "dialogue",
        "--loss-scope", "assistant",
        "--packing-mode", "sample_isolated",
        "--lr", str(args.lr),
        "--warmup", str(args.warmup),
        "--min-lr", "1e-5",
        "--save-every", str(args.steps),
        "--seed", "20260617",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return train_code

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    rows = _evaluate(
        tokenizer=args.tokenizer,
        checkpoints_root=checkpoints,
        checkpoint_name=checkpoint_name,
        device=args.device,
    )
    summary = _summary(rows)
    all_passed = summary["passed"] == summary["total"]
    status = (
        "PASSED_NEW_TOPIC_CONDITIONING_READY_FOR_GUARDED_SWITCH"
        if all_passed
        else "PARTIAL_NEW_TOPIC_CONDITIONING_KEEP_PHASE27_40_RUNTIME"
    )
    report = {
        "phase": "Phase 27.47",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "SF-10M new-topic conditioning repair only; no scaling",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_47",
        "train_records": len(records),
        "probe_case_count": len(PROBE_CASES),
        "conditioning_repair": {
            "added_topic_line_for": ["الوفاء", "الشجاعة"],
            "train_eval_format_aligned": True,
        },
        "summary": summary,
        "runtime_switch_allowed": all_passed,
        "sf50m_allowed": False,
        "phase28_allowed": False,
        "previous_phase27_46": {"passed": 14, "total": 16},
        "next_phase": (
            "Phase 27.48 — guarded runtime switch for phase27_47"
            if all_passed
            else "Phase 27.48 — inspect remaining conditioning blockers"
        ),
        "torch_version": torch.__version__,
        "rows": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)

    print("SF.AI — Phase 27.47 new-topic conditioning repair")
    print(f"  status      : {status}")
    print(f"  tokenizer   : {_rel(args.tokenizer)}")
    print(f"  checkpoint  : {checkpoint_name}")
    print(f"  train rows  : {len(records)}")
    print(f"  cases       : {summary['passed']}/{summary['total']}")
    for bucket, item in summary["bucket_summary"].items():
        print(f"  {bucket:<12}: {item['passed']}/{item['total']}")
    print(f"  reasons     : {summary['reason_counts']}")
    print(f"  report      : {args.report}")
    print(f"  samples     : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
