#!/usr/bin/env python3
"""Phase 27.74 targeted open_social semantic-collapse repair.

Phase 27.73 proved that one remaining failure is a guard gap and the other is
a semantic family collapse: an open_social prompt receives a topic definition.
This phase trains very small SF-10M repair candidates from the Phase 27.72
checkpoint, evaluates each against:

1. Phase 27.69 new fresh shadow.
2. Phase 27.67 known shadow.
3. Phase 27.60 broader regression.

Runtime remains blocked unless every gate passes, and even then a later live
review phase is required before UI exposure.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import _latest_checkpoint_name  # noqa: E402
from scripts.phase27_19_hygiene_repair_probe import _write_probe_corpus  # noqa: E402
from scripts.phase27_26_heldout_objective_repair import RepairPair, _rel  # noqa: E402
from scripts.phase27_39_topic_isolation_repair import _conditioned_record  # noqa: E402
from scripts.phase27_60_broader_natural_dialogue_canary import _evaluate as evaluate_phase27_60, _summary as summary_phase27_60  # noqa: E402
from scripts.phase27_67_fresh_shadow_canary import _evaluate as evaluate_phase27_67, _summary as summary_phase27_67  # noqa: E402
from scripts.phase27_69_new_fresh_shadow_canary import _evaluate as evaluate_phase27_69, _summary as summary_phase27_69  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v8_phase27_65"
DEFAULT_INIT_CHECKPOINTS = ROOT / "artifacts/eval/phase27_72_stability_first_repair/checkpoints"
DEFAULT_INIT_CHECKPOINT_NAME = "sf-10m-step64"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_74_open_social_semantic_collapse_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_74_open_social_semantic_collapse_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_74_open_social_semantic_collapse_repair.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_74_OPEN_SOCIAL_SEMANTIC_COLLAPSE_REPAIR_REPORT.md"


@dataclass(frozen=True)
class CandidateConfig:
    name: str
    steps: int
    epochs: int
    lr: float
    warmup: int
    repeat: int
    min_lr: float


DEFAULT_CANDIDATES: tuple[CandidateConfig, ...] = (
    CandidateConfig("gentle_48", steps=48, epochs=48, lr=3e-6, warmup=8, repeat=32, min_lr=1e-6),
    CandidateConfig("balanced_72", steps=72, epochs=72, lr=5e-6, warmup=10, repeat=40, min_lr=1e-6),
    CandidateConfig("focused_96", steps=96, epochs=96, lr=7e-6, warmup=12, repeat=48, min_lr=1e-6),
)


OPEN_SOCIAL_SEMANTIC_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("msa", "لنختر موضوعًا صغيرًا", "نختار موضوعًا صغيرًا وخفيفًا للكلام.", ("موضوع", "صغير"), "open_social"),
    RepairPair("msa", "لنختر موضوعًا صغيرًا", "نبدأ بموضوع صغير وخفيف ونتحدث عنه بهدوء.", ("موضوع", "صغير", "نبدأ"), "open_social"),
    RepairPair("msa", "لنختر موضوعًا صغيرًا", "موضوع صغير مناسب: نتحدث عن شيء لطيف من يومك.", ("موضوع", "صغير"), "open_social"),
    RepairPair("msa", "اختر موضوعًا صغيرًا", "نختار موضوعًا صغيرًا ونبدأ الكلام عنه ببساطة.", ("موضوع", "صغير", "نبدأ"), "open_social"),
    RepairPair("msa", "أريد موضوعًا صغيرًا للكلام", "نختار موضوعًا صغيرًا وخفيفًا للكلام.", ("موضوع", "صغير"), "open_social"),
    RepairPair("msa", "افتح موضوعًا صغيرًا", "نفتح موضوعًا صغيرًا وبسيطًا، مثل شيء لطيف حدث اليوم.", ("موضوع", "صغير"), "open_social"),
    RepairPair("msa", "ابدأ محادثة سهلة", "نبدأ محادثة سهلة عن موضوع بسيط.", ("محادثة", "نبدأ", "موضوع"), "open_social"),
    RepairPair("msa", "ابدأ محادثة سهلة", "نبدأ بسؤال خفيف عن يومك أو موضوع بسيط.", ("نبدأ", "موضوع", "يومك"), "open_social"),
    RepairPair("saudi", "ودي بموضوع سوالف", "نختار موضوع سوالف خفيف ونسولف عنه.", ("موضوع", "سوالف", "نسولف"), "open_social"),
    RepairPair("saudi", "ودي بموضوع سوالف", "أبشر، نسولف عن موضوع خفيف من يومك.", ("نسولف", "موضوع", "يومك"), "open_social"),
    RepairPair("saudi", "ابي موضوع سوالف", "موضوع سوالف خفيف: نسولف عن شيء صار في يومك.", ("موضوع", "سوالف", "نسولف"), "open_social"),
    RepairPair("saudi", "هات موضوع سوالف", "نختار موضوع سوالف بسيط ونبدأ فيه بهدوء.", ("موضوع", "سوالف"), "open_social"),
)


FAMILY_SEPARATION_PRESERVE: tuple[RepairPair, ...] = (
    # Topic definitions must stay definitions when the prompt actually asks for
    # meaning. This prevents the open_social repair from flattening topic lanes.
    RepairPair("msa", "ما معنى التعاون", "التعاون مشاركة الجهد بين الناس.", ("التعاون",), "topic"),
    RepairPair("saudi", "التعاون وش يعني", "التعاون إنك تساعد غيرك وتنجزون سوا.", ("التعاون",), "topic"),
    RepairPair("msa", "اشرح التعاون باختصار", "التعاون أن يعمل الناس معًا لهدف مشترك.", ("التعاون",), "topic"),
    RepairPair("msa", "ما معنى الصداقة", "الصداقة رفقة طيبة واهتمام وقت الحاجة.", ("الصداقة",), "topic"),
    RepairPair("msa", "ما الخطوة بعد هذا الشرح", "بعدها نكمل بخطوة أوضح من الفكرة.", ("بعدها", "خطوة"), "followup"),
    RepairPair("saudi", "وش قصدك بالضبط", "أقصد المعنى ببساطة، ونوضحه خطوة خطوة.", ("أقصد", "خطوة"), "followup"),
    RepairPair("msa", "كيف أقسم وقتي اليوم", "اكتب خطة قصيرة: مهمة واحدة الآن، ثم خطوة بعدها.", ("خطة", "مهمة", "خطوة"), "planning"),
    RepairPair("saudi", "ابي ارتب اولوياتي اليوم", "رتب أولوياتك: اختر الأهم وابدأ بخطوة واحدة.", ("رتب", "أولويات", "ابدأ"), "planning"),
    RepairPair("msa", "كيف أهدئ نفسي الآن", "تنفس بهدوء وخذ لحظة راحة قصيرة.", ("تنفس", "راحة"), "support"),
    RepairPair("saudi", "صدري ضايق وابغى اهدأ", "خذ نفسًا هادئًا وخفف الضغط خطوة خطوة.", ("نفس", "خفف"), "support"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.74 open_social semantic-collapse repair")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=80)
    p.add_argument("--device", default="auto")
    p.add_argument("--init-checkpoints", type=Path, default=DEFAULT_INIT_CHECKPOINTS)
    p.add_argument("--init-checkpoint-name", default=DEFAULT_INIT_CHECKPOINT_NAME)
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--candidate", action="append", help="Run only named candidate(s)")
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _records(repeat: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    idx = 74000
    for _ in range(repeat):
        for pair in (*OPEN_SOCIAL_SEMANTIC_REPAIR, *FAMILY_SEPARATION_PRESERVE):
            idx += 1
            records.append(_conditioned_record(pair, idx))
    return records


def _candidate_score(
    summary_69: dict[str, Any],
    summary_67: dict[str, Any],
    summary_60: dict[str, Any],
) -> tuple[int, int, int, int]:
    total = int(summary_69["passed"]) + int(summary_67["passed"]) + int(summary_60["passed"])
    open_social = int(summary_69["family_summary"]["open_social"]["passed"])
    known = int(summary_67["passed"])
    regression = int(summary_60["passed"])
    return total, open_social, known, regression


def _failed_rows(*groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in groups:
        rows.extend(row for row in group if not row["passed"])
    return rows


def _evaluate_candidate(args: argparse.Namespace, cfg: CandidateConfig) -> dict[str, Any]:
    candidate_dir = args.work_dir / cfg.name
    if candidate_dir.exists() and not args.keep_work:
        shutil.rmtree(candidate_dir)
    corpus_dir = candidate_dir / "corpus"
    checkpoints = candidate_dir / "checkpoints"
    records = _records(cfg.repeat)
    _write_probe_corpus(corpus_dir, records)

    train_args = [
        "--tokenizer", str(args.tokenizer),
        "--corpus", str(corpus_dir),
        "--size", "sf-10m",
        "--steps", str(cfg.steps),
        "--epochs", str(cfg.epochs),
        "--batch-size", str(args.batch_size),
        "--seq-len", str(args.seq_len),
        "--stream-format", "dialogue",
        "--loss-scope", "assistant",
        "--packing-mode", "sample_isolated",
        "--lr", str(cfg.lr),
        "--warmup", str(cfg.warmup),
        "--min-lr", str(cfg.min_lr),
        "--save-every", str(cfg.steps),
        "--seed", "20260704",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
        "--init-checkpoints", str(args.init_checkpoints),
        "--init-checkpoint-name", args.init_checkpoint_name,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return {
            "candidate": cfg.name,
            "status": "TRAINING_FAILED",
            "train_code": train_code,
            "passed": False,
        }

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    eval_args = argparse.Namespace(
        tokenizer=args.tokenizer,
        checkpoints=checkpoints,
        checkpoint_name=checkpoint_name,
        device=args.device,
    )
    rows_69 = evaluate_phase27_69(eval_args)
    rows_67 = evaluate_phase27_67(eval_args)
    rows_60 = evaluate_phase27_60(eval_args)
    summary_69 = summary_phase27_69(rows_69)
    summary_67 = summary_phase27_67(rows_67)
    summary_60 = summary_phase27_60(rows_60)
    passed = (
        summary_69["passed"] == summary_69["total"]
        and summary_67["passed"] == summary_67["total"]
        and summary_60["passed"] == summary_60["total"]
    )
    return {
        "candidate": cfg.name,
        "config": {
            "steps": cfg.steps,
            "epochs": cfg.epochs,
            "lr": cfg.lr,
            "warmup": cfg.warmup,
            "repeat": cfg.repeat,
            "min_lr": cfg.min_lr,
        },
        "status": "PASSED_ALL_GATES" if passed else "FAILED_GATES",
        "passed": passed,
        "train_records": len(records),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": f"sf_10m_phase27_74_{cfg.name}",
        "phase27_69_summary": summary_69,
        "phase27_67_summary": summary_67,
        "phase27_60_summary": summary_60,
        "score": list(_candidate_score(summary_69, summary_67, summary_60)),
        "phase27_69_rows": rows_69,
        "phase27_67_rows": rows_67,
        "phase27_60_rows": rows_60,
        "failures": _failed_rows(rows_69, rows_67, rows_60),
    }


def _write_samples(path: Path, report: dict[str, Any]) -> None:
    lines = ["# Phase 27.74 Open-Social Semantic-Collapse Repair", ""]
    best = report["selected_candidate"]
    lines.extend(
        [
            f"- selected candidate: `{best['candidate']}`",
            f"- status: `{best['status']}`",
            f"- Phase 27.69: `{best['phase27_69_summary']['passed']}/{best['phase27_69_summary']['total']}`",
            f"- Phase 27.67: `{best['phase27_67_summary']['passed']}/{best['phase27_67_summary']['total']}`",
            f"- Phase 27.60: `{best['phase27_60_summary']['passed']}/{best['phase27_60_summary']['total']}`",
            "",
        ]
    )
    for candidate in report["candidates"]:
        lines.extend([f"## {candidate['candidate']}", ""])
        lines.append(f"- score: `{candidate.get('score')}`")
        if not candidate.get("failures"):
            lines.extend(["- failures: none", ""])
            continue
        for row in candidate["failures"]:
            lines.extend(
                [
                    f"### {row['id']} — FAIL",
                    "",
                    f"- family: {row['family']}",
                    f"- prompt: {row['prompt']}",
                    f"- response: {row['response']}",
                    f"- guard_reason: {row.get('guard_reason')}",
                    f"- reason: {row['reason']}",
                    "",
                ]
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    best = report["selected_candidate"]
    lines = [
        "# Phase 27.74 — Open-Social Semantic-Collapse Repair",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تدريب إصلاح ضيقة على انهيار `open_social` إلى تعريفات موضوعية. لا تفتح runtime تلقائيًا.",
        "",
        f"- status: `{report['status']}`",
        f"- tokenizer: `{report['tokenizer']}`",
        f"- init checkpoint: `{report['init_checkpoint_root']}/{report['init_checkpoint_name']}`",
        f"- selected candidate: `{best['candidate']}`",
        f"- checkpoint: `{best.get('checkpoint_root')}/{best.get('checkpoint_name')}`",
        f"- Phase 27.69 fresh: `{best['phase27_69_summary']['passed']}/{best['phase27_69_summary']['total']}`",
        f"- Phase 27.67 known: `{best['phase27_67_summary']['passed']}/{best['phase27_67_summary']['total']}`",
        f"- Phase 27.60 regression: `{best['phase27_60_summary']['passed']}/{best['phase27_60_summary']['total']}`",
        f"- runtime switch allowed: `{report['decisions']['runtime_switch_allowed']}`",
        "",
        "## القرار",
        "",
        report["decision"],
        "",
        "## التالي",
        "",
        report["next_phase"],
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    if not (args.tokenizer / "meta.json").exists():
        print(f"error: missing tokenizer at {args.tokenizer}", file=sys.stderr)
        return 1
    init_dir = args.init_checkpoints / args.init_checkpoint_name
    if not (init_dir / "meta.json").exists() or not (init_dir / "state.pt").exists():
        print(f"error: missing init checkpoint at {init_dir}", file=sys.stderr)
        return 1
    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)

    selected_names = set(args.candidate or [])
    configs = [
        cfg for cfg in DEFAULT_CANDIDATES
        if not selected_names or cfg.name in selected_names
    ]
    if not configs:
        print(f"error: no candidate selected from {', '.join(c.name for c in DEFAULT_CANDIDATES)}", file=sys.stderr)
        return 1

    candidates = [_evaluate_candidate(args, cfg) for cfg in configs]
    valid = [item for item in candidates if item.get("score")]
    if not valid:
        return 1
    selected = max(valid, key=lambda item: tuple(item["score"]))
    all_gates = bool(selected["passed"])
    improved = (
        selected["phase27_69_summary"]["passed"] >= 58
        and selected["phase27_67_summary"]["passed"] >= 50
        and selected["phase27_60_summary"]["passed"] >= 30
    )
    status = (
        "PASSED_OPEN_SOCIAL_SEMANTIC_COLLAPSE_REPAIR_RUNTIME_REVIEW_ALLOWED"
        if all_gates
        else (
            "IMPROVED_OPEN_SOCIAL_SEMANTIC_COLLAPSE_REPAIR_RUNTIME_BLOCKED"
            if improved
            else "FAILED_OPEN_SOCIAL_SEMANTIC_COLLAPSE_REPAIR_RUNTIME_BLOCKED"
        )
    )
    report = {
        "phase": "Phase 27.74",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "targeted SF-10M open_social semantic-collapse repair from Phase 27.72; no runtime switch; no SF-50M",
        "tokenizer": _rel(args.tokenizer),
        "init_checkpoint_root": _rel(args.init_checkpoints),
        "init_checkpoint_name": args.init_checkpoint_name,
        "repair_pair_count": len(OPEN_SOCIAL_SEMANTIC_REPAIR),
        "family_preserve_pair_count": len(FAMILY_SEPARATION_PRESERVE),
        "candidates": candidates,
        "selected_candidate": selected,
        "decisions": {
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
            "live_runtime_review_allowed": all_gates,
            "repair_required_before_runtime": not all_gates,
        },
        "decision": (
            "The targeted repair passed all offline gates. Runtime still requires a separate guarded live review phase."
            if all_gates
            else "The targeted repair did not pass all gates. Keep runtime blocked and inspect the selected candidate failures before any UI/runtime change."
        ),
        "next_phase": (
            "Phase 27.75 — guarded live review for Phase 27.74 candidate"
            if all_gates
            else "Phase 27.75 — inspect Phase 27.74 failures and revise open_social strategy"
        ),
        "torch_version": torch.__version__,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, report)
    _write_doc(args.doc, report)

    print("SF.AI — Phase 27.74 open_social semantic-collapse repair")
    print(f"  status      : {status}")
    print(f"  selected    : {selected['candidate']}")
    print(f"  checkpoint  : {selected.get('checkpoint_name')}")
    print(f"  phase27.69  : {selected['phase27_69_summary']['passed']}/{selected['phase27_69_summary']['total']}")
    print(f"  phase27.67  : {selected['phase27_67_summary']['passed']}/{selected['phase27_67_summary']['total']}")
    print(f"  phase27.60  : {selected['phase27_60_summary']['passed']}/{selected['phase27_60_summary']['total']}")
    print(f"  report      : {_rel(args.report)}")
    print("  runtime     : blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
