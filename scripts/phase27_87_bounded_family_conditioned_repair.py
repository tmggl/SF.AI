#!/usr/bin/env python3
"""Phase 27.87 — evaluate bounded family-conditioned SF-10M repair training.

Training is run separately via the command recorded in this phase. This script
evaluates the produced checkpoints with the same Arabic family-conditioning
line used during training. No runtime release happens here.
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

from scripts.phase27_58_tokenizer_bounded_alignment_probe import _expected_ok, _family_terms, _surface
from scripts.phase27_60_broader_natural_dialogue_canary import _FORBIDDEN_BY_FAMILY
from scripts.phase27_67_fresh_shadow_canary import FRESH_SHADOW_CASES
from sf_ai.modules.chat.generation_guard import GenerationGuard
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig


DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v9_phase27_76"
DEFAULT_CHECKPOINTS = ROOT / "artifacts/eval/phase27_87_family_conditioned_renderer_repair/checkpoints"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_87_bounded_family_conditioned_repair_report.json"
DEFAULT_DECISION = ROOT / "artifacts/reports/PHASE27_87_BOUNDED_FAMILY_CONDITIONED_REPAIR_DECISION.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_87_BOUNDED_FAMILY_CONDITIONED_REPAIR_REPORT.md"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_87_bounded_family_conditioned_repair.md"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Evaluate Phase 27.87 checkpoints")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--checkpoints", type=Path, default=DEFAULT_CHECKPOINTS)
    p.add_argument("--device", default="auto")
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
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


def _family_ok(text: str, family: str, families: dict[str, tuple[str, ...]]) -> bool:
    surface = _surface(text)
    allowed = any(_surface(term) in surface for term in families.get(family, ()))
    forbidden = any(_surface(term) in surface for term in _FORBIDDEN_BY_FAMILY.get(family, ()))
    return allowed and not forbidden


def _checkpoint_meta(root: Path, checkpoint: str) -> dict[str, Any]:
    meta_path = root / checkpoint / "meta.json"
    meta = _load_json(meta_path)
    return {
        "checkpoint": checkpoint,
        "path": _rel(root / checkpoint),
        "state_exists": (root / checkpoint / "state.pt").exists(),
        "sf_origin": meta.get("sf_origin") is True,
        "step": meta.get("step"),
        "model_name": meta.get("model_name"),
        "notes": meta.get("notes", ""),
    }


def _evaluate_checkpoint(args: argparse.Namespace, checkpoint: str) -> dict[str, Any]:
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=args.tokenizer,
            checkpoints_root=args.checkpoints,
            checkpoint_name=checkpoint,
            generator_name=f"sf_10m_phase27_87_{checkpoint}",
            model_size="sf-10m",
            seq_len=96,
            max_new_tokens=28,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.12,
            device=args.device,
            dialogue_prompt=True,
            family_conditioning=True,
        )
    )
    guard = GenerationGuard(min_chars=4)
    families = _family_terms()
    rows: list[dict[str, Any]] = []
    for case in FRESH_SHADOW_CASES:
        out = generator.generate(
            case.prompt,
            dialect=case.dialect,
            intent=case.intent,
            topic=case.topic,
            max_new_tokens=28,
            temperature=1.0,
            top_k=0,
        )
        verdict = (
            guard.inspect(out.text)
            if case.family == "topic"
            else guard.inspect_for_prompt(case.prompt, out.text)
        )
        expected = _expected_ok(out.text, case.expected_any)
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
                "expected_any": list(case.expected_any),
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
    return {"checkpoint": checkpoint, "meta": _checkpoint_meta(args.checkpoints, checkpoint), "rows": rows, "summary": _summary(rows)}


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    families = sorted({str(row["family"]) for row in rows})
    passed = sum(1 for row in rows if row["passed"])
    return {
        "passed": passed,
        "total": len(rows),
        "pass_rate": round(passed / len(rows), 4) if rows else 0.0,
        "family_summary": {
            family: {
                "passed": sum(1 for row in rows if row["family"] == family and row["passed"]),
                "total": sum(1 for row in rows if row["family"] == family),
            }
            for family in families
        },
        "reason_counts": dict(Counter(str(row["reason"]) for row in rows)),
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    checkpoints = ("sf-10m-step600", "sf-10m-step1200", "sf-10m-step1800")
    evaluated = [_evaluate_checkpoint(args, checkpoint) for checkpoint in checkpoints]
    best = max(evaluated, key=lambda row: row["summary"]["passed"])
    all_state_ok = all(row["meta"]["state_exists"] and row["meta"]["sf_origin"] for row in evaluated)
    passed = int(best["summary"]["passed"])
    total = int(best["summary"]["total"])
    runtime_threshold = max(1, int(total * 0.9))
    runtime_release_allowed = bool(all_state_ok and passed >= runtime_threshold)
    decision = {
        "decision_id": "PHASE27_87_BOUNDED_FAMILY_CONDITIONED_REPAIR_DECISION",
        "engineering_decision": (
            "ALLOW_HELDOUT_RUNTIME_RELEASE_GATE"
            if runtime_release_allowed
            else "BLOCK_RUNTIME_DIAGNOSE_FAMILY_CONDITIONED_TRAINING_RESULT"
        ),
        "training_completed": True,
        "runtime_release_allowed": runtime_release_allowed,
        "ui_release_allowed": False,
        "sf50m_justified_transition": False,
        "tokenizer_retrain_allowed": False,
        "best_checkpoint_by_fresh_shadow": best["checkpoint"],
        "best_fresh_shadow_passed": passed,
        "best_fresh_shadow_total": total,
        "runtime_threshold": runtime_threshold,
        "why": (
            f"Best checkpoint reached {passed}/{total} fresh-shadow passes "
            "with explicit family conditioning."
        ),
        "next_phase": (
            "Phase 27.88 — Held-out Runtime Release Gate"
            if runtime_release_allowed
            else "Phase 27.88 — Family-conditioned Training Result Diagnosis"
        ),
    }
    return {
        "phase": "Phase 27.87",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "status": (
            "PHASE27_87_TRAINED_HELDOUT_RUNTIME_GATE_ALLOWED"
            if runtime_release_allowed
            else "PHASE27_87_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED"
        ),
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_completed": True,
        "runtime_changed": False,
        "training_scope": "bounded SF-10M repair training after Phase 27.86 renderer gate",
        "tokenizer": _rel(args.tokenizer),
        "init_checkpoint": "artifacts/eval/phase27_77_v9_bounded_open_social_lm_repair/checkpoints/sf-10m-step6200",
        "checkpoint_root": _rel(args.checkpoints),
        "family_conditioning_runtime_eval": True,
        "checkpoints": evaluated,
        "decision": decision,
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    decision = report["decision"]
    lines = [
        "# Phase 27.87 — Bounded Family-conditioned SF-10M Repair Training",
        "",
        "## الخلاصة",
        "",
        "اكتمل التدريب المقيّد بعد إصلاح renderer. لا يوجد runtime release من هذه المرحلة.",
        "",
        f"- status: `{report['status']}`",
        f"- decision: `{decision['engineering_decision']}`",
        f"- runtime release: `{decision['runtime_release_allowed']}`",
        f"- best checkpoint: `{decision['best_checkpoint_by_fresh_shadow']}`",
        f"- best fresh shadow: `{decision['best_fresh_shadow_passed']}/{decision['best_fresh_shadow_total']}`",
        f"- runtime threshold: `{decision['runtime_threshold']}/{decision['best_fresh_shadow_total']}`",
        f"- next: `{decision['next_phase']}`",
        "",
        "## Checkpoints",
        "",
    ]
    for row in report["checkpoints"]:
        summary = row["summary"]
        lines.extend(
            [
                f"### {row['checkpoint']}",
                "",
                f"- fresh shadow: `{summary['passed']}/{summary['total']}`",
                f"- family summary: `{summary['family_summary']}`",
                f"- reason counts: `{summary['reason_counts']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## القرار",
            "",
            "- لا تفعيل للواجهة من هذه المرحلة.",
            "- لا SF-50M.",
            "- لا tokenizer retrain.",
            "- أي انتقال لاحق يعتمد على تقرير التشخيص أو بوابة held-out إذا تجاوزت النتيجة الحد.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_samples(path: Path, report: dict[str, Any]) -> None:
    lines = ["# Phase 27.87 Samples", ""]
    for checkpoint in report["checkpoints"]:
        lines.extend([f"## {checkpoint['checkpoint']}", ""])
        for row in checkpoint["rows"][:20]:
            lines.extend(
                [
                    f"### {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                    "",
                    f"- family: {row['family']}",
                    f"- prompt: {row['prompt']}",
                    f"- response: {row['response']}",
                    f"- reason: {row['reason']}",
                    "",
                ]
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        report = build_report(args)
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as exc:
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
    _write_samples(args.samples, report)

    decision = report["decision"]
    print("SF.AI — Phase 27.87 bounded family-conditioned repair")
    print(f"status: {report['status']}")
    print(f"decision: {decision['engineering_decision']}")
    print(f"best: {decision['best_checkpoint_by_fresh_shadow']} ({decision['best_fresh_shadow_passed']}/{decision['best_fresh_shadow_total']})")
    print(f"next: {decision['next_phase']}")
    print(f"report: {_rel(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
