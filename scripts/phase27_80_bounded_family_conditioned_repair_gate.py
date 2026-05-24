#!/usr/bin/env python3
"""Phase 27.80 — bounded SF-10M family-conditioned repair gate.

No LM training happens here. This gate verifies that the new SF-native
Objective/Curriculum/Decoding Acceleration Track is executable before the
bounded training run is allowed.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets.chat_dataset import render_dialogue_text  # noqa: E402
from sf_ai.datasets.schemas import StructuredSample  # noqa: E402
from sf_ai.datasets.splits import (  # noqa: E402
    FAMILY_ORDER,
    iter_split_samples_round_robin_by_family,
)
from sf_ai.models.transformer.generation import GenerationConfig  # noqa: E402
from sf_ai.training.device import DeviceManager  # noqa: E402
from sf_ai.training.train_tiny_lm import (  # noqa: E402
    _encode_training_text,
    load_sovereign_tokenizer,
)

DEFAULT_PLAN = ROOT / "artifacts/reports/PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN.json"
DEFAULT_CORPUS = ROOT / "data/corpus/chat/jsonl"
DEFAULT_SPLIT = ROOT / "data/corpus/chat/splits/dialogue_split_v1.json"
DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v9_phase27_76"
DEFAULT_OUT_DIR = ROOT / "artifacts/eval/phase27_80_family_conditioned_gate"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_80_bounded_family_conditioned_repair_gate_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_80_BOUNDED_FAMILY_CONDITIONED_REPAIR_GATE_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_80_BOUNDED_FAMILY_CONDITIONED_REPAIR_GATE_REPORT.md"

WINDOW_SIZE = 500


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.80 bounded repair gates")
    p.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--split", type=Path, default=DEFAULT_SPLIT)
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def load_plan(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"missing plan: {path}")
    plan = json.loads(path.read_text(encoding="utf-8"))
    if plan.get("report_id") != "PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN":
        raise ValueError("Phase 27.80 requires PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN")
    if plan.get("decision", {}).get("new_training_allowed") is not False:
        raise ValueError("Phase 27.80 gate requires the plan to block training first")
    return plan


def validate_objective_renderer(tokenizer_path: Path) -> dict[str, Any]:
    sample = StructuredSample(
        domain="chat",
        lang="ar",
        messages=[
            {"role": "user", "content": "كيف أنظم يومي؟"},
            {"role": "assistant", "content": "اكتب ثلاث مهام، وابدأ بالأهم لمدة قصيرة."},
        ],
        provenance={
            "dialect": "saudi",
            "dialogue_family": "planning",
            "source": "phase27_80_gate_probe",
            "license": "owner-authored",
            "training_allowed": True,
            "quality": "gold",
        },
    )
    rendered = render_dialogue_text(sample)
    required_lines = [
        "النطاق: سعودي",
        "عائلة الحوار: تنظيم",
        "المستخدم: كيف أنظم يومي؟",
        "المساعد: اكتب ثلاث مهام، وابدأ بالأهم لمدة قصيرة. <eos>",
    ]
    line_pass = all(line in rendered for line in required_lines)
    tokenizer = load_sovereign_tokenizer(tokenizer_path)
    ids, labels = _encode_training_text(
        tokenizer,
        rendered,
        stream_format="dialogue",
        loss_scope="assistant",
    )
    non_masked = sum(1 for label in labels if label != -100)
    context_masked = True
    assistant_seen = False
    for raw_line in rendered.splitlines():
        line_ids = tokenizer.encode(raw_line)
        line_labels = labels[: len(line_ids)]
        labels = labels[len(line_ids) :]
        if raw_line.startswith("المساعد:"):
            assistant_seen = any(label != -100 for label in line_labels)
        elif any(label != -100 for label in line_labels):
            context_masked = False
    passed = line_pass and context_masked and assistant_seen and non_masked > 0
    return {
        "gate": "objective_renderer_assistant_loss_mask",
        "passed": passed,
        "rendered_preview": rendered,
        "required_lines_present": line_pass,
        "context_masked": context_masked,
        "assistant_supervised": assistant_seen,
        "non_masked_label_count": non_masked,
    }


def _family(sample: Any) -> str:
    provenance = getattr(sample, "provenance", None)
    for attr in ("dialogue_family", "answer_family", "prompt_family"):
        value = (getattr(provenance, attr, "") or "").strip().lower()
        if value in FAMILY_ORDER:
            return value
    return "unknown"


def validate_round_robin(corpus: Path, split: Path, out_dir: Path) -> dict[str, Any]:
    samples = []
    for sample in iter_split_samples_round_robin_by_family(
        corpus,
        split,
        split_name="train",
    ):
        family = _family(sample)
        if family in FAMILY_ORDER:
            samples.append((family, sample))
        if len(samples) >= WINDOW_SIZE:
            break
    counts = Counter(f for f, _ in samples)
    shares = {family: counts[family] / max(1, len(samples)) for family in FAMILY_ORDER}
    missing = [family for family in FAMILY_ORDER if counts[family] == 0]
    max_share = max(shares.values()) if shares else 0.0
    min_share = min(shares.values()) if shares else 0.0
    passed = len(samples) == WINDOW_SIZE and not missing and min_share >= 0.16 and max_share <= 0.24

    out_dir.mkdir(parents=True, exist_ok=True)
    preview = out_dir / "round_robin_window_preview.json"
    preview.write_text(
        json.dumps(
            {
                "window_size": len(samples),
                "family_counts": dict(counts),
                "family_shares": shares,
                "first_25_families": [family for family, _sample in samples[:25]],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "gate": "stratified_round_robin_window_balance",
        "passed": passed,
        "window_size": len(samples),
        "family_counts": {family: counts[family] for family in FAMILY_ORDER},
        "family_shares": {k: round(v, 4) for k, v in shares.items()},
        "missing_families": missing,
        "preview": rel(preview),
    }


def write_policy_artifacts(out_dir: Path) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    decoding = {
        "name": "guarded_decoding_policy_v2",
        "stop_at_eos": True,
        "no_repeat_ngram_size": 3,
        "repetition_penalty": 1.08,
        "known_fragment_blocklist": ["المعنى: المعنى", "وأين يستخدم؟ يستخدم؟"],
        "topic_substitution_guard": True,
        "family_drift_guard": True,
        "template_masking_forbidden": True,
        "blocked_response_rule": "return generator_blocked metadata, not fixed template",
    }
    decoding_path = out_dir / "decoding_policy_v2.json"
    decoding_path.write_text(json.dumps(decoding, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    config = GenerationConfig(
        max_new_tokens=64,
        temperature=0.8,
        top_k=40,
        eos_token_id=0,
        no_repeat_ngram_size=decoding["no_repeat_ngram_size"],
        repetition_penalty=decoding["repetition_penalty"],
    )
    decoding_passed = (
        config.no_repeat_ngram_size == 3
        and config.repetition_penalty > 1.0
        and decoding["stop_at_eos"]
        and decoding["template_masking_forbidden"]
    )

    selector = {
        "name": "contrastive_checkpoint_selector_v2",
        "required_suites": [
            "known_canary",
            "fresh_heldout_canary",
            "family_confusion_matrix",
            "topic_binding_canary",
            "open_social_canary",
            "followup_canary",
            "clean_stop_canary",
            "runtime_dry_run",
        ],
        "selection_metrics": [
            "held_out_dialogue_quality",
            "family_stability",
            "semantic_correctness",
            "clean_stop",
            "open_social_naturalness",
            "followup_continuity",
            "runtime_usability",
        ],
        "loss_only_is_never_enough": True,
    }
    selector_path = out_dir / "checkpoint_selector_v2.json"
    selector_path.write_text(json.dumps(selector, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    logging = {
        "backend": "csv",
        "local_only": True,
        "fields": [
            "step",
            "train_loss",
            "eval_loss",
            "perplexity",
            "family_accuracy",
            "clean_stop_rate",
            "topic_binding_pass_rate",
            "canary_pass_rate",
            "blocked_reason",
            "checkpoint_decision",
        ],
    }
    logging_path = out_dir / "local_csv_logging_schema.json"
    logging_path.write_text(json.dumps(logging, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    csv_path = out_dir / "metrics_template.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=logging["fields"])
        writer.writeheader()

    return {
        "gate": "decoding_eval_selector_logging_artifacts",
        "passed": decoding_passed,
        "decoding_policy": rel(decoding_path),
        "checkpoint_selector": rel(selector_path),
        "logging_schema": rel(logging_path),
        "metrics_template": rel(csv_path),
    }


def validate_canaries() -> dict[str, Any]:
    required = [
        ROOT / "artifacts/reports/phase27_30_fresh_mixed_shadow_canary_report.json",
        ROOT / "artifacts/reports/phase27_60_broader_natural_dialogue_canary_report.json",
        ROOT / "artifacts/reports/phase27_102_topic_prototype_contrastive_gate_report.json",
        ROOT / "artifacts/reports/phase27_dialogue_eval_v2_report.json",
    ]
    present = [rel(path) for path in required if path.exists()]
    return {
        "gate": "heldout_contrastive_canary_inventory",
        "passed": len(present) == len(required),
        "present": present,
        "missing": [rel(path) for path in required if not path.exists()],
    }


def smoke_mps_amp() -> dict[str, Any]:
    device = DeviceManager("auto").select()
    result: dict[str, Any] = {
        "gate": "mps_amp_smoke",
        "selected_device": device.name,
        "device_notes": device.notes,
        "mps_checked": True,
        "amp_enabled_for_training": False,
    }
    try:
        import torch

        mps_available = bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available())
        result["mps_available"] = mps_available
        if mps_available:
            x = torch.ones((2, 2), device="mps")
            y = x @ x
            result["mps_smoke_value"] = float(y[0, 0].detach().cpu())
            result["amp_smoke_status"] = "not_enabled_until_training_smoke"
        else:
            result["amp_smoke_status"] = "mps_unavailable_cpu_fallback"
        result["passed"] = True
    except Exception as exc:  # pragma: no cover - hardware dependent
        result["passed"] = False
        result["error"] = str(exc)
    return result


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    plan = load_plan(args.plan)
    gates = [
        validate_objective_renderer(args.tokenizer),
        validate_round_robin(args.corpus, args.split, args.out_dir),
        write_policy_artifacts(args.out_dir),
        validate_canaries(),
        smoke_mps_amp(),
    ]
    passed = all(g["passed"] for g in gates)
    decision = {
        "decision_id": "PHASE27_80_BOUNDED_FAMILY_CONDITIONED_REPAIR_GATE_DECISION",
        "engineering_decision": (
            "GATES_PASSED_BOUNDED_TRAINING_CAN_BE_SCHEDULED"
            if passed
            else "GATES_FAILED_TRAINING_BLOCKED"
        ),
        "all_gates_passed": passed,
        "new_training_started": False,
        "bounded_training_allowed_next": passed,
        "runtime_release_allowed": False,
        "sf50m_allowed": False,
        "tokenizer_retrain_allowed": False,
        "next_phase": (
            "Phase 27.81 — Execute bounded SF-10M family-conditioned repair training"
            if passed
            else "Phase 27.80 remediation — fix failed gates"
        ),
    }
    return {
        "phase": "Phase 27.80",
        "phase_title": "Bounded SF-10M Family-Conditioned Repair Gate",
        "active_track": plan["active_track"],
        "strategy": plan["strategy"],
        "source_plan": rel(args.plan),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "runtime_changed": False,
        "gates": gates,
        "blocked_actions": [
            "runtime release",
            "SF-50M transition",
            "tokenizer retrain",
            "pretrained/open-weight usage",
            "template masking",
        ],
        "decision": decision,
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Phase 27.80 — Bounded SF-10M Family-Conditioned Repair Gate",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة بوابة تنفيذية فقط. لم يبدأ تدريب جديد ولم يتغير runtime.",
        "",
        f"- decision: `{report['decision']['engineering_decision']}`",
        f"- all gates passed: `{report['decision']['all_gates_passed']}`",
        f"- next: `{report['decision']['next_phase']}`",
        "",
        "## Gates",
        "",
    ]
    for gate in report["gates"]:
        lines.append(f"- `{gate['gate']}`: `{gate['passed']}`")
    lines.extend(["", "## Blocked Actions", ""])
    for item in report["blocked_actions"]:
        lines.append(f"- {item}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        report = build_report(args)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.decision.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.decision.write_text(
        json.dumps(report["decision"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_doc(args.doc, report)
    print("SF.AI — Phase 27.80 bounded family-conditioned repair gate")
    print(f"all_gates_passed: {report['decision']['all_gates_passed']}")
    print(f"decision: {report['decision']['engineering_decision']}")
    print(f"next: {report['decision']['next_phase']}")
    print(f"report: {rel(args.report)}")
    return 0 if report["decision"]["all_gates_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
