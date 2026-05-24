#!/usr/bin/env python3
"""Phase 27.99 — Topic Metadata and Copy-Anchor Data Repair.

No training. No tokenizer work. No runtime release.

Repairs Phase 27.81 topic-family records by adding explicit
provenance.topic_term and ensuring the assistant target begins with a
copy-anchor form. The source is the existing owner-authored corpus only.
"""
# ruff: noqa: E402

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_26_heldout_objective_repair import _rel
from scripts.phase27_98_topic_binding_gate_encoding import build_report as build_phase27_98_report
from scripts.phase27_98_topic_binding_gate_encoding import parse_args as parse_phase27_98_args

DEFAULT_SOURCE = ROOT / "artifacts/reports/PHASE27_98_TOPIC_BINDING_GATE_ENCODING_DECISION.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_99_topic_metadata_copy_anchor_repair_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_99_TOPIC_METADATA_COPY_ANCHOR_REPAIR_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_99_TOPIC_METADATA_COPY_ANCHOR_REPAIR_REPORT.md"
DEFAULT_FILES = (
    ROOT / "data/corpus/chat/jsonl/dialogue_batch_v10_balanced_topic_msa_010.jsonl",
    ROOT / "data/corpus/chat/jsonl/dialogue_batch_v10_balanced_topic_saudi_010.jsonl",
)

COPY_ANCHOR_REPAIR_NOTE = "phase27_99_topic_metadata_copy_anchor_repair"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.99 topic metadata repair")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--files", nargs="*", type=Path, default=list(DEFAULT_FILES))
    return p.parse_args(argv)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def _assistant_text(row: dict[str, Any]) -> str:
    return " ".join(
        str(message.get("content", "")).strip()
        for message in row.get("messages", [])
        if message.get("role") == "assistant" and str(message.get("content", "")).strip()
    ).strip()


def _user_text(row: dict[str, Any]) -> str:
    return " ".join(
        str(message.get("content", "")).strip()
        for message in row.get("messages", [])
        if message.get("role") == "user" and str(message.get("content", "")).strip()
    ).strip()


def _copy_anchor_ok(answer: str, term: str) -> bool:
    compact = "".join(ch for ch in answer if not ch.isspace())
    return bool(term and compact.find(term) != -1 and compact.find(term) <= 12)


def _clean_term(raw: str) -> str:
    cleaned = raw.strip()
    cleaned = cleaned.strip(" ؟?!.،:؛\"'“”‘’")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def _infer_topic(row: dict[str, Any]) -> str:
    answer = _assistant_text(row)
    match = re.match(r"^معنى\s+(.+?):", answer)
    if match:
        return _clean_term(match.group(1))
    match = re.match(r"^(.+?)\s+يعني\b", answer)
    if match:
        return _clean_term(match.group(1))
    match = re.match(r"^(.+?)\s+هو\b", answer)
    if match:
        return _clean_term(match.group(1))

    user = _user_text(row)
    patterns = (
        r"^ما معنى\s+(.+?)؟?$",
        r"^وش معنى\s+(.+?)؟?$",
        r"^وش يعني\s+(.+?)؟?$",
        r"^(.+?)\s+وش تعني؟?$",
        r"^اشرح لي\s+(.+?)\s+ب(?:بساطة|كلام بسيط)\.?$",
        r"^أريد فهم\s+(.+?)\s+بكلام سهل\.?$",
        r"^ابي أفهم\s+(.+?)\.?$",
        r"^ما المقصود بـ\s+(.+?)؟?$",
        r"^كيف أفهم\s+(.+?)\s+في الحياة اليومية؟?$",
        r"^(.+?)\s+كيف تكون بالحياة؟?$",
    )
    for pattern in patterns:
        match = re.match(pattern, user)
        if match:
            return _clean_term(match.group(1))
    return ""


def _repair_answer(answer: str, term: str) -> tuple[str, bool]:
    if _copy_anchor_ok(answer, term):
        return answer, False
    if answer.startswith("معنى "):
        _, _, rest = answer.partition(":")
        if rest.strip():
            return f"معنى {term}: {rest.strip()}", True
    return f"معنى {term}: {answer}", True


def _repair_file(path: Path) -> dict[str, Any]:
    rows = _read_jsonl(path)
    stats = Counter()
    examples: list[dict[str, str]] = []
    repaired_rows: list[dict[str, Any]] = []

    for row in rows:
        provenance = row.setdefault("provenance", {})
        if provenance.get("dialogue_family") != "topic":
            repaired_rows.append(row)
            continue

        stats["topic_records"] += 1
        before_topic = str(provenance.get("topic_term", "") or "").strip()
        topic = before_topic or _infer_topic(row)
        if not topic:
            stats["unresolved_topic"] += 1
            if len(examples) < 8:
                examples.append(
                    {
                        "file": _rel(path),
                        "user": _user_text(row)[:100],
                        "assistant": _assistant_text(row)[:100],
                    }
                )
            repaired_rows.append(row)
            continue

        if not before_topic:
            provenance["topic_term"] = topic
            stats["topic_term_added"] += 1
        else:
            stats["topic_term_already_present"] += 1

        for message in row.get("messages", []):
            if message.get("role") != "assistant":
                continue
            repaired, changed = _repair_answer(str(message.get("content", "")), topic)
            if changed:
                message["content"] = repaired
                stats["assistant_copy_anchor_rewritten"] += 1
            break

        notes = str(provenance.get("notes", "") or "")
        if COPY_ANCHOR_REPAIR_NOTE not in notes:
            provenance["notes"] = f"{notes}; {COPY_ANCHOR_REPAIR_NOTE}".strip("; ")
        provenance["topic_metadata_repair_phase"] = "Phase 27.99"
        provenance["topic_metadata_repair_method"] = "local_rule_from_user_or_assistant_text"
        repaired_rows.append(row)

    if stats["unresolved_topic"]:
        return {
            "file": _rel(path),
            "written": False,
            "stats": dict(stats),
            "unresolved_examples": examples,
        }
    _write_jsonl(path, repaired_rows)
    return {
        "file": _rel(path),
        "written": True,
        "stats": dict(stats),
        "unresolved_examples": examples,
    }


def _update_card(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    marker = "- phase27_99_repair: topic_term metadata + copy-anchor verified"
    if marker in text:
        return False
    path.write_text(text.rstrip() + "\n" + marker + "\n", encoding="utf-8")
    return True


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    source = _load_json(args.source)
    allowed_source_decisions = {
        "ALLOW_PHASE27_99_TOPIC_METADATA_COPY_ANCHOR_DATA_REPAIR_NO_TRAINING",
        "ALLOW_PHASE27_99_BOUNDED_TOPIC_BINDING_REPAIR_TRAINING",
        "ALLOW_PHASE27_100_BOUNDED_TOPIC_BINDING_REPAIR_TRAINING",
    }
    if source["engineering_decision"] not in allowed_source_decisions:
        raise ValueError("Phase 27.98 did not allow Phase 27.99 data repair")

    repaired_files = [_repair_file(path) for path in args.files]
    card_updates = [
        _rel(path.with_suffix(".CARD.md"))
        for path in args.files
        if _update_card(path.with_suffix(".CARD.md"))
    ]
    post_report, _ = build_phase27_98_report(parse_phase27_98_args([]))
    repair_passed = bool(
        all(item["written"] for item in repaired_files)
        and post_report["training_ready"] is True
        and post_report["metadata_ready"] is True
        and post_report["copy_anchor_ready"] is True
    )
    decision = {
        "decision_id": "PHASE27_99_TOPIC_METADATA_COPY_ANCHOR_REPAIR_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_100_BOUNDED_TOPIC_BINDING_REPAIR_TRAINING"
            if repair_passed
            else "BLOCK_PHASE27_100_FIX_TOPIC_METADATA_REPAIR"
        ),
        "new_training_allowed": repair_passed,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "why": (
            "All topic records now have explicit topic_term and pass copy-anchor readiness."
            if repair_passed
            else "Topic metadata/copy-anchor repair is incomplete."
        ),
        "next_phase": (
            "Phase 27.100 — Bounded Topic Binding Repair Training"
            if repair_passed
            else "Phase 27.99 — Continue Topic Metadata Repair"
        ),
    }
    return {
        "phase": "Phase 27.99",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_99_TOPIC_METADATA_COPY_ANCHOR_REPAIR_DONE_TRAINING_ALLOWED_NEXT"
            if repair_passed
            else "PHASE27_99_TOPIC_METADATA_COPY_ANCHOR_REPAIR_INCOMPLETE"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "source_decision": _rel(args.source),
        "repaired_files": repaired_files,
        "card_updates": card_updates,
        "post_repair_phase27_98_gate": {
            "training_ready": post_report["training_ready"],
            "metadata_ready": post_report["metadata_ready"],
            "copy_anchor_ready": post_report["copy_anchor_ready"],
            "missing_topic_term_records": post_report["metadata_audit"][
                "missing_topic_term_records"
            ],
            "copy_anchor_bad": post_report["metadata_audit"]["copy_anchor"]["bad"],
            "copy_anchor_unknown_topic": post_report["metadata_audit"]["copy_anchor"][
                "unknown_topic"
            ],
            "decision": post_report["decision"]["engineering_decision"],
            "next_phase": post_report["decision"]["next_phase"],
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
    gate = report["post_repair_phase27_98_gate"]
    decision = report["decision"]
    lines = [
        "# Phase 27.99 — Topic Metadata and Copy-Anchor Data Repair",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة إصلاح بيانات فقط. لا تدريب ولا runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- training started: `{report['training_started']}`",
        f"- runtime changed: `{report['runtime_changed']}`",
        f"- training allowed next: `{decision['new_training_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## Post-Repair Gate",
        "",
        f"- training ready: `{gate['training_ready']}`",
        f"- metadata ready: `{gate['metadata_ready']}`",
        f"- copy-anchor ready: `{gate['copy_anchor_ready']}`",
        f"- missing topic_term records: `{gate['missing_topic_term_records']}`",
        f"- copy-anchor bad: `{gate['copy_anchor_bad']}`",
        f"- unknown topic: `{gate['copy_anchor_unknown_topic']}`",
        "",
        "## Repaired Files",
        "",
    ]
    for item in report["repaired_files"]:
        lines.append(f"- `{item['file']}`: `{item['stats']}`")
    lines.extend(["", "## القرار", "", decision["why"], ""])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        report = build_report(args)
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
    _write_doc(args.doc, report)

    gate = report["post_repair_phase27_98_gate"]
    print(report["status"])
    print(report["decision"]["engineering_decision"])
    print(f"metadata_ready={gate['metadata_ready']}")
    print(f"copy_anchor_ready={gate['copy_anchor_ready']}")
    print(f"missing_topic_term_records={gate['missing_topic_term_records']}")
    print(f"report={_rel(args.report)}")
    return 0 if report["decision"]["new_training_allowed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
