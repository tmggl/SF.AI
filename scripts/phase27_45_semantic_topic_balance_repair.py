#!/usr/bin/env python3
"""Phase 27.45 semantic topic balance repair.

Phase 27.44 fixed the weak social/planning lanes but regressed several
definition topics. This phase keeps tokenizer v6 and rebalances the curriculum
around topic-isolated definitions so each concept keeps its own surface and
does not borrow answers from neighboring concepts.
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
from scripts.phase27_33_advice_micro_stabilization import _records as phase27_33_records  # noqa: E402
from scripts.phase27_39_topic_isolation_repair import (  # noqa: E402
    BALANCED_TOPIC_REPAIR,
    _conditioned_record,
)
from scripts.phase27_43_guarded_data_backed_expansion import (  # noqa: E402
    PROBE_CASES,
    WEAK_LANE_REPAIR,
    _evaluate,
    _summary,
    _write_samples,
)
from scripts.phase27_44_tokenizer_curriculum_repair import (  # noqa: E402
    BALANCED_PLANNING_REPAIR,
    BALANCED_SOCIAL_REPAIR,
    NEW_TOPIC_REPAIR,
)
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v6_weak_lane_terms"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_45_semantic_topic_balance_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_45_semantic_topic_balance_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_45_semantic_topic_balance_repair.md"


SEMANTIC_TOPIC_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("msa", "ما معنى الصداقة", "الصداقة علاقة طيبة تقوم على الوفاء والرفقة.", ("الصداقة",), "definition"),
    RepairPair("saudi", "وش معنى الصداقة", "الصداقة رفقة طيبة ووقفة وقت الحاجة.", ("الصداقة",), "definition"),
    RepairPair("msa", "الصداقة ماذا تعني", "الصداقة مودة ووفاء بين الناس.", ("الصداقة",), "definition"),
    RepairPair("saudi", "الصداقة وش تعني", "الصداقة إنك تلقى رفيق يوقف معك.", ("الصداقة",), "definition"),
    RepairPair("msa", "ما معنى الصدق", "الصدق أن تقول الحقيقة وتلتزم بما تقول.", ("الصدق",), "definition"),
    RepairPair("saudi", "وش معنى الصدق", "الصدق يعني تقول الحقيقة بوضوح.", ("الصدق",), "definition"),
    RepairPair("msa", "اشرح الصدق بجملة", "الصدق وضوح في القول والعمل.", ("الصدق",), "definition"),
    RepairPair("saudi", "الصدق وش يعني", "الصدق إن كلامك يكون حقيقة بلا خداع.", ("الصدق",), "definition"),
    RepairPair("msa", "ما معنى التنظيم", "التنظيم ترتيب الوقت والمهام بطريقة واضحة.", ("التنظيم",), "definition"),
    RepairPair("saudi", "وش معنى التنظيم", "التنظيم إنك ترتب وقتك ومهامك بوضوح.", ("التنظيم",), "definition"),
    RepairPair("msa", "اشرح التنظيم ببساطة", "التنظيم معرفة ما تفعل ومتى تبدأ.", ("التنظيم",), "definition"),
    RepairPair("saudi", "التنظيم وش يعني", "التنظيم يعني تخلي أمورك مرتبة.", ("التنظيم",), "definition"),
    RepairPair("msa", "ما معنى الهدوء", "الهدوء سكينة تساعدك على التفكير بوضوح.", ("الهدوء",), "definition"),
    RepairPair("saudi", "وش معنى الهدوء", "الهدوء إنك تهدأ وتاخذ الأمور بروية.", ("الهدوء",), "definition"),
    RepairPair("msa", "اشرح الهدوء بجملة", "الهدوء راحة تقلل التوتر.", ("الهدوء",), "definition"),
    RepairPair("saudi", "الهدوء وش يعني", "الهدوء يعني تخفف توترك وتتكلم بروية.", ("الهدوء",), "definition"),
    RepairPair("msa", "ما معنى الوفاء", "الوفاء أن تحفظ الود وتثبت مع من تثق به.", ("الوفاء",), "definition"),
    RepairPair("saudi", "الوفاء وش يعني", "الوفاء إنك تحفظ المعروف وتوقف مع اللي تثق فيه.", ("الوفاء",), "definition"),
    RepairPair("msa", "اشرح الوفاء بجملة", "الوفاء ثبات في الود وحفظ للعهد.", ("الوفاء",), "definition"),
    RepairPair("saudi", "وش المقصود بالوفاء", "الوفاء إنك تثبت مع الناس وقت الحاجة.", ("الوفاء",), "definition"),
    RepairPair("msa", "ما معنى الشجاعة", "الشجاعة أن تفعل الصواب رغم الخوف.", ("الشجاعة",), "definition"),
    RepairPair("msa", "اشرح الشجاعة", "الشجاعة أن تفعل الصواب رغم الخوف.", ("الشجاعة",), "definition"),
    RepairPair("saudi", "الشجاعة وش تعني", "الشجاعة إنك تواجه الصح حتى لو كنت خايف.", ("الشجاعة",), "definition"),
    RepairPair("saudi", "وش المقصود بالشجاعة", "الشجاعة إنك تثبت على الصح وقت الخوف.", ("الشجاعة",), "definition"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.45 semantic topic balance repair")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--steps", type=int, default=7200)
    p.add_argument("--epochs", type=int, default=720)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=4.5e-4)
    p.add_argument("--warmup", type=int, default=180)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _records() -> list[dict[str, Any]]:
    base_train, micro_records, _repair_records = phase27_33_records()
    balanced_topic = [
        _conditioned_record(pair, 45000 + idx)
        for idx, pair in enumerate(BALANCED_TOPIC_REPAIR, start=1)
    ]
    semantic_topic = [
        _conditioned_record(pair, 46000 + idx)
        for idx, pair in enumerate(SEMANTIC_TOPIC_REPAIR, start=1)
    ]
    new_topic = [
        _conditioned_record(pair, 47000 + idx)
        for idx, pair in enumerate(NEW_TOPIC_REPAIR, start=1)
    ]
    weak = [
        _conditioned_record(pair, 48000 + idx)
        for idx, pair in enumerate(WEAK_LANE_REPAIR, start=1)
    ]
    social = [
        _conditioned_record(pair, 49000 + idx)
        for idx, pair in enumerate(BALANCED_SOCIAL_REPAIR, start=1)
    ]
    planning = [
        _conditioned_record(pair, 50000 + idx)
        for idx, pair in enumerate(BALANCED_PLANNING_REPAIR, start=1)
    ]

    records: list[dict[str, Any]] = []
    records.extend(base_train)
    records.extend(micro_records)
    for _ in range(48):
        records.extend(balanced_topic)
    for _ in range(58):
        records.extend(semantic_topic)
    for _ in range(34):
        records.extend(new_topic)
    for _ in range(12):
        records.extend(weak)
    for _ in range(10):
        records.extend(social)
    for _ in range(10):
        records.extend(planning)
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
        "--seed", "20260615",
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
        "PASSED_SEMANTIC_TOPIC_BALANCE_READY_FOR_GUARDED_SWITCH"
        if all_passed
        else "PARTIAL_SEMANTIC_TOPIC_BALANCE_KEEP_PHASE27_40_RUNTIME"
    )
    report = {
        "phase": "Phase 27.45",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "SF-10M semantic topic balance repair only; no scaling",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_45",
        "train_records": len(records),
        "summary": summary,
        "runtime_switch_allowed": all_passed,
        "sf50m_allowed": False,
        "phase28_allowed": False,
        "previous_phase27_44": {
            "status": "PARTIAL_TOKENIZER_CURRICULUM_REPAIR_KEEP_PHASE27_40_RUNTIME",
            "passed": 11,
            "total": 16,
        },
        "next_phase": (
            "Phase 27.46 — guarded runtime switch for phase27_45"
            if all_passed
            else "Phase 27.46 — inspect remaining semantic blockers"
        ),
        "torch_version": torch.__version__,
        "rows": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)

    print("SF.AI — Phase 27.45 semantic topic balance repair")
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
