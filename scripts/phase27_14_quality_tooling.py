#!/usr/bin/env python
"""Phase 27.14 — adopt sovereign training quality tooling.

This script does not train, crawl, or enable runtime generation. It turns the
tooling decision into local artifacts:

- a JSON decision report,
- a JSONL experiment registry seeded from Phase 27.12 and 27.13 reports.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sf_ai.training.experiment_tracker import (
    LocalExperimentTracker,
    phase27_12_record,
    phase27_13_record,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_14_quality_tooling_decision_report.json"
DEFAULT_REGISTRY = ROOT / "artifacts/reports/experiment_registry.jsonl"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase 27.14 sovereign quality tooling decision")
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    return p.parse_args()


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_report(*, registry_path: Path) -> dict[str, Any]:
    p2712 = _load(ROOT / "artifacts/reports/phase27_12_eos_probe_report.json")
    p2713 = _load(ROOT / "artifacts/reports/sf_10m_v0_8_boundary_eos_training_report.json")

    records = [phase27_12_record(p2712), phase27_13_record(p2713)]
    LocalExperimentTracker(registry_path).write_all(records)

    return {
        "phase": "Phase 27.14",
        "name": "Sovereign Training Quality Tooling Decision",
        "status": "completed_tooling_adoption_decision_no_training",
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_generator_enabled": False,
        "uses_external_ai": False,
        "uses_pretrained": False,
        "decision": (
            "Adopt the full sovereign quality tooling layer. Implemented items "
            "remain mandatory gates before runtime activation or SF-50M scaling."
        ),
        "tools": [
            {
                "tool": "assistant_eos_stop_boundary",
                "decision": "adopted",
                "status": "implemented_phase27_12",
                "evidence": "assistant <eos> target and EOS-aware generation are active in training/generation code.",
                "next_action": "keep mandatory in every assistant-target run",
            },
            {
                "tool": "sequence_packing_with_boundaries",
                "decision": "adopted",
                "status": "implemented_dialogue_stream",
                "evidence": "dialogue stream keeps user/assistant markers and dialect conditioning before samples.",
                "next_action": "audit packed examples before each training run",
            },
            {
                "tool": "local_experiment_tracker",
                "decision": "adopted",
                "status": "implemented_phase27_14",
                "evidence": str(registry_path),
                "next_action": "append every future training/eval/generation gate result",
            },
            {
                "tool": "data_quality_scanner",
                "decision": "adopted",
                "status": "partially_implemented_existing_corpus_audit",
                "evidence": "corpus-audit and operational-dialogue filter exist; Phase 27.15 should add semantic short-reply scanner.",
                "next_action": "scan weak social replies and malformed lexical targets before next training",
            },
            {
                "tool": "curriculum_sampler",
                "decision": "adopted",
                "status": "planned_phase27_15",
                "evidence": "v0.8 fails greetings/thanks/Saudi preference despite lower eval loss.",
                "next_action": "train from social micro-skills to short explanations before mixed corpus",
            },
            {
                "tool": "no_repeat_decoding_controls",
                "decision": "adopted",
                "status": "planned_generation_decoder",
                "evidence": "GenerationGuard catches repetition; decoder should prevent it earlier.",
                "next_action": "add deterministic no-repeat ngram and repetition penalty tests",
            },
            {
                "tool": "gold_micro_probes",
                "decision": "adopted",
                "status": "implemented_phase27_11_27_12",
                "evidence": "Phase 27.11 exposed missing clean-stop; Phase 27.12 measured EOS improvement.",
                "next_action": "expand probe to 32/64 social replies after curriculum repair",
            },
            {
                "tool": "checkpoint_selector",
                "decision": "adopted",
                "status": "implemented_phase27_13",
                "evidence": "v0.8 selected step6000 by held-out eval, then blocked by generation-quality.",
                "next_action": "select by eval + clean-stop + generation-quality, never by latest checkpoint only",
            },
            {
                "tool": "local_logs",
                "decision": "adopted",
                "status": "implemented_json_reports_and_registry",
                "evidence": "artifacts/reports/*.json plus experiment_registry.jsonl",
                "next_action": "keep local-only; no cloud tracker",
            },
            {
                "tool": "tokenizer_boundary_audit",
                "decision": "adopted",
                "status": "implemented_policy_audit_plus_required_future_check",
                "evidence": "tokenization-audit exists; boundary terms must be checked before tokenizer retrains.",
                "next_action": "add explicit protected boundary audit if tokenizer v3 starts",
            },
        ],
        "blocking_policy": {
            "activate_runtime_generator": "blocked_until_generation_quality_passes_all_required_social_and_fragment_gates",
            "start_sf50m": "blocked_until_sf10m_runtime_quality_passes_scaling_gates",
            "start_phase28": "blocked_until_sf50m_exists_and_passes_quality_gates",
        },
        "experiment_registry": str(registry_path),
        "seeded_experiments": [record.to_json() for record in records],
        "next": "Phase 27.15 — targeted social/lexical curriculum and decoder no-repeat controls for SF-10M.",
    }


def main() -> int:
    args = parse_args()
    report = build_report(registry_path=args.registry)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("SF.AI — Phase 27.14 quality tooling decision")
    print(f"  status          : {report['status']}")
    print(f"  tools adopted   : {len(report['tools'])}")
    print(f"  training_started: {str(report['training_started']).lower()}")
    print(f"  runtime_enabled : {str(report['runtime_generator_enabled']).lower()}")
    print(f"  registry        : {args.registry}")
    print(f"  report          : {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
