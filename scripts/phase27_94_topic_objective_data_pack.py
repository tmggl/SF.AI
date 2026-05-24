#!/usr/bin/env python3
"""Phase 27.94 — Topic Objective Data Pack Authoring.

No training. This phase authors a small, owner-delegated Saudi topic pack for
the exact gap found by Phase 27.93: الوفاء has no Saudi coverage.
"""
# ruff: noqa: E402, I001

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_93_topic_objective_gate_encoding import (  # noqa: E402
    build_report as build_phase27_93_report,
    parse_args as parse_phase27_93_args,
)
from sf_ai.datasets.corpus_governance import audit_jsonl_file_for_training  # noqa: E402
from sf_ai.datasets.splits import write_split_manifest  # noqa: E402

OUT_DIR = ROOT / "data/corpus/chat/jsonl"
OUT_FILE = OUT_DIR / "dialogue_batch_v11_topic_objective_wafa_saudi_011.jsonl"
SPLIT = ROOT / "data/corpus/chat/splits/dialogue_split_v1.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_94_topic_objective_data_pack_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_94_TOPIC_OBJECTIVE_DATA_PACK_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_94_TOPIC_OBJECTIVE_DATA_PACK_REPORT.md"


WAFA_SAUDI_PAIRS: tuple[tuple[str, str], ...] = (
    ("وش يعني الوفاء؟", "الوفاء إنك تثبت مع الشخص وتحفظ العهد حتى بعد الغياب."),
    ("كيف يكون الوفاء بين الأصحاب؟", "الوفاء إنك توقف مع خويك وقت الحاجة ولا تتغير بلا سبب."),
    ("ابي أفهم الوفاء ببساطة.", "الوفاء إنك تحفظ المعروف وترد الجميل بفعل واضح."),
    ("الوفاء كيف يظهر بالحياة؟", "الوفاء يظهر لما تلتزم بوعدك وتراعي من وثق فيك."),
    ("وش مثال على الوفاء؟", "الوفاء مثل إنك تسأل عن شخص وقف معك ولا تنساه."),
    ("ليش الوفاء مهم؟", "الوفاء يقوي العلاقة ويخلي الناس تطمئن لبعضها."),
    ("متى يظهر الوفاء في الشخص؟", "الوفاء يبان في الشخص إذا حفظ الوعد وقت الجد."),
    ("كيف أتعلم الوفاء؟", "الوفاء يبدأ بأن تلتزم بكلمتك وتحترم المعروف."),
    ("وش ضد الوفاء؟", "الوفاء يضعف إذا نسي الإنسان العهد وتخلى بلا سبب."),
    ("كيف أحافظ على الوفاء؟", "الوفاء يحتاج تذكر المعروف والالتزام بما وعدت به."),
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Author Phase 27.94 topic-objective data pack")
    p.add_argument("--out", type=Path, default=OUT_FILE)
    p.add_argument("--split", type=Path, default=SPLIT)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args(argv)


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def _record(index: int, user: str, assistant: str) -> dict[str, Any]:
    return {
        "domain": "chat",
        "lang": "ar",
        "messages": [
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "provenance": {
            "source": "sf-ai-topic-objective-wafa-saudi-pack-v1",
            "license": "owner-approved-for-sf-ai-training",
            "language": "ar",
            "dialect": "saudi",
            "quality": "gold",
            "training_allowed": True,
            "owner_user_id": "sami-local",
            "created_by_user_id": "sf-ai-local-author",
            "target_user_id": "sami-local",
            "user_scope": "single_user",
            "dialogue_family": "topic",
            "prompt_family": "topic",
            "answer_family": "topic",
            "topic_term": "الوفاء",
            "pack_id": "phase27_94_topic_objective_wafa_saudi_pack_v1",
            "pack_index": index,
            "notes": (
                "owner-delegated Saudi topic-objective dialogue; no external dataset; "
                "no pretrained output; gap-fill for Phase 27.93 الوفاء shortfall"
            ),
        },
    }


def _records() -> list[dict[str, Any]]:
    return [_record(index, user, assistant) for index, (user, assistant) in enumerate(WAFA_SAUDI_PAIRS, 1)]


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _audit_json(report: Any) -> dict[str, Any]:
    return {
        "path": str(report.path) if report.path else "",
        "total_records": report.total_records,
        "training_ready": report.training_ready,
        "error_count": report.error_count,
        "dialect_counts": report.dialect_counts,
        "quality_counts": report.quality_counts,
        "source_counts": report.source_counts,
        "issues": [
            {
                "line_number": issue.line_number,
                "kind": issue.kind,
                "message": issue.message,
                "snippet": issue.snippet,
            }
            for issue in report.issues
        ],
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    records = _records()
    _write_jsonl(args.out, records)
    file_audit = audit_jsonl_file_for_training(args.out)
    split_manifest = write_split_manifest(
        OUT_DIR,
        args.split,
        eval_ratio=0.10,
        salt="sf-ai-dialogue-v1",
    )
    post_gate, _canary = build_phase27_93_report(parse_phase27_93_args([]))
    post_coverage = post_gate["corpus_topic_coverage"]
    training_ready = bool(post_gate["training_data_ready"] and post_gate["dry_run_passed"])
    decision = {
        "decision_id": "PHASE27_94_TOPIC_OBJECTIVE_DATA_PACK_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_95_BOUNDED_TOPIC_OBJECTIVE_REPAIR_TRAINING"
            if training_ready
            else "BLOCK_PHASE27_95_FIX_TOPIC_DATA_PACK"
        ),
        "new_training_started": False,
        "phase27_95_training_allowed": training_ready,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "why": (
            "The Saudi الوفاء gap is closed and the topic-objective dry-run is ready for one bounded SF-10M repair."
            if training_ready
            else "Topic-objective data coverage is still incomplete."
        ),
        "next_phase": (
            "Phase 27.95 — Bounded Topic Objective Repair Training"
            if training_ready
            else "Phase 27.94b — Topic Objective Data Pack Repair"
        ),
    }
    return {
        "phase": "Phase 27.94",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_94_TOPIC_OBJECTIVE_DATA_PACK_READY_FOR_BOUNDED_TRAINING"
            if training_ready
            else "PHASE27_94_TOPIC_OBJECTIVE_DATA_PACK_INCOMPLETE"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "authored_file": _rel(args.out),
        "records_authored": len(records),
        "topic_term": "الوفاء",
        "dialect": "saudi",
        "quality": "gold",
        "file_audit": _audit_json(file_audit),
        "split_manifest": {
            "path": _rel(args.split),
            "total_records": split_manifest["total_records"],
            "counts": split_manifest["counts"],
            "dialects": split_manifest["dialects"],
            "qualities": split_manifest["qualities"],
        },
        "post_pack_phase27_93_gate": {
            "dry_run_passed": post_gate["dry_run_passed"],
            "training_data_ready": post_gate["training_data_ready"],
            "status": post_gate["status"],
            "shortfalls": post_coverage["shortfalls"],
            "wafa_counts": post_coverage["terms"]["الوفاء"],
        },
        "blocked_actions": [
            "runtime release",
            "UI generator release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
        ],
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.94 — Topic Objective Data Pack",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة بيانات فقط: لا تدريب ولا runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- authored file: `{report['authored_file']}`",
        f"- records authored: `{report['records_authored']}`",
        f"- topic: `{report['topic_term']}`",
        f"- dialect: `{report['dialect']}`",
        f"- training started: `{report['training_started']}`",
        f"- phase27_95 training allowed: `{decision['phase27_95_training_allowed']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## بعد الحزمة",
        "",
        f"- dry-run passed: `{report['post_pack_phase27_93_gate']['dry_run_passed']}`",
        f"- training data ready: `{report['post_pack_phase27_93_gate']['training_data_ready']}`",
        f"- الوفاء counts: `{report['post_pack_phase27_93_gate']['wafa_counts']}`",
        f"- remaining shortfalls: `{report['post_pack_phase27_93_gate']['shortfalls']}`",
        "",
        "## القرار",
        "",
        decision["why"],
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    report = build_report(args)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.decision.write_text(
        json.dumps(report["decision"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_doc(args.doc, report)
    print(json.dumps(report["decision"], ensure_ascii=False, indent=2))
    return 0 if report["decision"]["phase27_95_training_allowed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
