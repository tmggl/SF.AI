#!/usr/bin/env python3
"""Phase 27.93 — Topic Objective Gate Encoding and Dry-Run Validation.

No training. No runtime release. This phase encodes the Phase 27.92
topic-objective design into renderer/eval dry-runs, then decides whether data
is sufficient for bounded training or whether a topic data pack is required.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets import ChatDataset  # noqa: E402
from sf_ai.datasets.chat_dataset import (  # noqa: E402
    TOPIC_CONDITION_TERMS,
    render_dialogue_text,
)
from sf_ai.datasets.loaders import iter_chat_samples  # noqa: E402
from sf_ai.datasets.schemas import StructuredSample  # noqa: E402
from sf_ai.models.tokenizer import BPETokenizer  # noqa: E402
from sf_ai.training.train_tiny_lm import (  # noqa: E402
    _encode_training_text,
    _iter_training_texts,
)

DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_92_topic_objective_repair_design_gate_report.json"
DEFAULT_CORPUS = ROOT / "data/corpus/chat/jsonl"
DEFAULT_SPLIT = ROOT / "data/corpus/chat/splits/dialogue_split_v1.json"
DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v9_phase27_76"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_93_topic_objective_gate_encoding_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_DECISION.json"
DEFAULT_CANARY = ROOT / "eval/prompts/phase27_93_topic_objective_canary.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_REPORT.md"

MIN_PER_TOPIC = 20
MIN_PER_DIALECT = 10
TARGET_DIALECTS = ("msa", "saudi")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.93 topic objective dry-run gate")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--canary", type=Path, default=DEFAULT_CANARY)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args(argv)


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _sample(term: str, dialect: str) -> StructuredSample:
    user = f"ما معنى {term}؟" if dialect == "msa" else f"وش يعني {term}؟"
    answer = (
        f"{term} خلق واضح يظهر في التصرف اليومي."
        if dialect == "msa"
        else f"{term} يظهر في المواقف اليومية بكلام وفعل واضح."
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


def _renderer_probe() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for term in TOPIC_CONDITION_TERMS:
        for dialect in TARGET_DIALECTS:
            text = render_dialogue_text(_sample(term, dialect))
            expected_topic = f"الموضوع المطلوب: {term}"
            rows.append(
                {
                    "term": term,
                    "dialect": dialect,
                    "preview": text,
                    "has_dialect_line": ("النطاق: فصحى" in text or "النطاق: سعودي" in text),
                    "has_family_line": "عائلة الحوار: موضوع" in text,
                    "has_topic_line": expected_topic in text,
                    "topic_before_user": text.index(expected_topic) < text.index("المستخدم:"),
                    "has_user_line": "المستخدم:" in text,
                    "has_assistant_line": "المساعد:" in text,
                }
            )
    passed = all(
        row["has_dialect_line"]
        and row["has_family_line"]
        and row["has_topic_line"]
        and row["topic_before_user"]
        and row["has_user_line"]
        and row["has_assistant_line"]
        for row in rows
    )
    return {"passed": passed, "rows": rows}


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
            if "عائلة الحوار: موضوع" in text and "الموضوع المطلوب:" in text
        ),
        "",
    )
    return {
        "split_order": "family_round_robin",
        "has_topic_anchor_in_training_stream": bool(first_topic),
        "preview": first_topic,
    }


def _mask_probe(tokenizer_path: Path) -> dict[str, Any]:
    tokenizer = BPETokenizer.load(tokenizer_path)
    text = (
        "النطاق: سعودي\n"
        "عائلة الحوار: موضوع\n"
        "الموضوع المطلوب: الشجاعة\n"
        "المستخدم: وش يعني الشجاعة؟\n"
        "المساعد: الشجاعة فعل الصواب رغم الخوف.\n"
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
        "text": text,
        "total_tokens": len(ids),
        "masked_tokens": sum(1 for label in labels if label == -100),
        "supervised_tokens": sum(1 for label in labels if label != -100),
        "conditioning_and_user_masked": prefix_masked,
        "assistant_content_supervised": assistant_supervised,
        "passed": prefix_masked and assistant_supervised,
    }


def _canary_manifest() -> dict[str, Any]:
    prompts: list[dict[str, Any]] = []
    for term in TOPIC_CONDITION_TERMS:
        other_terms = [other for other in TOPIC_CONDITION_TERMS if other != term]
        prompts.extend(
            [
                {
                    "id": f"topic_msa_{term}",
                    "dialect": "msa",
                    "dialogue_family": "topic",
                    "message": f"اشرح لي {term} بجملة قصيرة.",
                    "required_terms": [term],
                    "forbidden_terms": other_terms,
                    "max_sentences": 1,
                },
                {
                    "id": f"topic_saudi_{term}",
                    "dialect": "saudi",
                    "dialogue_family": "topic",
                    "message": f"وش يعني {term} باختصار؟",
                    "required_terms": [term],
                    "forbidden_terms": other_terms,
                    "max_sentences": 1,
                },
            ]
        )
    dialect_counts = Counter(row["dialect"] for row in prompts)
    term_counts = Counter(row["required_terms"][0] for row in prompts)
    return {
        "suite_id": "phase27_93_topic_objective_canary",
        "phase": "Phase 27.93",
        "language_track": ["msa", "saudi"],
        "target_terms": list(TOPIC_CONDITION_TERMS),
        "thresholds": {
            "known_topic_canary_min": "18/20",
            "fresh_topic_shadow_min": "16/20",
            "all_family_regression_min": "45/50",
            "topic_family_min": "8/10",
            "malformed_max": 0,
            "repeated_phrase_max": 0,
        },
        "prompts": prompts,
        "coverage": {
            "prompt_count": len(prompts),
            "dialect_counts": dict(dialect_counts),
            "term_counts": dict(term_counts),
            "all_terms_covered": set(term_counts) == set(TOPIC_CONDITION_TERMS),
            "all_dialects_covered": set(dialect_counts) == set(TARGET_DIALECTS),
        },
    }


def _corpus_topic_coverage(corpus: Path) -> dict[str, Any]:
    counts: dict[str, Counter[str]] = {
        term: Counter() for term in TOPIC_CONDITION_TERMS
    }
    examples: dict[str, list[str]] = defaultdict(list)
    for path in sorted(corpus.rglob("*.jsonl")):
        for sample in iter_chat_samples(path):
            provenance = getattr(sample, "provenance", None)
            family = (getattr(provenance, "dialogue_family", "") or "").strip()
            if family != "topic":
                continue
            messages = sample.messages if isinstance(sample, StructuredSample) else sample.to_messages()
            user_text = " ".join(msg.content for msg in messages if msg.role == "user")
            dialect = (getattr(provenance, "dialect", "") or "").strip().lower()
            explicit_topic = (getattr(provenance, "topic_term", "") or "").strip()
            for term in TOPIC_CONDITION_TERMS:
                if explicit_topic == term or term in user_text:
                    counts[term][dialect] += 1
                    if len(examples[term]) < 3:
                        examples[term].append(user_text)
    term_rows: dict[str, dict[str, Any]] = {}
    shortfalls: dict[str, dict[str, int]] = {}
    for term, term_counts in counts.items():
        total = sum(term_counts.values())
        dialect_shortfalls = {
            dialect: max(0, MIN_PER_DIALECT - int(term_counts.get(dialect, 0)))
            for dialect in TARGET_DIALECTS
        }
        total_shortfall = max(0, MIN_PER_TOPIC - total)
        term_rows[term] = {
            "total": total,
            "dialect_counts": {dialect: int(term_counts.get(dialect, 0)) for dialect in TARGET_DIALECTS},
            "examples": examples.get(term, []),
            "meets_total_min": total >= MIN_PER_TOPIC,
            "meets_dialect_min": all(value == 0 for value in dialect_shortfalls.values()),
        }
        if total_shortfall or any(dialect_shortfalls.values()):
            shortfalls[term] = {
                "total_shortfall": total_shortfall,
                **{f"{dialect}_shortfall": value for dialect, value in dialect_shortfalls.items()},
            }
    return {
        "criteria": {
            "min_per_topic": MIN_PER_TOPIC,
            "min_per_dialect": MIN_PER_DIALECT,
            "dialects": list(TARGET_DIALECTS),
        },
        "terms": term_rows,
        "shortfalls": shortfalls,
        "training_data_ready": not shortfalls,
    }


def build_report(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    source = _load_json(args.source)
    source_decision = source["decision"]["engineering_decision"]
    if source_decision != "ALLOW_PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_NO_TRAINING":
        raise ValueError("Phase 27.92 did not allow Phase 27.93 gate encoding")

    renderer = _renderer_probe()
    stream = _stream_probe(args.corpus, args.split_manifest)
    mask = _mask_probe(args.tokenizer)
    canary = _canary_manifest()
    coverage = _corpus_topic_coverage(args.corpus)
    canary_ready = bool(
        canary["coverage"]["all_terms_covered"]
        and canary["coverage"]["all_dialects_covered"]
        and canary["coverage"]["prompt_count"] == 16
    )
    dry_run_passed = bool(
        renderer["passed"]
        and stream["has_topic_anchor_in_training_stream"]
        and mask["passed"]
        and canary_ready
    )
    training_data_ready = bool(coverage["training_data_ready"])
    decision = {
        "decision_id": "PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_95_BOUNDED_TOPIC_OBJECTIVE_REPAIR_TRAINING"
            if dry_run_passed and training_data_ready
            else "ALLOW_PHASE27_94_TOPIC_OBJECTIVE_DATA_PACK_AUTHORING_NO_TRAINING"
        ),
        "new_training_allowed": bool(dry_run_passed and training_data_ready),
        "data_pack_authoring_allowed": bool(dry_run_passed and not training_data_ready),
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "why": (
            "Topic-objective dry-run passed, but current topic corpus does not meet "
            "the per-topic/per-dialect minimums from Phase 27.92."
            if dry_run_passed and not training_data_ready
            else "Topic-objective dry-run and data readiness both passed."
        ),
        "next_phase": (
            "Phase 27.94 — Topic Objective Data Pack Authoring"
            if dry_run_passed and not training_data_ready
            else "Phase 27.95 — Bounded Topic Objective Repair Training"
        ),
    }
    report = {
        "phase": "Phase 27.93",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_93_TOPIC_OBJECTIVE_GATE_PASSED_DATA_PACK_REQUIRED_NO_TRAINING"
            if dry_run_passed and not training_data_ready
            else "PHASE27_93_TOPIC_OBJECTIVE_GATE_PASSED_TRAINING_ALLOWED_NEXT"
            if dry_run_passed
            else "PHASE27_93_TOPIC_OBJECTIVE_GATE_FAILED_TRAINING_BLOCKED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "source_report": _rel(args.source),
        "renderer_probe": renderer,
        "stream_probe": stream,
        "mask_probe": mask,
        "canary_manifest_path": _rel(args.canary),
        "canary_ready": canary_ready,
        "corpus_topic_coverage": coverage,
        "dry_run_passed": dry_run_passed,
        "training_data_ready": training_data_ready,
        "blocked_actions": [
            "runtime release",
            "UI generator release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
            "blind full retraining",
        ],
        "decision": decision,
    }
    return report, canary


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.93 — Topic Objective Gate Encoding",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة ترميز وتحقيق جاف فقط. لا تدريب ولا runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- dry-run passed: `{report['dry_run_passed']}`",
        f"- training data ready: `{report['training_data_ready']}`",
        f"- training allowed: `{decision['new_training_allowed']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## ما ثبت",
        "",
        "- renderer يضيف `الموضوع المطلوب: <topic_term>` لعائلة topic.",
        "- assistant-only loss يخفي سطور السياق والطلب عن الهدف.",
        "- canary manifest يغطي كل الموضوعات الثمانية بالفصحى والسعودي.",
        "",
        "## فجوة البيانات",
        "",
    ]
    for term, shortfall in report["corpus_topic_coverage"]["shortfalls"].items():
        lines.append(f"- `{term}`: `{shortfall}`")
    lines.extend(
        [
            "",
            "## القرار",
            "",
            decision["why"],
            "",
        ]
    )
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
    print(json.dumps(report["decision"], ensure_ascii=False, indent=2))
    return 0 if report["dry_run_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
