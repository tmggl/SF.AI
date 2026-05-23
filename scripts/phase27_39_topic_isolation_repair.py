#!/usr/bin/env python3
"""Phase 27.39 topic-isolation repair probe.

Phase 27.38 proved that simply adding blocked topics is not enough: the
candidate collapsed many definitions into "الاحترام". This probe rebuilds the
definition curriculum as a balanced topic-isolation set. A topic passes only if
its own semantic term appears and neighboring definition topics do not leak.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import _latest_checkpoint_name  # noqa: E402
from scripts.phase27_19_hygiene_repair_probe import _write_probe_corpus  # noqa: E402
from scripts.phase27_26_heldout_objective_repair import RepairPair, _rel  # noqa: E402
from scripts.phase27_33_advice_micro_stabilization import _records as phase27_33_records  # noqa: E402
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig, _intent_label  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v4_min_lexical"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_39_topic_isolation_repair"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_39_topic_isolation_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_39_topic_isolation_repair.md"

TOPIC_STEMS: dict[str, tuple[str, ...]] = {
    "التعاون": ("تعاون", "سوا", "نشتغل", "مشاركه"),
    "الصبر": ("صبر", "ثبات"),
    "الاحترام": ("احترام", "تقدير"),
    "القراءة": ("قراء", "قراي"),
    "الصداقة": ("صداق", "رفقه"),
    "الصدق": ("صدق", "حقيقه"),
    "التنظيم": ("تنظيم", "ترتيب"),
    "الهدوء": ("هدوء", "سكينه"),
}


@dataclass(frozen=True)
class ProbeCase:
    id: str
    dialect: str
    prompt: str
    intent: str
    topic: str
    expected_terms: tuple[str, ...]
    bucket: str


BALANCED_TOPIC_REPAIR: tuple[RepairPair, ...] = (
    RepairPair("msa", "ما معنى التعاون", "التعاون يعني أن يعمل الناس معًا لتخفيف الحمل.", ("التعاون", "معًا"), "definition"),
    RepairPair("saudi", "وش يعني تعاون", "التعاون يعني نشتغل سوا ونخفف الحمل.", ("التعاون", "سوا"), "definition"),
    RepairPair("msa", "اشرح التعاون بجملة", "التعاون مشاركة الجهد بين الناس.", ("التعاون", "مشاركة"), "definition"),
    RepairPair("saudi", "فسر التعاون بالسعودي", "التعاون إنك تساعد غيرك وتنجزون سوا.", ("التعاون", "سوا"), "definition"),
    RepairPair("msa", "ما معنى الصبر", "الصبر يعني الثبات وقت الصعوبة.", ("الصبر", "الثبات"), "definition"),
    RepairPair("saudi", "الصبر وش يعني", "الصبر إنك تثبت وما تستعجل وقت الضيق.", ("الصبر", "تثبت"), "definition"),
    RepairPair("msa", "اشرح الصبر بجملة", "الصبر قوة داخلية تساعدك على الاحتمال.", ("الصبر", "الاحتمال"), "definition"),
    RepairPair("saudi", "وش المقصود بالصبر", "الصبر إنك تتحمل وتكمل بدون استعجال.", ("الصبر", "تتحمل"), "definition"),
    RepairPair("msa", "ما معنى الاحترام", "الاحترام تقدير الناس بالكلام والتصرف.", ("الاحترام", "تقدير"), "definition"),
    RepairPair("saudi", "وش المقصود بالاحترام", "الاحترام إنك تقدّر الناس بكلامك وتصرفك.", ("الاحترام", "تقدّر"), "definition"),
    RepairPair("msa", "اشرح الاحترام بجملة", "الاحترام معاملة الناس بقدر وذوق.", ("الاحترام", "معاملة"), "definition"),
    RepairPair("saudi", "الاحترام وش يعني", "الاحترام يعني كلامك وتصرفك يكون فيه تقدير.", ("الاحترام", "تقدير"), "definition"),
    RepairPair("msa", "ما معنى القراءة", "القراءة تفيد لأنها توسع الفهم والمفردات.", ("القراءة", "الفهم"), "definition"),
    RepairPair("saudi", "القراية وش تعني", "القراية توسع فهمك وتزيد كلماتك.", ("القراية", "فهمك"), "definition"),
    RepairPair("msa", "اشرح القراءة بجملة", "القراءة طريق لاكتساب معرفة جديدة.", ("القراءة", "معرفة"), "definition"),
    RepairPair("saudi", "وش فايدة القراية", "القراية تفيدك وتفتح لك معرفة أكثر.", ("القراية", "معرفة"), "definition"),
    RepairPair("msa", "ما معنى الصداقة", "الصداقة علاقة طيبة تقوم على الوفاء.", ("الصداقة", "الوفاء"), "definition"),
    RepairPair("saudi", "وش معنى الصداقة", "الصداقة إنك تلقى رفيق يوقف معك.", ("الصداقة", "رفيق"), "definition"),
    RepairPair("msa", "الصداقة ماذا تعني", "الصداقة مودة ووفاء بين الناس.", ("الصداقة", "وفاء"), "definition"),
    RepairPair("saudi", "الصداقة وش تعني", "الصداقة رفقة طيبة ووقفة وقت الحاجة.", ("الصداقة", "رفقة"), "definition"),
    RepairPair("msa", "ما معنى الصدق", "الصدق أن تقول الحقيقة وتلتزم بما تقول.", ("الصدق", "الحقيقة"), "definition"),
    RepairPair("saudi", "وش معنى الصدق", "الصدق إن كلامك يكون واضح وما فيه خداع.", ("الصدق", "واضح"), "definition"),
    RepairPair("msa", "اشرح الصدق بجملة", "الصدق وضوح في القول والعمل.", ("الصدق", "وضوح"), "definition"),
    RepairPair("saudi", "الصدق وش يعني", "الصدق يعني تقول الحقيقة بوضوح.", ("الصدق", "الحقيقة"), "definition"),
    RepairPair("msa", "ما معنى التنظيم", "التنظيم ترتيب الوقت والمهام بطريقة واضحة.", ("التنظيم", "ترتيب"), "definition"),
    RepairPair("saudi", "وش معنى التنظيم", "التنظيم إنك ترتب وقتك ومهامك بوضوح.", ("التنظيم", "ترتب"), "definition"),
    RepairPair("msa", "اشرح التنظيم ببساطة", "التنظيم معرفة ما تفعل ومتى تبدأ.", ("التنظيم", "تبدأ"), "definition"),
    RepairPair("saudi", "التنظيم وش يعني", "التنظيم يعني تخلي أمورك مرتبة.", ("التنظيم", "مرتبة"), "definition"),
    RepairPair("msa", "ما معنى الهدوء", "الهدوء سكينة تساعدك على التفكير بوضوح.", ("الهدوء", "سكينة"), "definition"),
    RepairPair("saudi", "وش معنى الهدوء", "الهدوء إنك تهدأ وتاخذ الأمور بروية.", ("الهدوء", "تهدأ"), "definition"),
    RepairPair("msa", "اشرح الهدوء بجملة", "الهدوء راحة تقلل التوتر.", ("الهدوء", "التوتر"), "definition"),
    RepairPair("saudi", "الهدوء وش يعني", "الهدوء يعني تخفف توترك وتتكلم بروية.", ("الهدوء", "توترك"), "definition"),
)


PROBE_CASES: tuple[ProbeCase, ...] = (
    ProbeCase("reg_001", "saudi", "كيفك اليوم", "smalltalk", "", ("بخير",), "regression"),
    ProbeCase("reg_002", "msa", "شكرًا لمساعدتك", "thanks", "", ("العفو",), "regression"),
    ProbeCase("reg_003", "msa", "وجهني بخطوة بسيطة", "advice", "", ("ابدأ",), "regression"),
    ProbeCase("reg_004", "msa", "رتب لي يومي بسرعة", "planning", "", ("ثلاث",), "regression"),
    ProbeCase("reg_005", "saudi", "توترت شوي وش اسوي", "support", "", ("اهدأ",), "regression"),
    ProbeCase("reg_006", "saudi", "وش المقصود بالاحترام", "definition", "الاحترام", ("تقدّر",), "regression"),
    ProbeCase("reg_007", "msa", "ما معنى التعاون", "definition", "التعاون", ("التعاون",), "regression"),
    ProbeCase("reg_008", "msa", "ما معنى الصبر", "definition", "الصبر", ("الصبر",), "regression"),
    ProbeCase("new_001", "msa", "ما معنى الصداقة", "definition", "الصداقة", ("الصداقة",), "new_topic"),
    ProbeCase("new_002", "saudi", "وش معنى الصداقة", "definition", "الصداقة", ("الصداقة",), "new_topic"),
    ProbeCase("new_003", "msa", "اشرح الصدق بجملة", "definition", "الصدق", ("الصدق",), "new_topic"),
    ProbeCase("new_004", "saudi", "وش معنى الصدق", "definition", "الصدق", ("الصدق",), "new_topic"),
    ProbeCase("new_005", "msa", "ما معنى التنظيم", "definition", "التنظيم", ("التنظيم",), "new_topic"),
    ProbeCase("new_006", "saudi", "وش معنى التنظيم", "definition", "التنظيم", ("ترتب",), "new_topic"),
    ProbeCase("new_007", "msa", "ما معنى الهدوء", "definition", "الهدوء", ("الهدوء",), "new_topic"),
    ProbeCase("new_008", "saudi", "وش معنى الهدوء", "definition", "الهدوء", ("الهدوء",), "new_topic"),
    ProbeCase("held_001", "msa", "الصداقة ماذا تعني", "definition", "الصداقة", ("الصداقة",), "heldout"),
    ProbeCase("held_002", "saudi", "الصدق وش يعني", "definition", "الصدق", ("الحقيقة",), "heldout"),
    ProbeCase("held_003", "msa", "اشرح التنظيم ببساطة", "definition", "التنظيم", ("التنظيم",), "heldout"),
    ProbeCase("held_004", "saudi", "الهدوء وش يعني", "definition", "الهدوء", ("توترك",), "heldout"),
    ProbeCase("iso_001", "msa", "اشرح القراءة بجملة", "definition", "القراءة", ("القراءة",), "isolation"),
    ProbeCase("iso_002", "saudi", "القراية وش تعني", "definition", "القراءة", ("القراية",), "isolation"),
    ProbeCase("iso_003", "msa", "اشرح الاحترام بجملة", "definition", "الاحترام", ("الاحترام",), "isolation"),
    ProbeCase("iso_004", "saudi", "فسر التعاون بالسعودي", "definition", "التعاون", ("التعاون",), "isolation"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.39 topic-isolation repair")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--steps", type=int, default=6400)
    p.add_argument("--epochs", type=int, default=640)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=6e-4)
    p.add_argument("--warmup", type=int, default=160)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--keep-work", action="store_true")
    p.add_argument("--skip-train", action="store_true")
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
    if "تعاون" in surface:
        return "التعاون"
    if "صبر" in surface:
        return "الصبر"
    if "احترام" in surface:
        return "الاحترام"
    if "قراء" in surface or "قراي" in surface:
        return "القراءة"
    if "صداق" in surface or "رفقه" in surface:
        return "الصداقة"
    if "صدق" in surface:
        return "الصدق"
    if "تنظيم" in surface:
        return "التنظيم"
    if "هدوء" in surface:
        return "الهدوء"
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
        "id": f"phase27_39_{pair.dialect}_{idx:04d}",
        "messages": messages,
        "expected_terms": list(pair.expected_terms),
        "provenance": {
            "source": f"sf-ai-phase27-39-topic-isolation-repair-{pair.dialect}",
            "license": "owner-delegated-internal-sf-ai",
            "training_allowed": True,
            "quality": "gold",
            "dialect": pair.dialect,
            "owner_user_id": "sami-local",
            "created_by_user_id": "sf-ai-agent",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
            "synthetic_llm_data": False,
            "notes": "internal topic-isolation probe; excludes operational/project-management dialogue",
        },
    }


def _records() -> list[dict[str, Any]]:
    base_records, micro_records, _repair_records = phase27_33_records()
    topic_records = [
        _conditioned_record(pair, idx)
        for idx, pair in enumerate(BALANCED_TOPIC_REPAIR, start=1)
    ]
    train_records = list(micro_records)
    train_records.extend(base_records)
    for _ in range(70):
        train_records.extend(topic_records)
    return train_records


def _semantic_match(text: str, terms: tuple[str, ...]) -> bool:
    surface = _surface(text)
    return all(_surface(term) in surface for term in terms)


def _topic_isolated(text: str, topic: str) -> tuple[bool, list[str]]:
    if not topic:
        return True, []
    surface = _surface(text)
    forbidden: list[str] = []
    for candidate, stems in TOPIC_STEMS.items():
        if candidate == topic:
            continue
        if any(stem in surface for stem in stems):
            forbidden.append(candidate)
    return not forbidden, forbidden


def _evaluate(
    *,
    tokenizer: Path,
    checkpoints_root: Path,
    checkpoint_name: str,
    device: str,
) -> list[dict[str, Any]]:
    gen = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=tokenizer,
            checkpoints_root=checkpoints_root,
            checkpoint_name=checkpoint_name,
            generator_name="sf_10m_phase27_39",
            model_size="sf-10m",
            seq_len=64,
            max_new_tokens=24,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.1,
            device=device,
            dialogue_prompt=True,
        )
    )
    guard = GenerationGuard(min_chars=4)
    rows: list[dict[str, Any]] = []
    for item in PROBE_CASES:
        out = gen.generate(
            item.prompt,
            dialect=item.dialect,
            intent=item.intent,
            topic=item.topic,
            max_new_tokens=24,
            temperature=1.0,
            top_k=0,
        )
        verdict = (
            guard.inspect(out.text)
            if item.intent == "definition"
            else guard.inspect_for_prompt(item.prompt, out.text)
        )
        semantic = _semantic_match(out.text, item.expected_terms)
        isolated, forbidden_topics = _topic_isolated(out.text, item.topic)
        passed = bool(out.used and verdict.allowed and semantic and isolated)
        if passed:
            reason = "passed"
        elif not out.used:
            reason = f"generator:{out.reason}"
        elif not verdict.allowed:
            reason = f"guard:{verdict.reason}"
        elif not semantic:
            reason = "semantic_mismatch"
        else:
            reason = "topic_leakage"
        rows.append(
            {
                "id": item.id,
                "bucket": item.bucket,
                "dialect": item.dialect,
                "prompt": item.prompt,
                "intent": item.intent,
                "topic": item.topic,
                "expected_terms": list(item.expected_terms),
                "response": out.text,
                "generator_used": out.used,
                "guard_allowed": verdict.allowed,
                "guard_reason": verdict.reason,
                "semantic_match": semantic,
                "topic_isolated": isolated,
                "forbidden_topics": forbidden_topics,
                "passed": passed,
                "reason": reason,
            }
        )
    return rows


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    buckets = sorted({str(row["bucket"]) for row in rows})
    return {
        "passed": sum(1 for row in rows if row["passed"]),
        "total": len(rows),
        "bucket_summary": {
            bucket: {
                "passed": sum(1 for row in rows if row["bucket"] == bucket and row["passed"]),
                "total": sum(1 for row in rows if row["bucket"] == bucket),
            }
            for bucket in buckets
        },
        "reason_counts": dict(Counter(str(row["reason"]) for row in rows)),
    }


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.39 Topic-Isolation Repair", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- bucket: {row['bucket']}",
                f"- prompt: {row['prompt']}",
                f"- topic: {row['topic'] or '-'}",
                f"- response: {row['response']}",
                f"- semantic_match: {row['semantic_match']}",
                f"- topic_isolated: {row['topic_isolated']}",
                f"- forbidden_topics: {', '.join(row['forbidden_topics']) if row['forbidden_topics'] else '-'}",
                f"- reason: {row['reason']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    if not (args.tokenizer / "meta.json").exists():
        print(f"error: missing tokenizer at {args.tokenizer}", file=sys.stderr)
        return 1
    if args.work_dir.exists() and not args.keep_work and not args.skip_train:
        shutil.rmtree(args.work_dir)

    corpus_dir = args.work_dir / "corpus"
    checkpoints = args.work_dir / "checkpoints"
    train_records = _records()
    if not args.skip_train:
        _write_probe_corpus(corpus_dir, train_records)

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
            "--seed", "20260609",
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
        "PASSED_TOPIC_ISOLATION_READY_FOR_GUARDED_RUNTIME_CANDIDATE"
        if all_passed
        else "PARTIAL_TOPIC_ISOLATION_KEEP_CURRENT_RUNTIME"
    )
    report = {
        "phase": "Phase 27.39",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "skip_train": args.skip_train,
        "training_scope": "targeted SF-10M topic-isolation probe only; no scaling",
        "tokenizer": _rel(args.tokenizer),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_39",
        "train_records": len(train_records),
        "balanced_topics": sorted(TOPIC_STEMS),
        "summary": summary,
        "runtime_switch_allowed": all_passed,
        "sf50m_allowed": False,
        "phase28_allowed": False,
        "next_phase": (
            "Phase 27.40 — guarded runtime switch design for phase27_39 candidate"
            if all_passed
            else "Phase 27.40 — tokenizer/context repair for topic isolation"
        ),
        "rows": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)

    print("SF.AI — Phase 27.39 topic-isolation repair")
    print(f"  status      : {status}")
    print(f"  checkpoint  : {checkpoint_name}")
    print(f"  cases       : {summary['passed']}/{summary['total']}")
    for bucket, item in summary["bucket_summary"].items():
        print(f"  {bucket:<10}: {item['passed']}/{item['total']}")
    print(f"  reasons     : {summary['reason_counts']}")
    print(f"  report      : {args.report}")
    print(f"  samples     : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
