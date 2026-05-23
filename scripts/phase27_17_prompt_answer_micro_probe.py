#!/usr/bin/env python3
"""Phase 27.17 prompt-to-answer micro-probe.

This diagnostic trains SF-10M on a tiny, owner-delegated, sovereign set of
MSA/Saudi prompt-answer pairs. It stays under artifacts/eval and must not be
treated as public corpus expansion.

Goal: prove the stack can learn "this user prompt -> this assistant answer"
before any wider training or SF-50M scaling.
"""

from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

from sf_ai.modules.chat.generation_guard import GenerationGuard
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_17_prompt_answer_micro_probe"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_17_prompt_answer_micro_probe_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_17_prompt_answer_micro_probe_generations.md"


MSA_PAIRS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("السلام عليكم", "وعليكم السلام، أهلًا بك.", ("وعليكم", "أهلًا")),
    ("كيف حالك اليوم", "بخير، شكرًا لسؤالك.", ("بخير", "شكرًا")),
    ("أريد نصيحة قصيرة", "ابدأ بخطوة صغيرة وواضحة.", ("خطوة", "واضحة")),
    ("ما معنى الصبر", "الصبر هو الثبات عند الصعوبة.", ("الثبات", "الصعوبة")),
    ("أشعر بتوتر بسيط", "خذ نفسًا هادئًا وابدأ بالأهم.", ("نفسًا", "الأهم")),
    ("أريد ترتيب يومي", "اكتب ثلاث مهام وابدأ بالأقرب.", ("ثلاث", "الأقرب")),
    ("هل تفهم كلامي", "نعم، أفهم كلامك وأرد بوضوح.", ("أفهم", "بوضوح")),
    ("اشرح لي التعاون", "التعاون يعني أن ننجز معًا بدل الانفراد.", ("التعاون", "معًا")),
    ("ماذا أفعل عند الزحمة", "اخرج مبكرًا واترك وقتًا إضافيًا.", ("مبكرًا", "إضافيًا")),
    ("كيف أتعلم عادة جديدة", "كررها يوميًا ولو لمدة قصيرة.", ("يوميًا", "قصيرة")),
    ("ما فائدة القراءة", "القراءة توسع الفهم وتزيد المفردات.", ("الفهم", "المفردات")),
    ("أريد جوابا مختصرا", "نعم، سأجيبك باختصار.", ("نعم", "باختصار")),
    ("كيف أهدأ قبل النوم", "خفف الإضاءة واترك الهاتف قليلًا.", ("الإضاءة", "الهاتف")),
    ("ما معنى الاحترام", "الاحترام تقدير الناس بالكلام والفعل.", ("تقدير", "الفعل")),
    ("أريد تشجيعا بسيطا", "أنت قادر، ابدأ ولا تنتظر الكمال.", ("قادر", "الكمال")),
    ("شكرا لك", "العفو، يسعدني أن أساعدك.", ("العفو", "أساعدك")),
)


SAUDI_PAIRS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("هلا والله", "هلا بك، تفضل وش تحتاج؟", ("هلا", "تحتاج")),
    ("كيفك", "بخير ولله الحمد، أنت كيفك؟", ("بخير", "كيفك")),
    ("وش تنصحني اليوم", "ابدأ بشي واحد بسيط ولا تكثرها.", ("ابدأ", "بسيط")),
    ("وش معنى الصبر", "الصبر إنك تثبت وقت الصعوبة.", ("تثبت", "الصعوبة")),
    ("متضايق شوي", "الله يهونها، خذ نفس واهدأ شوي.", ("يهونها", "اهدأ")),
    ("ابي ارتب يومي", "اكتب أهم ثلاث أشياء وابدأ بالأول.", ("ثلاث", "الأول")),
    ("تفهم كلامي", "إيه أفهمك، وبرد عليك بوضوح.", ("أفهمك", "بوضوح")),
    ("وش يعني تعاون", "يعني نشتغل سوا ونخفف الحمل.", ("سوا", "الحمل")),
    ("الزحمة تعبتني", "اطلع بدري وخل عندك وقت زيادة.", ("بدري", "زيادة")),
    ("ابي اتعلم عادة", "كررها كل يوم حتى لو شوي.", ("كررها", "شوي")),
    ("القراءة وش تفيد", "توسع فهمك وتزيد كلماتك.", ("فهمك", "كلماتك")),
    ("ابي جواب قصير", "تم، بعطيك جواب مختصر.", ("تم", "مختصر")),
    ("ما انام بسرعة", "خفف الجوال وخلي الجو أهدأ.", ("الجوال", "أهدأ")),
    ("وش معنى الاحترام", "يعني تقدّر الناس بكلامك وتصرفك.", ("تقدّر", "تصرفك")),
    ("حمسني بكلمة", "تقدر، ابدأ بخطوة ولا توقف.", ("تقدر", "خطوة")),
    ("مشكور", "العفو، حاضر بأي وقت.", ("العفو", "حاضر")),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.17 prompt-answer micro-probe")
    p.add_argument("--steps", type=int, default=2400)
    p.add_argument("--epochs", type=int, default=300)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--lr", type=float, default=8e-4)
    p.add_argument("--warmup", type=int, default=80)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--keep-work", action="store_true")
    return p.parse_args()


def _record(dialect: str, idx: int, prompt: str, answer: str, terms: tuple[str, ...]) -> dict[str, Any]:
    return {
        "id": f"phase27_17_{dialect}_{idx:03d}",
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": answer},
        ],
        "expected_terms": list(terms),
        "provenance": {
            "source": f"sf-ai-phase27-17-micro-probe-{dialect}",
            "license": "owner-delegated-internal-sf-ai",
            "training_allowed": True,
            "quality": "gold",
            "dialect": dialect,
            "owner_user_id": "sami-local",
            "created_by_user_id": "sf-ai-agent",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
            "synthetic_llm_data": False,
            "notes": "internal diagnostic prompt-to-answer micro-probe; not public corpus expansion",
        },
    }


def _records() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for idx, (prompt, answer, terms) in enumerate(MSA_PAIRS, start=1):
        out.append(_record("msa", idx, prompt, answer, terms))
    for idx, (prompt, answer, terms) in enumerate(SAUDI_PAIRS, start=1):
        out.append(_record("saudi", idx, prompt, answer, terms))
    return out


def _write_probe_corpus(corpus_dir: Path, records: list[dict[str, Any]]) -> Path:
    corpus_dir.mkdir(parents=True, exist_ok=True)
    out = corpus_dir / "phase27_17_prompt_answer_micro_probe.jsonl"
    out.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )
    return out


def _latest_checkpoint_name(checkpoints_root: Path) -> str:
    steps: list[tuple[int, str]] = []
    for path in checkpoints_root.glob("sf-10m-step*"):
        try:
            step = int(path.name.rsplit("step", 1)[1])
        except (IndexError, ValueError):
            continue
        if (path / "meta.json").exists() and (path / "state.pt").exists():
            steps.append((step, path.name))
    if not steps:
        raise RuntimeError(f"no saved probe checkpoints under {checkpoints_root}")
    return sorted(steps)[-1][1]


def _messages(record: dict[str, Any]) -> tuple[str, str]:
    user = ""
    assistant = ""
    for msg in record.get("messages", ()):
        if msg.get("role") == "user" and not user:
            user = str(msg.get("content", "")).strip()
        if msg.get("role") == "assistant" and not assistant:
            assistant = str(msg.get("content", "")).strip()
    return user, assistant


def _surface(text: str) -> str:
    table = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ة": "ه"})
    clean = (text or "").replace("ـ", "").translate(table)
    return " ".join(clean.split()).strip(" .،؟!؛:")


def _exact_clean(generated: str, expected: str) -> bool:
    g = _surface(generated)
    e = _surface(expected)
    if not g or not e:
        return False
    if g == e:
        return True
    if g.startswith(e):
        extra = g[len(e):].strip(" .،؟!؛:")
        return len(extra) <= 4
    return False


def _semantic_match(generated: str, terms: tuple[str, ...]) -> bool:
    g = _surface(generated)
    normalized_terms = [_surface(term) for term in terms if term.strip()]
    if not normalized_terms:
        return False
    hits = sum(1 for term in normalized_terms if term in g)
    return hits == len(normalized_terms)


def _evaluate(
    *,
    records: list[dict[str, Any]],
    checkpoints_root: Path,
    checkpoint_name: str,
    device: str,
) -> tuple[list[dict[str, Any]], Counter[str]]:
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=ROOT / "artifacts/tokenizers/sf_bpe/v2",
            checkpoints_root=checkpoints_root,
            checkpoint_name=checkpoint_name,
            generator_name="sf_10m_phase27_17_micro_probe",
            model_size="sf-10m",
            seq_len=64,
            max_new_tokens=24,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.08,
            device=device,
            dialogue_prompt=True,
        )
    )
    guard = GenerationGuard(min_chars=4)
    results: list[dict[str, Any]] = []
    reasons: Counter[str] = Counter()
    for record in records:
        prompt, expected = _messages(record)
        dialect = str(record.get("provenance", {}).get("dialect", ""))
        expected_terms = tuple(str(term) for term in record.get("expected_terms", ()))
        out = generator.generate(
            prompt,
            dialect=dialect,
            max_new_tokens=24,
            temperature=1.0,
            top_k=0,
        )
        verdict = guard.inspect_for_prompt(prompt, out.text)
        exact = _exact_clean(out.text, expected)
        semantic = _semantic_match(out.text, expected_terms)
        passed = bool(out.used and verdict.allowed and exact and semantic)
        if passed:
            reason = "passed"
        elif not out.used:
            reason = f"generator:{out.reason}"
        elif not verdict.allowed:
            reason = f"guard:{verdict.reason}"
        elif not semantic:
            reason = "missing_semantic_terms"
        else:
            reason = "not_exact_clean"
        reasons[reason] += 1
        results.append(
            {
                "id": record["id"],
                "dialect": dialect,
                "prompt": prompt,
                "expected": expected,
                "expected_terms": list(expected_terms),
                "generated": out.text,
                "used": out.used,
                "generator_reason": out.reason,
                "guard_reason": verdict.reason,
                "exact_clean": exact,
                "semantic_match": semantic,
                "passed": passed,
                "reason": reason,
            }
        )
    return results, reasons


def _write_samples(path: Path, results: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.17 Prompt-to-Answer Micro-Probe Generations", ""]
    for item in results:
        lines.extend(
            [
                f"## {item['id']} — {item['dialect']} — {'PASS' if item['passed'] else 'FAIL'}",
                "",
                f"- prompt: {item['prompt']}",
                f"- expected: {item['expected']}",
                f"- generated: {item['generated']}",
                f"- exact_clean: {item['exact_clean']}",
                f"- semantic_match: {item['semantic_match']}",
                f"- reason: {item['reason']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    records = _records()
    if args.work_dir.exists() and not args.keep_work:
        shutil.rmtree(args.work_dir)
    corpus_dir = args.work_dir / "corpus"
    checkpoints = args.work_dir / "checkpoints"
    _write_probe_corpus(corpus_dir, records)

    train_args = [
        "--tokenizer", str(ROOT / "artifacts/tokenizers/sf_bpe/v2"),
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
        "--seed", "20260525",
        "--checkpoints", str(checkpoints),
        "--device", args.device,
    ]
    train_code = train_tiny_lm_run(train_args)
    if train_code != 0:
        return train_code

    checkpoint_name = _latest_checkpoint_name(checkpoints)
    results, reasons = _evaluate(
        records=records,
        checkpoints_root=checkpoints,
        checkpoint_name=checkpoint_name,
        device=args.device,
    )
    total = len(results)
    passed = sum(1 for item in results if item["passed"])
    exact = sum(1 for item in results if item["exact_clean"])
    semantic = sum(1 for item in results if item["semantic_match"])
    guard = sum(1 for item in results if item["guard_reason"] == "passed")
    status = (
        "PASSED_PROMPT_ANSWER_MICRO_PROBE"
        if passed == total
        else "FAILED_PROMPT_ANSWER_MICRO_PROBE_BLOCK_RUNTIME"
    )
    report = {
        "phase": "Phase 27.17",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "records": total,
        "records_by_dialect": {"msa": len(MSA_PAIRS), "saudi": len(SAUDI_PAIRS)},
        "training": {
            "steps": args.steps,
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "seq_len": args.seq_len,
            "lr": args.lr,
            "packing_mode": "sample_isolated",
            "checkpoint_name": checkpoint_name,
        },
        "passed": passed,
        "failed": total - passed,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "exact_clean": exact,
        "semantic_match": semantic,
        "guard_passed": guard,
        "reason_counts": dict(reasons),
        "runtime_allowed": False,
        "sf50m_allowed": False,
        "decision": (
            "Do not enable runtime or SF-50M until prompt-to-answer exact and semantic gates pass."
            if passed != total
            else "Micro-probe passed; next compare against held-out prompt-answer probes before wider training."
        ),
        "results": results,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, results)

    print("SF.AI — Phase 27.17 prompt-answer micro-probe")
    print(f"  status       : {status}")
    print(f"  checkpoint   : {checkpoint_name}")
    print(f"  records      : {total}")
    print(f"  passed       : {passed}/{total}")
    print(f"  exact_clean  : {exact}/{total}")
    print(f"  semantic     : {semantic}/{total}")
    print(f"  guard_passed : {guard}/{total}")
    print(f"  reasons      : {dict(reasons)}")
    print(f"  report       : {args.report}")
    print(f"  samples      : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
