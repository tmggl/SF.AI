#!/usr/bin/env python3
"""Phase 27.22 spacing/boundary repair.

Read-only evaluation over the Phase 27.21 tokenizer-v3 micro-probe checkpoint.
This phase fixes decoder/guard boundary behavior, then re-evaluates the same
checkpoint to measure whether spacing artifacts were caused by decoding rather
than the model alone.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import _evaluate  # noqa: E402
from scripts.phase27_19_hygiene_repair_probe import _records  # noqa: E402


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v3"
DEFAULT_CHECKPOINTS = ROOT / "artifacts/eval/phase27_21_tokenizer_v3_micro_probe/checkpoints"
DEFAULT_CHECKPOINT = "sf-10m-step3200"
DEFAULT_PREVIOUS_REPORT = ROOT / "artifacts/reports/phase27_21_tokenizer_v3_micro_probe_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_22_spacing_boundary_repair_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_22_spacing_boundary_repair_generations.md"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.22 spacing/boundary repair eval")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--checkpoints", type=Path, default=DEFAULT_CHECKPOINTS)
    p.add_argument("--checkpoint-name", default=DEFAULT_CHECKPOINT)
    p.add_argument("--previous-report", type=Path, default=DEFAULT_PREVIOUS_REPORT)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--device", default="auto")
    return p.parse_args()


def _load_previous(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_samples_phase27_22(path: Path, results: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.22 Spacing/Boundary Repair Generations", ""]
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
    if not (args.tokenizer / "meta.json").exists():
        print(f"error: missing tokenizer at {args.tokenizer}", file=sys.stderr)
        return 1
    ckpt_dir = args.checkpoints / args.checkpoint_name
    if not (ckpt_dir / "state.pt").exists():
        print(f"error: missing checkpoint at {ckpt_dir}", file=sys.stderr)
        return 1

    _, eval_records = _records()
    previous = _load_previous(args.previous_report)
    results, reasons = _evaluate(
        records=eval_records,
        checkpoints_root=args.checkpoints,
        checkpoint_name=args.checkpoint_name,
        device=args.device,
        tokenizer_path=args.tokenizer,
    )

    total = len(results)
    passed = sum(1 for item in results if item["passed"])
    exact = sum(1 for item in results if item["exact_clean"])
    semantic = sum(1 for item in results if item["semantic_match"])
    guard = sum(1 for item in results if item["guard_reason"] == "passed")
    previous_passed = int(previous.get("passed", 0) or 0)
    previous_exact = int(previous.get("exact_clean", 0) or 0)
    previous_semantic = int(previous.get("semantic_match", 0) or 0)
    previous_guard = int(previous.get("guard_passed", 0) or 0)

    glued_markers = ("سواونخفف", "تفيدوتوسع", "هادئًاوابدأ")
    glued_remaining = [
        {
            "id": item["id"],
            "generated": item["generated"],
        }
        for item in results
        if any(marker in item["generated"] for marker in glued_markers)
    ]

    status = (
        "PASSED_SPACING_BOUNDARY_REPAIR_HOLD_RUNTIME_FOR_CANARY"
        if passed == total and not glued_remaining
        else "PARTIAL_SPACING_BOUNDARY_REPAIR_BLOCK_RUNTIME"
    )

    report = {
        "phase": "Phase 27.22",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "tokenizer": str(args.tokenizer.relative_to(ROOT)),
        "checkpoint_root": str(args.checkpoints.relative_to(ROOT)),
        "checkpoint_name": args.checkpoint_name,
        "repair_actions": [
            "BPETokenizer.decode inserts a word boundary after protected phrase tokens.",
            "GenerationGuard no longer blocks valid tanween word ending 'تًا' globally.",
        ],
        "previous_phase27_21": {
            "passed": previous_passed,
            "exact_clean": previous_exact,
            "semantic_match": previous_semantic,
            "guard_passed": previous_guard,
        },
        "current": {
            "passed": passed,
            "failed": total - passed,
            "eval_records": total,
            "pass_rate": round(passed / total, 4) if total else 0.0,
            "exact_clean": exact,
            "semantic_match": semantic,
            "guard_passed": guard,
            "reason_counts": dict(Counter(reasons)),
        },
        "delta": {
            "passed": passed - previous_passed,
            "exact_clean": exact - previous_exact,
            "semantic_match": semantic - previous_semantic,
            "guard_passed": guard - previous_guard,
        },
        "glued_spacing_markers_checked": list(glued_markers),
        "glued_spacing_markers_remaining": glued_remaining,
        "runtime_allowed": False,
        "sf50m_allowed": False,
        "decision": (
            "Spacing repair fully passed the micro-probe; keep runtime blocked until broader canary."
            if status == "PASSED_SPACING_BOUNDARY_REPAIR_HOLD_RUNTIME_FOR_CANARY"
            else "Spacing repair improved decoding but did not fully pass; keep runtime and SF-50M blocked."
        ),
        "next_phase": (
            "Phase 27.23 — broader generation-quality canary"
            if status == "PASSED_SPACING_BOUNDARY_REPAIR_HOLD_RUNTIME_FOR_CANARY"
            else "Phase 27.23 — semantic/lexical confusion repair"
        ),
        "results": results,
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples_phase27_22(args.samples, results)

    print("SF.AI — Phase 27.22 spacing/boundary repair")
    print(f"  status        : {status}")
    print(f"  checkpoint    : {args.checkpoint_name}")
    print(f"  passed        : {passed}/{total} (delta {passed - previous_passed:+d})")
    print(f"  exact_clean   : {exact}/{total} (delta {exact - previous_exact:+d})")
    print(f"  semantic      : {semantic}/{total} (delta {semantic - previous_semantic:+d})")
    print(f"  guard_passed  : {guard}/{total} (delta {guard - previous_guard:+d})")
    print(f"  glued_left    : {len(glued_remaining)}")
    print(f"  reasons       : {dict(reasons)}")
    print(f"  runtime       : blocked")
    print(f"  report        : {args.report}")
    print(f"  samples       : {args.samples}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
