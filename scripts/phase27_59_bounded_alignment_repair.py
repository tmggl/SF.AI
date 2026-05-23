#!/usr/bin/env python3
"""Phase 27.59 bounded alignment repair.

Phase 27.58 proved tokenizer v7 fixed protected phrase splitting, but the
bounded generator still confused response families. This phase keeps tokenizer
v7, trains a small repair-only SF-10M probe, and evaluates the same bounded
families before any runtime switch.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
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
from scripts.phase27_58_tokenizer_bounded_alignment_probe import (  # noqa: E402
    AlignmentCase,
    PROBE_CASES,
    _expected_ok,
    _family_terms,
    _surface,
)
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v7_phase27_58"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_59_bounded_alignment_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_59_bounded_alignment_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_59_bounded_alignment_repair.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_59_BOUNDED_ALIGNMENT_REPAIR_REPORT.md"


ALIGNMENT_REPAIR: tuple[RepairPair, ...] = (
    # open_social: must not collapse into thanks/planning.
    RepairPair("saudi", "وش ودك نسولف عنه", "أكيد، نقدر نسولف عن موضوع خفيف أو عن يومك.", ("نسولف", "موضوع"), "open_social"),
    RepairPair("saudi", "هات سالفة خفيفة", "خلنا نختار موضوع خفيف من يومك ونسولف عنه.", ("موضوع", "يومك"), "open_social"),
    RepairPair("msa", "أريد كلامًا خفيفًا", "نبدأ بموضوع بسيط وخفيف عن يومك.", ("نبدأ", "موضوع"), "open_social"),
    RepairPair("saudi", "سولف معي", "أبشر، خلنا نسولف عن موضوع خفيف.", ("نسولف", "موضوع"), "open_social"),
    RepairPair("saudi", "وش عندك من سالفة", "عندي موضوع خفيف: وش أفضل شي صار في يومك؟", ("موضوع", "يومك"), "open_social"),
    RepairPair("msa", "افتح حديثًا بسيطًا", "نبدأ بحديث خفيف عن شيء لطيف في يومك.", ("نبدأ", "يومك"), "open_social"),
    # followup: continuation/clarification, not thanks or task planning.
    RepairPair("saudi", "يعني كيف", "أقصد ابدأ بشي صغير ثم كمل بعده بهدوء.", ("أقصد", "ابدأ"), "followup"),
    RepairPair("msa", "اشرحها أكثر", "أقصد أن الفكرة أبسط: ابدأ بالجزء الواضح ثم أكمل.", ("أقصد", "ابدأ"), "followup"),
    RepairPair("saudi", "طيب بعدين", "بعدها شوف النتيجة وكمل على الشيء المناسب.", ("بعدها", "كمل"), "followup"),
    RepairPair("saudi", "وضح لي", "أقصد لا تستعجل؛ خذ الجزء الأول وافهمه ثم كمل.", ("أقصد", "كمل"), "followup"),
    RepairPair("msa", "ماذا تقصد", "أقصد أن تبدأ بالواضح ثم تنتقل لما بعده.", ("أقصد", "بعده"), "followup"),
    RepairPair("saudi", "كمل كلامك", "نكمل: الفكرة إنك تختار الأسهل ثم تبني عليه.", ("نكمل", "الفكرة"), "followup"),
    # planning/support regressions.
    RepairPair("msa", "كيف أنظم يومي", "اكتب ثلاث مهام وابدأ بالأهم.", ("مهام", "ابدأ"), "planning"),
    RepairPair("saudi", "ابي ارتب يومي", "ابدأ بشي واحد واضح، ثم انتقل للخطوة التالية.", ("ابدأ", "خطوة"), "planning"),
    RepairPair("msa", "دلني على بداية عملية", "اختر مهمة واحدة وابدأ بها الآن.", ("مهمة", "ابدأ"), "planning"),
    RepairPair("saudi", "توترت شوي", "خذ نفسًا هادئًا وركز على خطوة واحدة.", ("نفس", "خطوة"), "support"),
    RepairPair("msa", "أحتاج أهدأ", "تنفس بهدوء وامنح نفسك لحظة قصيرة.", ("تنفس", "بهدوء"), "support"),
    RepairPair("saudi", "طمني", "تقدر تهدأ خطوة خطوة، خذ نفس وابدأ بهدوء.", ("تهدأ", "خطوة"), "support"),
    # topic isolation: each topic must keep its own term.
    RepairPair("msa", "ما معنى الصداقة", "الصداقة رفقة طيبة واهتمام وقت الحاجة.", ("الصداقة",), "topic"),
    RepairPair("saudi", "الشجاعة وش تعني", "الشجاعة إنك تسوي الصح حتى لو كنت خايف.", ("الشجاعة",), "topic"),
    RepairPair("msa", "اشرح الصدق", "الصدق أن تقول الحقيقة بوضوح وتلتزم بها.", ("الصدق",), "topic"),
    RepairPair("msa", "ما معنى الهدوء", "الهدوء سكينة تخفف التوتر وتوضح التفكير.", ("الهدوء",), "topic"),
    RepairPair("saudi", "الصداقة وش تعني", "الصداقة رفقة ووقفة صادقة وقت الحاجة.", ("الصداقة",), "topic"),
    RepairPair("saudi", "الصدق وش يعني", "الصدق إن كلامك يكون واضح وما فيه خداع.", ("الصدق",), "topic"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.59 bounded alignment repair")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--steps", type=int, default=6400)
    p.add_argument("--epochs", type=int, default=640)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=80)
    p.add_argument("--lr", type=float, default=7e-4)
    p.add_argument("--warmup", type=int, default=160)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _records() -> list[dict[str, Any]]:
    repair = [
        _conditioned_record(pair, 59000 + idx)
        for idx, pair in enumerate(ALIGNMENT_REPAIR, start=1)
    ]
    records: list[dict[str, Any]] = []
    for _ in range(120):
        records.extend(repair)
    return records


_FORBIDDEN_BY_FAMILY: dict[str, tuple[str, ...]] = {
    "open_social": ("العفو", "مهام", "الأهم", "اولوية", "اولويات", "نفس", "تنفس"),
    "followup": ("العفو", "مهام", "اولويات", "نفس", "تنفس"),
    "planning": ("العفو", "نسولف", "يومك", "نفس", "تنفس"),
    "support": ("العفو", "مهام", "الصداقة", "الشجاعة", "الصدق"),
    "topic": ("مهام", "اولويات", "نفس", "تنفس"),
}


def _family_ok(text: str, family: str, families: dict[str, tuple[str, ...]]) -> bool:
    surface = _surface(text)
    allowed = any(_surface(term) in surface for term in families.get(family, ()))
    forbidden = any(_surface(term) in surface for term in _FORBIDDEN_BY_FAMILY.get(family, ()))
    return allowed and not forbidden


def _evaluate(args: argparse.Namespace, checkpoint_name: str) -> list[dict[str, Any]]:
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=args.tokenizer,
            checkpoints_root=args.work_dir / "checkpoints",
            checkpoint_name=checkpoint_name,
            generator_name="sf_10m_phase27_59_alignment_repair",
            model_size="sf-10m",
            seq_len=args.seq_len,
            max_new_tokens=26,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.12,
            device=args.device,
            dialogue_prompt=True,
        )
    )
    guard = GenerationGuard(min_chars=4)
    families = _family_terms()
    rows: list[dict[str, Any]] = []
    for case in PROBE_CASES:
        out = generator.generate(
            case.prompt,
            dialect=case.dialect,
            intent=case.intent,
            topic=case.topic,
            max_new_tokens=26,
            temperature=1.0,
            top_k=0,
        )
        verdict = guard.inspect(out.text) if case.family == "topic" else guard.inspect_for_prompt(case.prompt, out.text)
        expected = _expected_ok(out.text, case.expected_terms)
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
                "expected_terms": list(case.expected_terms),
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
    families = sorted({str(row["family"]) for row in rows})
    passed = sum(1 for row in rows if row["passed"])
    return {
        "passed": passed,
        "total": len(rows),
        "pass_rate": round(passed / len(rows), 4) if rows else 0.0,
        "family_summary": {
            family: {
                "passed": sum(1 for row in rows if row["family"] == family and row["passed"]),
                "total": sum(1 for row in rows if row["family"] == family),
            }
            for family in families
        },
        "reason_counts": dict(Counter(str(row["reason"]) for row in rows)),
    }


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.59 Bounded Alignment Repair", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- family: {row['family']}",
                f"- prompt: {row['prompt']}",
                f"- response: {row['response']}",
                f"- guard_reason: {row['guard_reason']}",
                f"- expected_ok: {row['expected_ok']}",
                f"- family_ok: {row['family_ok']}",
                f"- reason: {row['reason']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_doc(report: dict[str, Any], path: Path) -> None:
    summary = report["summary"]
    lines = [
        "# Phase 27.59 — Bounded Alignment Repair",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تدريب repair محدودة على tokenizer v7. لا تفتح الواجهة ولا تغيّر runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- tokenizer: `{report['tokenizer']}`",
        f"- train records: `{report['train_records']}`",
        f"- probe pass: `{summary['passed']}/{summary['total']}`",
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
        "--seed", "20260625",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return train_code

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    rows = _evaluate(args, checkpoint_name)
    summary = _summary(rows)
    passed = summary["passed"] == summary["total"]
    status = (
        "PASSED_BOUNDED_ALIGNMENT_REPAIR_READY_FOR_BROADER_CANARY_RUNTIME_BLOCKED"
        if passed
        else "FAILED_BOUNDED_ALIGNMENT_REPAIR_RUNTIME_BLOCKED"
    )

    report = {
        "phase": "Phase 27.59",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "bounded SF-10M alignment repair only; no runtime switch; no SF-50M",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_59_alignment_repair",
        "train_records": len(records),
        "repair_pair_count": len(ALIGNMENT_REPAIR),
        "summary": summary,
        "rows": rows,
        "decisions": {
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
            "broader_canary_allowed": passed,
        },
        "decision": (
            "Bounded alignment repair passed. Keep runtime blocked and run a broader natural-dialogue canary next."
            if passed
            else "Bounded alignment repair failed. Keep runtime blocked and inspect remaining family failures."
        ),
        "next_phase": (
            "Phase 27.60 — broader natural-dialogue canary using tokenizer v7 + Phase 27.59 repair"
            if passed
            else "Phase 27.60 — inspect Phase 27.59 failures and repair family conditioning"
        ),
        "torch_version": torch.__version__,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)
    _write_doc(report, args.doc)

    print("SF.AI — Phase 27.59 bounded alignment repair")
    print(f"  status      : {status}")
    print(f"  tokenizer   : {_rel(args.tokenizer)}")
    print(f"  checkpoint  : {checkpoint_name}")
    print(f"  probe       : {summary['passed']}/{summary['total']}")
    print(f"  reasons     : {summary['reason_counts']}")
    print("  runtime     : blocked")
    print(f"  report      : {args.report}")
    print(f"  samples     : {args.samples}")
    print(f"  doc         : {args.doc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
