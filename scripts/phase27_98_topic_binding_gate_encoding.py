#!/usr/bin/env python3
"""Phase 27.98 — Topic Binding Gate Encoding and Metadata Audit.

No training. No tokenizer work. No runtime release.

This phase encodes the Phase 27.97 copy/contrastive objective as dry-run
checks, then decides whether bounded training is allowed or whether topic
metadata/copy-anchor data must be repaired first.
"""
# ruff: noqa: E402

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_26_heldout_objective_repair import _rel
from sf_ai.datasets import ChatDataset
from sf_ai.datasets.chat_dataset import render_dialogue_text
from sf_ai.datasets.loaders import iter_chat_samples
from sf_ai.datasets.schemas import StructuredSample
from sf_ai.models.tokenizer import BPETokenizer
from sf_ai.training.train_tiny_lm import _encode_training_text, _iter_training_texts

DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_97_topic_variable_binding_objective_design_report.json"
DEFAULT_SPEC = ROOT / "artifacts/reports/phase27_97_topic_variable_binding_objective_spec.json"
DEFAULT_CORPUS = ROOT / "data/corpus/chat/jsonl"
DEFAULT_SPLIT = ROOT / "data/corpus/chat/splits/dialogue_split_v1.json"
DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v9_phase27_76"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_98_topic_binding_gate_encoding_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_98_TOPIC_BINDING_GATE_ENCODING_DECISION.json"
DEFAULT_CANARY = ROOT / "eval/prompts/phase27_98_topic_binding_contrastive_canary.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_98_TOPIC_BINDING_GATE_ENCODING_REPORT.md"

TARGET_DIALECTS: tuple[str, ...] = ("msa", "saudi")
FRESH_PROMPTS: tuple[tuple[str, str, str], ...] = (
    ("الوفاء", "msa", "عرّف الوفاء بكلام بسيط."),
    ("التعاون", "saudi", "وش معنى التعاون في الحياة اليومية؟"),
    ("الصبر", "msa", "اشرح الصبر بجملة قصيرة."),
    ("الاحترام", "saudi", "وش يعني الاحترام؟"),
    ("الهدوء", "msa", "ما المقصود بالهدوء؟"),
    ("الصدق", "saudi", "وش يعني الصدق باختصار؟"),
    ("الصداقة", "msa", "عرّف الصداقة دون إطالة."),
    ("الشجاعة", "saudi", "وش معنى الشجاعة؟"),
    ("الوفاء", "saudi", "علمني عن الوفاء بجملة وحدة."),
    ("الصبر", "saudi", "الصبر وش معناه؟"),
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.98 topic binding gate encoding")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--canary", type=Path, default=DEFAULT_CANARY)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args(argv)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _target_terms(spec: dict[str, Any]) -> tuple[str, ...]:
    return tuple(str(item) for item in spec["target_terms"])


def _sample(term: str, dialect: str) -> StructuredSample:
    user = f"ما معنى {term}؟" if dialect == "msa" else f"وش يعني {term}؟"
    answer = (
        f"معنى {term}: خلق يظهر في المواقف اليومية بوضوح."
        if dialect == "msa"
        else f"{term} يعني خلق يبان في المواقف اليومية."
    )
    return StructuredSample(
        domain="chat",
        lang="ar",
        messages=[
            {"role": "user", "content": user},
            {"role": "assistant", "content": answer},
        ],
        provenance={
            "dialect": dialect,
            "dialogue_family": "topic",
            "prompt_family": "topic",
            "answer_family": "topic",
            "topic_term": term,
        },
    )


def _assistant_text(sample: StructuredSample) -> str:
    return " ".join(
        message.content.strip()
        for message in sample.messages
        if message.role == "assistant" and message.content.strip()
    ).strip()


def _copy_anchor_ok(answer: str, term: str) -> bool:
    compact = "".join(ch for ch in answer if not ch.isspace())
    return bool(term and compact.find(term) != -1 and compact.find(term) <= 12)


def _infer_topic(text: str, terms: tuple[str, ...]) -> str:
    for term in terms:
        if term in text:
            return term
    return ""


def _renderer_probe(terms: tuple[str, ...]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for term in terms:
        for dialect in TARGET_DIALECTS:
            sample = _sample(term, dialect)
            rendered = render_dialogue_text(sample)
            answer = _assistant_text(sample)
            topic_line = f"الموضوع المطلوب: {term}"
            rows.append(
                {
                    "term": term,
                    "dialect": dialect,
                    "has_topic_line": topic_line in rendered,
                    "topic_line_before_user": rendered.index(topic_line) < rendered.index("المستخدم:"),
                    "assistant_copy_anchor": _copy_anchor_ok(answer, term),
                    "preview": rendered,
                }
            )
    return {
        "passed": all(
            row["has_topic_line"]
            and row["topic_line_before_user"]
            and row["assistant_copy_anchor"]
            for row in rows
        ),
        "rows": rows,
    }


def _mask_probe(tokenizer_path: Path) -> dict[str, Any]:
    tokenizer = BPETokenizer.load(tokenizer_path)
    text = (
        "النطاق: سعودي\n"
        "عائلة الحوار: موضوع\n"
        "الموضوع المطلوب: الشجاعة\n"
        "المستخدم: وش يعني الشجاعة؟\n"
        "المساعد: الشجاعة يعني فعل الصواب رغم الخوف.\n"
    )
    ids, labels = _encode_training_text(
        tokenizer,
        text,
        stream_format="dialogue",
        loss_scope="assistant",
    )
    masked_prefix_token_count = sum(
        len(tokenizer.encode(line))
        for line in [
            "النطاق: سعودي",
            "عائلة الحوار: موضوع",
            "الموضوع المطلوب: الشجاعة",
            "المستخدم: وش يعني الشجاعة؟",
            "المساعد:",
        ]
    )
    prefix_masked = all(label == -100 for label in labels[:masked_prefix_token_count])
    assistant_supervised = any(label != -100 for label in labels[masked_prefix_token_count:])
    return {
        "tokenizer": _rel(tokenizer_path),
        "total_tokens": len(ids),
        "masked_tokens": sum(1 for label in labels if label == -100),
        "supervised_tokens": sum(1 for label in labels if label != -100),
        "conditioning_and_user_masked": prefix_masked,
        "assistant_content_supervised": assistant_supervised,
        "passed": prefix_masked and assistant_supervised,
    }


def _metadata_audit(corpus: Path, terms: tuple[str, ...]) -> dict[str, Any]:
    counts = Counter()
    dialect_counts = Counter()
    explicit_by_term: Counter[str] = Counter()
    inferred_by_term: Counter[str] = Counter()
    missing_by_file: Counter[str] = Counter()
    off_spec_examples: list[dict[str, str]] = []
    missing_examples: list[dict[str, str]] = []
    copy_anchor = Counter()

    for path in sorted(corpus.rglob("*.jsonl")):
        for sample in iter_chat_samples(path):
            provenance = getattr(sample, "provenance", None)
            family = (getattr(provenance, "dialogue_family", "") or "").strip()
            if family != "topic":
                continue

            counts["topic_records"] += 1
            dialect = (getattr(provenance, "dialect", "") or "").strip().lower()
            dialect_counts[dialect] += 1
            explicit = (getattr(provenance, "topic_term", "") or "").strip()
            messages = sample.messages if isinstance(sample, StructuredSample) else sample.to_messages()
            user = " ".join(msg.content.strip() for msg in messages if msg.role == "user")
            assistant = " ".join(msg.content.strip() for msg in messages if msg.role == "assistant")
            inferred = explicit or _infer_topic(f"{user}\n{assistant}", terms)

            if explicit:
                counts["explicit_topic_term_records"] += 1
                explicit_by_term[explicit] += 1
            else:
                counts["missing_topic_term_records"] += 1
                missing_by_file[_rel(path)] += 1
                if len(missing_examples) < 12:
                    missing_examples.append(
                        {
                            "file": _rel(path),
                            "dialect": dialect,
                            "user": user[:100],
                            "assistant": assistant[:100],
                            "inferred_target_term": inferred,
                        }
                    )

            if inferred:
                inferred_by_term[inferred] += 1
                copy_anchor["ok" if _copy_anchor_ok(assistant, inferred) else "bad"] += 1
            else:
                copy_anchor["unknown_topic"] += 1
                if len(off_spec_examples) < 12:
                    off_spec_examples.append(
                        {
                            "file": _rel(path),
                            "dialect": dialect,
                            "user": user[:100],
                            "assistant": assistant[:100],
                        }
                    )

    target_term_records = sum(inferred_by_term.values())
    return {
        "total_topic_records": counts["topic_records"],
        "explicit_topic_term_records": counts["explicit_topic_term_records"],
        "missing_topic_term_records": counts["missing_topic_term_records"],
        "all_topic_records_have_explicit_topic_term": counts["missing_topic_term_records"] == 0,
        "dialect_counts": dict(dialect_counts),
        "explicit_by_term": dict(explicit_by_term),
        "inferred_by_target_term": dict(inferred_by_term),
        "missing_by_file_top": dict(missing_by_file.most_common(12)),
        "missing_examples": missing_examples,
        "off_spec_topic_examples": off_spec_examples,
        "copy_anchor": {
            "target_term_records": target_term_records,
            "ok": copy_anchor["ok"],
            "bad": copy_anchor["bad"],
            "unknown_topic": copy_anchor["unknown_topic"],
            "target_term_copy_anchor_ready": target_term_records > 0
            and copy_anchor["bad"] == 0,
            "all_topic_copy_anchor_ready": counts["topic_records"] > 0
            and copy_anchor["bad"] == 0
            and copy_anchor["unknown_topic"] == 0,
        },
    }


def _canary_manifest(terms: tuple[str, ...]) -> dict[str, Any]:
    prompts: list[dict[str, Any]] = []
    for term in terms:
        forbidden = [other for other in terms if other != term]
        for dialect in TARGET_DIALECTS:
            message = f"اشرح لي {term} بجملة قصيرة." if dialect == "msa" else f"وش يعني {term} باختصار؟"
            prompts.append(
                {
                    "id": f"known_{dialect}_{term}",
                    "set": "known",
                    "dialect": dialect,
                    "dialogue_family": "topic",
                    "message": message,
                    "requested_topic": term,
                    "required_terms": [term],
                    "forbidden_terms": forbidden,
                    "copy_anchor_required": True,
                    "copy_anchor_max_visible_arabic_chars": 12,
                    "accepted_prefixes": [f"معنى {term}:", f"{term} يعني", f"{term} هو"],
                    "max_sentences": 1,
                }
            )
    for idx, (term, dialect, message) in enumerate(FRESH_PROMPTS, start=1):
        forbidden = [other for other in terms if other != term]
        prompts.append(
            {
                "id": f"fresh_{idx:02d}_{dialect}_{term}",
                "set": "fresh",
                "dialect": dialect,
                "dialogue_family": "topic",
                "message": message,
                "requested_topic": term,
                "required_terms": [term],
                "forbidden_terms": forbidden,
                "copy_anchor_required": True,
                "copy_anchor_max_visible_arabic_chars": 12,
                "accepted_prefixes": [f"معنى {term}:", f"{term} يعني", f"{term} هو"],
                "max_sentences": 1,
            }
        )
    return {
        "suite_id": "phase27_98_topic_binding_contrastive_canary",
        "phase": "Phase 27.98",
        "objective": "topic_copy_contrastive_binding_objective_v1",
        "language_track": list(TARGET_DIALECTS),
        "target_terms": list(terms),
        "thresholds": {
            "known_topic_min": "16/16",
            "fresh_topic_min": "8/10",
            "contrastive_wrong_topic_max": 0,
            "copy_anchor_min": "26/26",
            "all_family_regression_min": "45/50",
            "topic_family_min": "8/10",
            "malformed_max": 0,
            "repeated_phrase_max": 0,
        },
        "coverage": {
            "prompt_count": len(prompts),
            "known_count": sum(1 for row in prompts if row["set"] == "known"),
            "fresh_count": sum(1 for row in prompts if row["set"] == "fresh"),
            "all_terms_covered": {row["requested_topic"] for row in prompts} == set(terms),
            "all_dialects_covered": {row["dialect"] for row in prompts} == set(TARGET_DIALECTS),
        },
        "prompts": prompts,
    }


def _stream_probe(corpus: Path, split_manifest: Path) -> dict[str, Any]:
    dataset = ChatDataset(corpus)
    first_topic = next(
        (
            text
            for text in _iter_training_texts(
                dataset,
                stream_format="dialogue",
                split_manifest=split_manifest,
                split_name="train",
                split_order="family_round_robin",
            )
            if "عائلة الحوار: موضوع" in text
        ),
        "",
    )
    return {
        "split_order": "family_round_robin",
        "has_topic_sample_in_training_stream": bool(first_topic),
        "has_topic_anchor_in_first_topic_sample": "الموضوع المطلوب:" in first_topic,
        "preview": first_topic,
    }


def _topic_round_robin_probe(metadata: dict[str, Any]) -> dict[str, Any]:
    inferred = metadata["inferred_by_target_term"]
    queues = {
        term: deque(range(count))
        for term, count in inferred.items()
        if count > 0
    }
    sequence: list[str] = []
    while queues and len(sequence) < 80:
        for term in sorted(list(queues)):
            if queues[term]:
                queues[term].popleft()
                sequence.append(term)
            if not queues[term]:
                del queues[term]
        if not queues:
            break
    window = Counter(sequence[:80])
    all_terms_present = all(count > 0 for count in window.values()) and len(window) >= 8
    return {
        "proposed_sampler": "topic_term_round_robin_within_family_round_robin",
        "dry_run_possible_from_inferred_terms": bool(sequence),
        "blocked_for_training": not metadata["all_topic_records_have_explicit_topic_term"],
        "reason": (
            "training sampler cannot rely on inferred topic terms; explicit provenance.topic_term is required"
            if not metadata["all_topic_records_have_explicit_topic_term"]
            else "explicit metadata is available"
        ),
        "preview_first_80_counts": dict(window),
        "all_target_terms_present_in_preview": all_terms_present,
    }


def build_report(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    source = _load_json(args.source)
    spec = _load_json(args.spec)
    source_decision = source["decision"]["engineering_decision"]
    if source_decision != "ALLOW_PHASE27_98_TOPIC_BINDING_GATE_ENCODING_NO_TRAINING":
        raise ValueError("Phase 27.97 did not allow Phase 27.98 gate encoding")

    terms = _target_terms(spec)
    renderer = _renderer_probe(terms)
    mask = _mask_probe(args.tokenizer)
    metadata = _metadata_audit(args.corpus, terms)
    canary = _canary_manifest(terms)
    stream = _stream_probe(args.corpus, args.split_manifest)
    round_robin = _topic_round_robin_probe(metadata)

    canary_ready = bool(
        canary["coverage"]["prompt_count"] == 26
        and canary["coverage"]["known_count"] == 16
        and canary["coverage"]["fresh_count"] == 10
        and canary["coverage"]["all_terms_covered"]
        and canary["coverage"]["all_dialects_covered"]
    )
    encoded_gate_passed = bool(renderer["passed"] and mask["passed"] and canary_ready)
    metadata_ready = bool(metadata["all_topic_records_have_explicit_topic_term"])
    copy_anchor_ready = bool(metadata["copy_anchor"]["all_topic_copy_anchor_ready"])
    sampler_ready = bool(
        metadata_ready
        and round_robin["all_target_terms_present_in_preview"]
        and not round_robin["blocked_for_training"]
    )
    training_ready = bool(encoded_gate_passed and metadata_ready and copy_anchor_ready and sampler_ready)

    decision = {
        "decision_id": "PHASE27_98_TOPIC_BINDING_GATE_ENCODING_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_99_BOUNDED_TOPIC_BINDING_REPAIR_TRAINING"
            if training_ready
            else "ALLOW_PHASE27_99_TOPIC_METADATA_COPY_ANCHOR_DATA_REPAIR_NO_TRAINING"
        ),
        "new_training_allowed": training_ready,
        "data_repair_allowed": not training_ready,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "why": (
            "Gate encoding works, but corpus metadata/copy-anchor readiness is not strict enough "
            "for the Phase 27.97 objective."
            if not training_ready
            else "Gate encoding, metadata, copy-anchor, and sampler readiness all passed."
        ),
        "next_phase": (
            "Phase 27.99 — Topic Metadata and Copy-Anchor Data Repair"
            if not training_ready
            else "Phase 27.99 — Bounded Topic Binding Repair Training"
        ),
    }
    report = {
        "phase": "Phase 27.98",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_98_TOPIC_BINDING_GATE_ENCODED_DATA_REPAIR_REQUIRED_NO_TRAINING"
            if not training_ready and encoded_gate_passed
            else "PHASE27_98_TOPIC_BINDING_GATE_PASSED_TRAINING_ALLOWED_NEXT"
            if training_ready
            else "PHASE27_98_TOPIC_BINDING_GATE_FAILED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "source_report": _rel(args.source),
        "spec": _rel(args.spec),
        "renderer_probe": renderer,
        "mask_probe": mask,
        "stream_probe": stream,
        "canary_manifest_path": _rel(args.canary),
        "canary_ready": canary_ready,
        "metadata_audit": metadata,
        "topic_round_robin_probe": round_robin,
        "encoded_gate_passed": encoded_gate_passed,
        "metadata_ready": metadata_ready,
        "copy_anchor_ready": copy_anchor_ready,
        "sampler_ready": sampler_ready,
        "training_ready": training_ready,
        "blocked_actions": [
            "LM training before data repair",
            "runtime release",
            "UI generator release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
            "keyword/template masking",
        ],
        "decision": decision,
    }
    return report, canary


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    meta = report["metadata_audit"]
    lines = [
        "# Phase 27.98 — Topic Binding Gate Encoding and Metadata Audit",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة بوابة فقط. لا تدريب ولا runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- encoded gate passed: `{report['encoded_gate_passed']}`",
        f"- metadata ready: `{report['metadata_ready']}`",
        f"- copy-anchor ready: `{report['copy_anchor_ready']}`",
        f"- sampler ready: `{report['sampler_ready']}`",
        f"- training allowed: `{decision['new_training_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## ما ثبت",
        "",
        "- renderer يستطيع إنتاج target يبدأ بالموضوع المطلوب.",
        "- assistant-only loss يبقي سطور السياق والطلب masked.",
        "- canary contrastive جديد يغطي 26 حالة: 16 known و10 fresh.",
        "",
        "## سبب منع التدريب",
        "",
        f"- total topic records: `{meta['total_topic_records']}`",
        f"- explicit topic_term records: `{meta['explicit_topic_term_records']}`",
        f"- missing topic_term records: `{meta['missing_topic_term_records']}`",
        f"- copy-anchor unknown topic: `{meta['copy_anchor']['unknown_topic']}`",
        f"- copy-anchor bad: `{meta['copy_anchor']['bad']}`",
        "",
        "## القرار",
        "",
        decision["why"],
        "",
        "## الملفات الأكثر احتياجًا لإصلاح metadata",
        "",
    ]
    for file_name, count in meta["missing_by_file_top"].items():
        lines.append(f"- `{file_name}`: `{count}`")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        report, canary = build_report(args)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.decision.write_text(
        json.dumps(report["decision"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    args.canary.parent.mkdir(parents=True, exist_ok=True)
    args.canary.write_text(json.dumps(canary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_doc(args.doc, report)

    print(report["status"])
    print(report["decision"]["engineering_decision"])
    print(f"encoded_gate_passed={report['encoded_gate_passed']}")
    print(f"metadata_ready={report['metadata_ready']}")
    print(f"missing_topic_term_records={report['metadata_audit']['missing_topic_term_records']}")
    print(f"report={_rel(args.report)}")
    return 0 if report["encoded_gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
