#!/usr/bin/env python3
"""Phase 27.86 — Family Conditioning Renderer Gate.

No training. No runtime release. This gate verifies that the Phase 27.85
family-conditioning objective is actually visible in the text streamed to
training, while remaining masked under assistant-only loss.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets import ChatDataset
from sf_ai.datasets.chat_dataset import FAMILY_CONDITION_LABELS, render_dialogue_text
from sf_ai.datasets.loaders import iter_chat_samples
from sf_ai.models.tokenizer import BPETokenizer
from sf_ai.training.train_tiny_lm import _encode_training_text, _iter_training_texts


DEFAULT_SOURCE = ROOT / "artifacts/reports/phase27_85_explicit_family_conditioning_objective_design_report.json"
DEFAULT_CORPUS = ROOT / "data/corpus/chat/jsonl"
DEFAULT_SPLIT = ROOT / "data/corpus/chat/splits/dialogue_split_v1.json"
DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v9_phase27_76"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_86_family_conditioning_renderer_gate_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_86_FAMILY_CONDITIONING_RENDERER_GATE_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_86_FAMILY_CONDITIONING_RENDERER_GATE_REPORT.md"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.86 renderer gate")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args()


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _first_sample(path: Path):  # type: ignore[no-untyped-def]
    for sample in iter_chat_samples(path):
        return sample
    raise ValueError(f"empty sample file: {path}")


def _family_sample_files(corpus: Path) -> dict[str, Path]:
    return {
        "open_social": corpus / "dialogue_batch_v10_balanced_open_social_saudi_010.jsonl",
        "followup": corpus / "dialogue_batch_v10_balanced_followup_saudi_010.jsonl",
        "planning": corpus / "dialogue_batch_v10_balanced_planning_saudi_010.jsonl",
        "support": corpus / "dialogue_batch_v10_balanced_support_saudi_010.jsonl",
        "topic": corpus / "dialogue_batch_v10_balanced_topic_saudi_010.jsonl",
    }


def _render_probes(corpus: Path) -> dict[str, dict[str, Any]]:
    probes: dict[str, dict[str, Any]] = {}
    for family, path in _family_sample_files(corpus).items():
        sample = _first_sample(path)
        text = render_dialogue_text(sample)
        expected = f"عائلة الحوار: {FAMILY_CONDITION_LABELS[family]}"
        probes[family] = {
            "file": _rel(path),
            "expected_family_line": expected,
            "rendered_preview": text,
            "has_dialect_line": "النطاق: سعودي" in text or "النطاق: فصحى" in text,
            "has_family_line": expected in text,
            "has_user_line": "المستخدم:" in text,
            "has_assistant_line": "المساعد:" in text,
        }
    return probes


def _stream_probe(corpus: Path, split_manifest: Path) -> dict[str, Any]:
    dataset = ChatDataset(corpus)
    no_split = next((t for t in dataset.iter_dialogue_texts() if "عائلة الحوار:" in t), "")
    split_train = next(
        (
            t
            for t in _iter_training_texts(
                dataset,
                stream_format="dialogue",
                split_manifest=split_manifest,
                split_name="train",
            )
            if "عائلة الحوار:" in t
        ),
        "",
    )
    return {
        "no_split_has_family_line": "عائلة الحوار:" in no_split,
        "split_train_has_family_line": "عائلة الحوار:" in split_train,
        "no_split_preview": no_split,
        "split_train_preview": split_train,
    }


def _mask_probe(tokenizer_path: Path) -> dict[str, Any]:
    tokenizer = BPETokenizer.load(tokenizer_path)
    text = (
        "النطاق: سعودي\n"
        "عائلة الحوار: تنظيم\n"
        "المستخدم: كيف أرتب يومي؟\n"
        "المساعد: ابدأ بثلاث مهام واضحة.\n"
    )
    ids, labels = _encode_training_text(
        tokenizer,
        text,
        stream_format="dialogue",
        loss_scope="assistant",
    )
    line_results: list[dict[str, Any]] = []
    offset = 0
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("المساعد:"):
            prefix = "المساعد:"
            content = line[len(prefix):].strip()
            prefix_ids = tokenizer.encode(prefix)
            content_ids = tokenizer.encode(content)
            prefix_labels = labels[offset:offset + len(prefix_ids)]
            offset += len(prefix_ids)
            content_labels = labels[offset:offset + len(content_ids)]
            offset += len(content_ids)
            eos_label = labels[offset] if offset < len(labels) else None
            if eos_label is not None:
                offset += 1
            line_results.append(
                {
                    "line": prefix,
                    "masked": all(label == -100 for label in prefix_labels),
                    "assistant_content_supervised": (
                        bool(content_labels)
                        and all(label != -100 for label in content_labels)
                    ),
                    "eos_supervised": eos_label is not None and eos_label != -100,
                }
            )
        else:
            line_ids = tokenizer.encode(line)
            line_labels = labels[offset:offset + len(line_ids)]
            offset += len(line_ids)
            line_results.append(
                {
                    "line": line,
                    "masked": bool(line_labels) and all(label == -100 for label in line_labels),
                    "assistant_content_supervised": False,
                }
            )
    return {
        "tokenizer": _rel(tokenizer_path),
        "text": text,
        "total_tokens": len(ids),
        "masked_tokens": sum(1 for label in labels if label == -100),
        "supervised_tokens": sum(1 for label in labels if label != -100),
        "line_results": line_results,
        "conditioning_lines_masked": all(
            row["masked"]
            for row in line_results
            if row["line"].startswith("النطاق:") or row["line"].startswith("عائلة الحوار:")
        ),
        "user_line_masked": all(
            row["masked"] for row in line_results if row["line"].startswith("المستخدم:")
        ),
        "assistant_content_supervised": any(
            row["assistant_content_supervised"] for row in line_results
        ),
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    source = _load_json(args.source)
    if source["decision"]["engineering_decision"] != "ALLOW_PHASE27_86_RENDERER_GATE_IMPLEMENTATION_NO_TRAINING":
        raise ValueError("Phase 27.85 did not allow Phase 27.86 renderer gate")

    render_probes = _render_probes(args.corpus)
    stream_probe = _stream_probe(args.corpus, args.split_manifest)
    mask_probe = _mask_probe(args.tokenizer)
    family_labels_complete = set(FAMILY_CONDITION_LABELS) == {
        "open_social",
        "followup",
        "planning",
        "support",
        "topic",
    }
    all_rendered = all(
        row["has_dialect_line"]
        and row["has_family_line"]
        and row["has_user_line"]
        and row["has_assistant_line"]
        for row in render_probes.values()
    )
    gate_passed = (
        family_labels_complete
        and all_rendered
        and stream_probe["no_split_has_family_line"]
        and stream_probe["split_train_has_family_line"]
        and mask_probe["conditioning_lines_masked"]
        and mask_probe["user_line_masked"]
        and mask_probe["assistant_content_supervised"]
    )
    decision = {
        "decision_id": "PHASE27_86_FAMILY_CONDITIONING_RENDERER_GATE_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_87_BOUNDED_FAMILY_CONDITIONED_SF10M_REPAIR_TRAINING"
            if gate_passed
            else "BLOCK_TRAINING_FIX_RENDERER"
        ),
        "new_training_allowed": gate_passed,
        "runtime_release_allowed": False,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "why": (
            "الرندر الآن يضيف سطر عائلة الحوار العربي في مساري التدريب، "
            "وassistant-only loss يخفي سطور السياق عن الهدف."
        ),
        "next_phase": "Phase 27.87 — Bounded Family-conditioned SF-10M Repair Training",
    }
    return {
        "phase": "Phase 27.86",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_86_RENDERER_GATE_PASSED_TRAINING_ALLOWED_NEXT_NO_RUNTIME"
            if gate_passed
            else "PHASE27_86_RENDERER_GATE_FAILED_TRAINING_BLOCKED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "source_report": _rel(args.source),
        "corpus": _rel(args.corpus),
        "split_manifest": _rel(args.split_manifest),
        "family_labels": FAMILY_CONDITION_LABELS,
        "family_labels_complete": family_labels_complete,
        "render_probes": render_probes,
        "stream_probe": stream_probe,
        "assistant_loss_mask_probe": mask_probe,
        "gate_passed": gate_passed,
        "blocked_actions": [
            "runtime release",
            "UI generator release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
        ],
        "allowed_next_actions": [
            "bounded SF-10M repair training with family-conditioned rendered text",
            "fresh held-out family canary after training",
            "checkpoint selection by runtime-quality metrics, not loss alone",
        ],
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.86 — Family Conditioning Renderer Gate",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة gate فقط. لم يبدأ تدريب ولم يتغير runtime.",
        "",
        f"- status: `{report['status']}`",
        f"- gate passed: `{report['gate_passed']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- training allowed for next phase: `{decision['new_training_allowed']}`",
        f"- runtime release allowed: `{decision['runtime_release_allowed']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## Family Lines",
        "",
    ]
    for family, probe in report["render_probes"].items():
        lines.append(f"- `{family}` → `{probe['expected_family_line']}`")
    lines.extend(
        [
            "",
            "## Masking",
            "",
            "- conditioning lines masked: "
            f"`{report['assistant_loss_mask_probe']['conditioning_lines_masked']}`",
            "- user line masked: "
            f"`{report['assistant_loss_mask_probe']['user_line_masked']}`",
            "- assistant content supervised: "
            f"`{report['assistant_loss_mask_probe']['assistant_content_supervised']}`",
            "",
            "## القرار",
            "",
            decision["why"],
            "",
            "لا يوجد runtime release من هذه المرحلة؛ المسموح فقط تدريب مقيّد في Phase 27.87.",
            "",
        ]
    )
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
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.write_text(
        json.dumps(report["decision"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_doc(args.doc, report)

    print("SF.AI — Phase 27.86 family conditioning renderer gate")
    print(f"status: {report['status']}")
    print(f"gate_passed: {report['gate_passed']}")
    print(f"decision: {report['decision']['engineering_decision']}")
    print(f"next: {report['decision']['next_phase']}")
    print(f"report: {_rel(args.report)}")
    return 0 if report["gate_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
