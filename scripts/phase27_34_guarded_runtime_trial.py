#!/usr/bin/env python3
"""Phase 27.34 guarded runtime trial smoke.

This does not train. It exercises the same ChatModule policy that `/chat/message`
uses when `generator_trial=true`:

* eligible non-sensitive chat prompts should use `sf_10m_phase27_33`;
* pinned identity/capability/project prompts should stay template-first;
* sensitive domains should stay on the composer/template path.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_17_prompt_answer_micro_probe import _semantic_match  # noqa: E402
from sf_ai.core.index import load_default_registry  # noqa: E402
from sf_ai.core.orchestrator import Orchestrator, UserMessage  # noqa: E402
from sf_ai.modules.chat import ChatModule, GenerationPolicy  # noqa: E402


DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_34_guarded_runtime_trial_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_34_guarded_runtime_trial_generations.md"


@dataclass(frozen=True)
class TrialPrompt:
    id: str
    message: str
    expected_generator: str
    expected_terms: tuple[str, ...]
    note: str


TRIAL_PROMPTS: tuple[TrialPrompt, ...] = (
    TrialPrompt("trial_001", "كيفك اليوم", "sf_10m_phase27_33", ("بخير", "كيفك"), "smalltalk generator"),
    TrialPrompt("trial_002", "شكرًا لمساعدتك", "sf_10m_phase27_33", ("العفو", "أساعدك"), "thanks generator"),
    TrialPrompt("trial_003", "وجهني بخطوة بسيطة", "sf_10m_phase27_33", ("ابدأ", "خطوة"), "advice generator"),
    TrialPrompt("trial_004", "رتب لي يومي بسرعة", "sf_10m_phase27_33", ("ثلاث",), "planning generator"),
    TrialPrompt("trial_005", "توترت شوي وش اسوي", "sf_10m_phase27_33", ("يهونها", "اهدأ"), "support generator"),
    TrialPrompt("trial_006", "وش المقصود بالاحترام", "sf_10m_phase27_33", ("تقدّر", "تصرفك"), "definition generator"),
    TrialPrompt("trial_007", "القراية تفيدني بشي", "sf_10m_phase27_33", ("فهمك", "كلماتك"), "definition generator"),
    TrialPrompt("control_001", "من أنت", "template", ("SF.AI",), "pinned identity remains template"),
    TrialPrompt("control_002", "عندي ألم في الراس", "template", ("طبيب",), "sensitive medical remains composer"),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.34 guarded runtime trial smoke")
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    return p.parse_args()


def _trial_orchestrator() -> Orchestrator:
    policy = GenerationPolicy(
        enabled=True,
        experimental_runtime=True,
        canary=True,
        guarded_runtime_trial=True,
        min_confidence=0.0,
        max_new_tokens=24,
        temperature=1.0,
        top_k=0,
    )
    return Orchestrator(
        registry=load_default_registry(),
        modules={"chat": ChatModule(generation_policy=policy)},
    )


def _run() -> list[dict[str, Any]]:
    orch = _trial_orchestrator()
    rows: list[dict[str, Any]] = []
    for item in TRIAL_PROMPTS:
        result = orch.process(UserMessage(text=item.message, session_id=f"phase27-34-{item.id}"))
        generator = result.debug.get("generator", "template")
        semantic = _semantic_match(result.response, item.expected_terms)
        passed = generator == item.expected_generator and semantic
        rows.append(
            {
                "id": item.id,
                "message": item.message,
                "domain": result.domain,
                "intent": result.intent,
                "confidence": result.confidence,
                "dispatch": result.debug.get("dispatch", ""),
                "expected_generator": item.expected_generator,
                "generator": generator,
                "expected_terms": list(item.expected_terms),
                "semantic_match": semantic,
                "response": result.response,
                "module_notes": result.debug.get("module_notes", ""),
                "note": item.note,
                "passed": passed,
            }
        )
    return rows


def _write_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Phase 27.34 Guarded Runtime Trial Samples", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']} — {'PASS' if row['passed'] else 'FAIL'}",
                "",
                f"- message: {row['message']}",
                f"- generator: {row['generator']}",
                f"- dispatch: {row['dispatch']}",
                f"- response: {row['response']}",
                f"- notes: {row['module_notes'] or '-'}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    rows = _run()
    passed = sum(1 for row in rows if row["passed"])
    total = len(rows)
    generator_rows = [row for row in rows if row["expected_generator"] != "template"]
    template_rows = [row for row in rows if row["expected_generator"] == "template"]
    status = (
        "PASSED_GUARDED_RUNTIME_TRIAL_READY_FOR_UI_TEST"
        if passed == total
        else "FAILED_GUARDED_RUNTIME_TRIAL_KEEP_TEMPLATE_DEFAULT"
    )
    report = {
        "phase": "Phase 27.34",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "checkpoint": "artifacts/eval/phase27_33_advice_micro_stabilization/checkpoints/sf-10m-step9800",
        "tokenizer": "artifacts/tokenizers/sf_bpe/v4_min_lexical",
        "trial_policy": {
            "request_flag": "generator_trial=true",
            "default_runtime": "template",
            "candidate_generator": "sf_10m_phase27_33",
            "fallback": "template on guard/policy failure",
        },
        "summary": {
            "passed": passed,
            "total": total,
            "generator_prompts": len(generator_rows),
            "template_controls": len(template_rows),
            "generator_passed": sum(1 for row in generator_rows if row["passed"]),
            "template_controls_passed": sum(1 for row in template_rows if row["passed"]),
        },
        "ui_test_allowed": passed == total,
        "sf50m_allowed": False,
        "next_phase": (
            "Phase 27.35 — live UI trial observations"
            if passed == total
            else "Phase 27.35 — runtime trial repair"
        ),
        "failures": [row for row in rows if not row["passed"]],
        "results": rows,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_samples(args.samples, rows)

    print("SF.AI — Phase 27.34 guarded runtime trial")
    print(f"  status          : {status}")
    print(f"  passed          : {passed}/{total}")
    print(f"  generator       : {report['trial_policy']['candidate_generator']}")
    print(f"  ui_test_allowed : {str(report['ui_test_allowed']).lower()}")
    print(f"  report          : {args.report}")
    print(f"  samples         : {args.samples}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
