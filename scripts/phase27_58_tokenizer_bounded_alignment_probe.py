#!/usr/bin/env python3
"""Phase 27.58 tokenizer v7 + bounded format/alignment probe.

This is a deliberately bounded training phase:
- train a fresh sovereign tokenizer with Phase 27.57 protected phrases;
- train a small SF-10M probe on curated msa/saudi dialogue families;
- evaluate by response family alignment, not prompt-overlap matching;
- keep runtime/UI blocked regardless of pass/fail.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any

import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import _latest_checkpoint_name  # noqa: E402
from scripts.phase27_19_hygiene_repair_probe import _write_probe_corpus  # noqa: E402
from scripts.phase27_26_heldout_objective_repair import RepairPair, _rel  # noqa: E402
from scripts.phase27_39_topic_isolation_repair import _conditioned_record  # noqa: E402
from scripts.phase27_44_tokenizer_curriculum_repair import _records as phase27_44_records  # noqa: E402
from sf_ai.models.tokenizer import BPETokenizer, TokenizerConfig, train_bpe_from_corpus  # noqa: E402
from sf_ai.models.tokenizer.policy_audit import load_plain_terms, load_tokenization_rules  # noqa: E402
from sf_ai.modules.chat.generation_guard import GenerationGuard  # noqa: E402
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig  # noqa: E402
from sf_ai.training.train_tiny_lm import run as train_tiny_lm_run  # noqa: E402


DEFAULT_TOKENIZER_OUT = ROOT / "artifacts/tokenizers/sf_bpe/v7_phase27_58"
DEFAULT_WORK = ROOT / "artifacts/eval/phase27_58_tokenizer_bounded_alignment_probe"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_58_tokenizer_bounded_alignment_probe_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_58_tokenizer_bounded_alignment_probe.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_58_TOKENIZER_BOUNDED_ALIGNMENT_PROBE_REPORT.md"
TOKENIZATION_RULES = ROOT / "resources/tokenization/tokenization_rules.yaml"
SEMANTIC_RULES = ROOT / "resources/evaluation/semantic_alignment_phase27_57.json"
RESPONSE_FAMILIES = ROOT / "resources/dialogue_format/response_families_phase27_57.json"
_DIACRITICS_RE = re.compile(r"[\u064b-\u065f\u0670]")
_PUNCT_RE = re.compile(r"[^\w\s\u0600-\u06ff]")


@dataclass(frozen=True)
class AlignmentCase:
    id: str
    dialect: str
    prompt: str
    intent: str
    topic: str
    family: str
    expected_terms: tuple[str, ...]


REPAIR_PAIRS: tuple[RepairPair, ...] = (
    RepairPair("saudi", "سولف معي شوي", "أكيد، ودك نسولف عن يومك أو عن موضوع خفيف؟", ("نسولف", "موضوع"), "open_social"),
    RepairPair("saudi", "هات موضوع خفيف", "خلنا نبدأ بسؤال بسيط: وش الشيء اللي حسّن يومك اليوم؟", ("نبدأ", "يومك"), "open_social"),
    RepairPair("msa", "أريد حديثًا خفيفًا", "تفضل، نستطيع أن نبدأ بموضوع بسيط عن يومك.", ("نبدأ", "يومك"), "open_social"),
    RepairPair("saudi", "الي تحب", "خلنا نختار موضوع خفيف ونسولف عنه بهدوء.", ("موضوع", "نسولف"), "open_social"),
    RepairPair("saudi", "يعني كيف أبدأ", "ابدأ بخطوة صغيرة وواضحة، ثم كمل بعدها بهدوء.", ("ابدأ", "خطوة"), "followup"),
    RepairPair("msa", "وضح لي أكثر", "أقصد أن تبدأ بالأسهل ثم تنتقل للخطوة التالية.", ("أقصد", "خطوة"), "followup"),
    RepairPair("saudi", "طيب ليه", "لأن البداية الصغيرة تخفف الضغط وتوضح لك الطريق.", ("البداية", "توضح"), "followup"),
    RepairPair("saudi", "كمل كلامك", "نكمل: اختر خطوة واحدة، نفذها، ثم قيّم النتيجة.", ("نكمل", "خطوة"), "followup"),
    RepairPair("msa", "ساعدني أرتب يومي", "اكتب ثلاث مهام، ثم ابدأ بالأهم واترك الباقي لوقته.", ("مهام", "الأهم"), "planning"),
    RepairPair("saudi", "ابي بداية بسيطة لليوم", "اكتب أهم شي عندك وابدأ فيه عشر دقائق.", ("ابدأ", "دقائق"), "planning"),
    RepairPair("msa", "كيف أبدأ بدون تعقيد", "اختر مهمة واحدة صغيرة وابدأ بها الآن.", ("مهمة", "ابدأ"), "planning"),
    RepairPair("saudi", "رتب لي بداية بسيطة", "ابدأ بشي واحد واضح، وبعده قرر الخطوة التالية.", ("ابدأ", "خطوة"), "planning"),
    RepairPair("saudi", "توترت وش أسوي", "خذ نفسًا هادئًا، وخل تركيزك على خطوة واحدة الآن.", ("نفس", "خطوة"), "support"),
    RepairPair("msa", "أنا متوتر قليلًا", "تنفس بهدوء، واكتب ما يقلقك في سطر واحد.", ("تنفس", "يقلقك"), "support"),
    RepairPair("saudi", "طمني شوي", "أنت تقدر تهدأ خطوة خطوة، لا تستعجل الحكم على نفسك.", ("تهدأ", "خطوة"), "support"),
    RepairPair("saudi", "حاس بضغط", "خففها عليك: خذ نفس وابدأ بالأقرب والأسهل.", ("نفس", "ابدأ"), "support"),
    RepairPair("msa", "اشرح الصداقة ببساطة", "الصداقة رفقة طيبة تقوم على الوفاء والاهتمام.", ("الصداقة", "رفقة"), "topic"),
    RepairPair("saudi", "الشجاعة وش معناها", "الشجاعة إنك تسوي الصح حتى لو كنت خايف.", ("الشجاعة", "الصح"), "topic"),
    RepairPair("msa", "ما معنى الصدق", "الصدق أن تقول الحقيقة بوضوح وتلتزم بها.", ("الصدق", "الحقيقة"), "topic"),
    RepairPair("saudi", "الهدوء وش يعني", "الهدوء إنك تخفف التوتر وتفكر بروية.", ("الهدوء", "التوتر"), "topic"),
)


PROBE_CASES: tuple[AlignmentCase, ...] = (
    AlignmentCase("open_social_01", "saudi", "وش ودك نسولف عنه", "open_social", "", "open_social", ("نسولف", "موضوع")),
    AlignmentCase("open_social_02", "saudi", "هات سالفة خفيفة", "open_social", "", "open_social", ("موضوع", "يومك")),
    AlignmentCase("open_social_03", "msa", "أريد كلامًا خفيفًا", "open_social", "", "open_social", ("نبدأ", "موضوع")),
    AlignmentCase("followup_01", "saudi", "يعني كيف", "followup", "", "followup", ("ابدأ", "خطوة")),
    AlignmentCase("followup_02", "msa", "اشرحها أكثر", "followup", "", "followup", ("أقصد", "خطوة")),
    AlignmentCase("followup_03", "saudi", "طيب بعدين", "followup", "", "followup", ("بعدها", "خطوة")),
    AlignmentCase("planning_01", "msa", "كيف أنظم يومي", "planning", "", "planning", ("مهام", "ابدأ")),
    AlignmentCase("planning_02", "saudi", "ابي ارتب يومي", "planning", "", "planning", ("ابدأ", "خطوة")),
    AlignmentCase("planning_03", "msa", "دلني على بداية عملية", "planning", "", "planning", ("مهمة", "ابدأ")),
    AlignmentCase("support_01", "saudi", "توترت شوي", "support", "", "support", ("نفس", "خطوة")),
    AlignmentCase("support_02", "msa", "أحتاج أهدأ", "support", "", "support", ("تنفس", "بهدوء")),
    AlignmentCase("support_03", "saudi", "طمني", "support", "", "support", ("تهدأ", "خطوة")),
    AlignmentCase("topic_01", "msa", "ما معنى الصداقة", "topic", "الصداقة", "topic", ("الصداقة",)),
    AlignmentCase("topic_02", "saudi", "الشجاعة وش تعني", "topic", "الشجاعة", "topic", ("الشجاعة",)),
    AlignmentCase("topic_03", "msa", "اشرح الصدق", "topic", "الصدق", "topic", ("الصدق",)),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.58 tokenizer + bounded alignment probe")
    p.add_argument("--corpus", type=Path, default=ROOT / "data/corpus/chat/jsonl")
    p.add_argument("--tokenizer-out", type=Path, default=DEFAULT_TOKENIZER_OUT)
    p.add_argument("--vocab-size", type=int, default=9000)
    p.add_argument("--min-frequency", type=int, default=2)
    p.add_argument("--steps", type=int, default=7600)
    p.add_argument("--epochs", type=int, default=760)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--seq-len", type=int, default=80)
    p.add_argument("--lr", type=float, default=6.5e-4)
    p.add_argument("--warmup", type=int, default=180)
    p.add_argument("--device", default="auto")
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--keep-work", action="store_true")
    p.add_argument("--reuse-existing", action="store_true")
    return p.parse_args()


def _surface(text: str) -> str:
    normalized = (
        (text or "")
        .replace("أ", "ا")
        .replace("إ", "ا")
        .replace("آ", "ا")
        .replace("ى", "ي")
        .replace("ة", "ه")
    )
    normalized = _DIACRITICS_RE.sub("", normalized)
    normalized = _PUNCT_RE.sub(" ", normalized.lower())
    return " ".join(normalized.split())


def _load_policy_terms() -> list[str]:
    rules = load_tokenization_rules(TOKENIZATION_RULES)
    paths: list[str] = []
    for section in ("protected_terms", "protected_phrases"):
        raw = rules.get(section) or {}
        paths.extend(str(path) for path in raw.get("active_paths", ()))
    terms: list[str] = []
    seen: set[str] = set()
    for raw_path in paths:
        path = ROOT / raw_path
        for term in load_plain_terms(path):
            if term not in seen:
                seen.add(term)
                terms.append(term)
    return terms


def _train_tokenizer(args: argparse.Namespace, terms: list[str]) -> BPETokenizer:
    if args.tokenizer_out.exists():
        shutil.rmtree(args.tokenizer_out)
    repair_texts = [pair.prompt for pair in REPAIR_PAIRS] + [pair.answer for pair in REPAIR_PAIRS]
    cfg = TokenizerConfig(
        vocab_size=args.vocab_size,
        min_frequency=args.min_frequency,
        protected_terms=tuple(terms),
    )
    return train_bpe_from_corpus(
        corpus_root=args.corpus,
        output_dir=args.tokenizer_out,
        config=cfg,
        extra_texts=[*terms, *terms, *repair_texts, *repair_texts],
        name="sf_bpe_v7_phase27_58_protected_alignment",
    )


def _tokenizer_rows(tokenizer: BPETokenizer, terms: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    critical = set(load_plain_terms(ROOT / "resources/tokenization/protected_phrases_phase27_57.txt"))
    for term in terms:
        ids = tokenizer.encode(term)
        decoded = tokenizer.decode(ids)
        rows.append(
            {
                "term": term,
                "piece_count": len(ids),
                "decoded": decoded,
                "roundtrip_ok": decoded == term,
                "phase27_57_critical": term in critical,
            }
        )
    return rows


def _family_terms() -> dict[str, tuple[str, ...]]:
    raw = json.loads(SEMANTIC_RULES.read_text(encoding="utf-8"))
    categories = raw["categories"]
    return {
        str(name): tuple(str(term) for term in spec["required_any"])
        for name, spec in categories.items()
    }


def _forbidden_for_family(family: str, families: dict[str, tuple[str, ...]]) -> tuple[str, ...]:
    raw = json.loads(SEMANTIC_RULES.read_text(encoding="utf-8"))
    spec = raw["categories"].get(family, {})
    forbidden: list[str] = []
    for name in spec.get("forbidden_family", ()):
        forbidden.extend(families.get(str(name), ()))
    return tuple(forbidden)


def _records() -> list[dict[str, Any]]:
    records = list(phase27_44_records())
    repair_records = [
        _conditioned_record(pair, 58000 + idx)
        for idx, pair in enumerate(REPAIR_PAIRS, start=1)
    ]
    for _ in range(48):
        records.extend(repair_records)
    return records


def _expected_ok(text: str, terms: tuple[str, ...]) -> bool:
    surface = _surface(text)
    return any(_surface(term) in surface for term in terms)


def _family_ok(text: str, family: str, families: dict[str, tuple[str, ...]]) -> bool:
    surface = _surface(text)
    allowed = any(_surface(term) in surface for term in families.get(family, ()))
    forbidden = any(_surface(term) in surface for term in _forbidden_for_family(family, families))
    return allowed and not forbidden


def _evaluate(args: argparse.Namespace, checkpoint_name: str) -> list[dict[str, Any]]:
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=args.tokenizer_out,
            checkpoints_root=args.work_dir / "checkpoints",
            checkpoint_name=checkpoint_name,
            generator_name="sf_10m_phase27_58_probe",
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
    buckets = sorted({str(row["family"]) for row in rows})
    return {
        "passed": sum(1 for row in rows if row["passed"]),
        "total": len(rows),
        "pass_rate": round(sum(1 for row in rows if row["passed"]) / len(rows), 4) if rows else 0.0,
        "family_summary": {
            family: {
                "passed": sum(1 for row in rows if row["family"] == family and row["passed"]),
                "total": sum(1 for row in rows if row["family"] == family),
            }
            for family in buckets
        },
        "reason_counts": dict(Counter(str(row["reason"]) for row in rows)),
    }


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.58 Tokenizer Bounded Alignment Probe", ""]
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
    tok = report["protected_phrase_behavior"]
    lines = [
        "# Phase 27.58 — Tokenizer v7 + Bounded Alignment Probe",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة تدريب محدودة وليست فتح واجهة.",
        "",
        f"- status: `{report['status']}`",
        f"- tokenizer: `{report['tokenizer']['path']}`",
        f"- protected terms/phrases: `{report['tokenizer']['protected_terms_count']}`",
        f"- Phase 27.57 protected max pieces: `{tok['phase27_57_max_pieces']}`",
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
    terms = _load_policy_terms()
    if args.reuse_existing and (args.tokenizer_out / "meta.json").exists():
        tokenizer = BPETokenizer.load(args.tokenizer_out)
    else:
        tokenizer = _train_tokenizer(args, terms)
    tokenizer_rows = _tokenizer_rows(tokenizer, terms)
    meta = json.loads((args.tokenizer_out / "meta.json").read_text(encoding="utf-8"))

    checkpoints = args.work_dir / "checkpoints"
    can_reuse_checkpoint = (
        args.reuse_existing
        and checkpoints.exists()
        and any(path.name == "meta.json" for path in checkpoints.glob("*/meta.json"))
    )

    if args.work_dir.exists() and not args.keep_work and not can_reuse_checkpoint:
        shutil.rmtree(args.work_dir)
    corpus_dir = args.work_dir / "corpus"
    records = _records()
    if can_reuse_checkpoint:
        checkpoint_name = _latest_checkpoint_name(checkpoints)
    else:
        _write_probe_corpus(corpus_dir, records)
        train_args = [
            "--tokenizer", str(args.tokenizer_out),
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
            "--seed", "20260624",
            "--checkpoints", str(checkpoints),
            "--device", args.device,
        ]
        train_code = train_tiny_lm_run(train_args)
        if train_code != 0:
            return train_code
        checkpoint_name = _latest_checkpoint_name(checkpoints)
    rows = _evaluate(args, checkpoint_name)
    summary = _summary(rows)
    phase57_rows = [row for row in tokenizer_rows if row["phase27_57_critical"]]
    phase57_piece_counts = [int(row["piece_count"]) for row in phase57_rows]
    passed = summary["passed"] == summary["total"]
    status = (
        "PASSED_TOKENIZER_V7_BOUNDED_ALIGNMENT_PROBE_RUNTIME_STILL_BLOCKED"
        if passed
        else "FAILED_TOKENIZER_V7_BOUNDED_ALIGNMENT_PROBE_RUNTIME_BLOCKED"
    )

    response_family_policy = json.loads(RESPONSE_FAMILIES.read_text(encoding="utf-8"))
    semantic_policy = json.loads(SEMANTIC_RULES.read_text(encoding="utf-8"))
    report = {
        "phase": "Phase 27.58",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "bounded SF-10M tokenizer/probe only; no runtime switch; no SF-50M",
        "tokenizer": {
            "path": _rel(args.tokenizer_out),
            "sf_origin": bool(meta.get("sf_origin")),
            "vocab_size": meta.get("vocab_size"),
            "merges": meta.get("merges"),
            "protected_terms_count": len(terms),
            "protected_joiner": meta.get("protected_joiner"),
        },
        "protected_phrase_behavior": {
            "average_pieces": round(mean(int(row["piece_count"]) for row in tokenizer_rows), 4) if tokenizer_rows else 0,
            "max_pieces": max((int(row["piece_count"]) for row in tokenizer_rows), default=0),
            "all_roundtrip_ok": all(bool(row["roundtrip_ok"]) for row in tokenizer_rows),
            "phase27_57_count": len(phase57_rows),
            "phase27_57_max_pieces": max(phase57_piece_counts, default=0),
            "phase27_57_all_single_piece": all(count == 1 for count in phase57_piece_counts),
            "rows": tokenizer_rows,
        },
        "alignment_policy": {
            "prompt_overlap_required": semantic_policy["decision_rules"]["prompt_overlap_required"],
            "cross_family_blocking_enabled": semantic_policy["decision_rules"]["cross_family_blocking_enabled"],
            "forbidden_collapses": response_family_policy["forbidden_collapses"],
        },
        "train_records": len(records),
        "checkpoint_root": _rel(checkpoints),
        "checkpoint_name": checkpoint_name,
        "candidate_generator": "sf_10m_phase27_58_probe",
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
            "Bounded alignment probe passed. Keep UI on current runtime and run a broader natural-dialogue canary before any switch."
            if passed
            else "Bounded alignment probe failed. Keep runtime blocked and inspect tokenizer/probe samples before more scaling."
        ),
        "next_phase": (
            "Phase 27.59 — broader natural-dialogue canary using tokenizer v7"
            if passed
            else "Phase 27.59 — inspect Phase 27.58 failures and repair bounded alignment"
        ),
        "torch_version": torch.__version__,
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)
    _write_doc(report, args.doc)

    print("SF.AI — Phase 27.58 tokenizer v7 bounded alignment probe")
    print(f"  status       : {status}")
    print(f"  tokenizer    : {_rel(args.tokenizer_out)}")
    print(f"  protected    : {len(terms)}")
    print(f"  phase27.57 max pieces: {max(phase57_piece_counts, default=0)}")
    print(f"  checkpoint   : {checkpoint_name}")
    print(f"  probe        : {summary['passed']}/{summary['total']}")
    print(f"  reasons      : {summary['reason_counts']}")
    print("  runtime      : blocked")
    print(f"  report       : {args.report}")
    print(f"  samples      : {args.samples}")
    print(f"  doc          : {args.doc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
