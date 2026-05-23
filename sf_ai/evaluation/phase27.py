"""Phase 27 dialogue evaluation v2 and corpus expansion plan.

This phase evaluates multi-turn routing/runtime behavior and translates the
Phase 26 scaling decision into a concrete corpus expansion target. It is
read-only: no training, no checkpoint writes, and no corpus mutation.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from sf_ai.core.config import PROJECT_DIR
from sf_ai.core.index import load_default_registry
from sf_ai.core.orchestrator import Orchestrator, UserMessage
from sf_ai.datasets.corpus_governance import audit_jsonl_directory_for_training
from sf_ai.modules.chat import ChatModule
from sf_ai.training.phase26_readiness import (
    MIN_SF50M_RECORDS,
    REQUIRED_DIALECTS,
    build_phase26_scaling_decision,
)


DEFAULT_DIALOGUE_SUITE = PROJECT_DIR / "eval/prompts/dialogue_v2.json"
DEFAULT_REPORT = PROJECT_DIR / "eval/reports/dialogue_eval_v2.json"
DEFAULT_ARTIFACT_REPORT = PROJECT_DIR / "artifacts/reports/phase27_dialogue_eval_v2_report.json"
DEFAULT_CORPUS_DIR = PROJECT_DIR / "data/corpus/chat/jsonl"
BATCH_SIZE = 500
TARGET_GOLD_RECORDS = 1_000


@dataclass(frozen=True)
class DialogueTurn:
    message: str
    expected_domain: str
    expected_intent: str
    expected_status: str
    expected_generator: str = "template"
    expected_requires_safety: bool = False
    allow_fallback: bool = False
    required_response_terms: tuple[str, ...] = ()
    forbidden_response_terms: tuple[str, ...] = ()

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> "DialogueTurn":
        return cls(
            message=str(raw["message"]),
            expected_domain=str(raw["expected_domain"]),
            expected_intent=str(raw["expected_intent"]),
            expected_status=str(raw["expected_status"]),
            expected_generator=str(raw.get("expected_generator", "template")),
            expected_requires_safety=bool(raw.get("expected_requires_safety", False)),
            allow_fallback=bool(raw.get("allow_fallback", False)),
            required_response_terms=tuple(raw.get("required_response_terms") or ()),
            forbidden_response_terms=tuple(raw.get("forbidden_response_terms") or ()),
        )


@dataclass(frozen=True)
class DialogueScenario:
    id: str
    category: str
    dialect: str
    turns: tuple[DialogueTurn, ...]

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> "DialogueScenario":
        turns = tuple(DialogueTurn.from_json(turn) for turn in raw["turns"])
        return cls(
            id=str(raw["id"]),
            category=str(raw["category"]),
            dialect=str(raw["dialect"]),
            turns=turns,
        )


@dataclass(frozen=True)
class DialogueTurnResult:
    scenario_id: str
    turn_index: int
    category: str
    message: str
    passed: bool
    issues: tuple[str, ...]
    domain: str
    intent: str
    status: str
    requires_safety: bool
    fallback_used: bool
    generator: str
    dispatch: str
    detected_dialect: str
    response_preview: str


@dataclass(frozen=True)
class Phase27DialogueEvalReport:
    phase: str
    status: str
    language_track: tuple[str, ...]
    suite_path: str
    total_scenarios: int
    total_turns: int
    passed_turns: int
    failed_turns: int
    pass_rate: float
    fallback_turns: int
    fallback_rate: float
    safety_turns: int
    generator_modes: dict[str, int]
    category_counts: dict[str, int]
    dialogue_baseline_passed: bool
    open_generator_ready: bool
    can_reopen_sf50m_gate: bool
    can_start_phase28: bool
    phase26_status: str
    corpus_expansion_plan: dict[str, object]
    blockers: tuple[str, ...] = field(default_factory=tuple)
    recommended_commands: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)
    results: tuple[DialogueTurnResult, ...] = field(default_factory=tuple)

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["language_track"] = list(self.language_track)
        data["blockers"] = list(self.blockers)
        data["recommended_commands"] = list(self.recommended_commands)
        data["notes"] = list(self.notes)
        data["results"] = [asdict(result) for result in self.results]
        return data


def load_dialogue_scenarios(path: str | Path = DEFAULT_DIALOGUE_SUITE) -> tuple[DialogueScenario, ...]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Phase 27 dialogue suite must be a JSON list")
    return tuple(DialogueScenario.from_json(item) for item in raw)


def run_phase27_dialogue_eval(
    *,
    suite_path: str | Path = DEFAULT_DIALOGUE_SUITE,
    project_dir: str | Path | None = None,
    orchestrator: Orchestrator | None = None,
) -> Phase27DialogueEvalReport:
    root = Path(project_dir) if project_dir is not None else PROJECT_DIR
    scenarios = load_dialogue_scenarios(root / Path(suite_path) if not Path(suite_path).is_absolute() else suite_path)
    orch = orchestrator or Orchestrator(
        registry=load_default_registry(),
        modules={"chat": ChatModule()},
    )

    results: list[DialogueTurnResult] = []
    for scenario in scenarios:
        session_id = f"phase27-{scenario.id}"
        for idx, turn in enumerate(scenario.turns, start=1):
            results.append(_evaluate_turn(scenario, idx, turn, orch, session_id))

    total_turns = len(results)
    passed_turns = sum(1 for result in results if result.passed)
    failed_turns = total_turns - passed_turns
    fallback_turns = sum(1 for result in results if result.fallback_used)
    safety_turns = sum(1 for result in results if result.requires_safety)
    generator_modes: dict[str, int] = {}
    category_counts: dict[str, int] = {}
    for result in results:
        generator_modes[result.generator] = generator_modes.get(result.generator, 0) + 1
        category_counts[result.category] = category_counts.get(result.category, 0) + 1

    phase26 = build_phase26_scaling_decision(root)
    corpus_plan = build_corpus_expansion_plan(root)
    dialogue_baseline_passed = failed_turns == 0
    open_generator_ready = bool(
        dialogue_baseline_passed
        and phase26.phase25.get("open_chat_allowed") is True
        and phase26.phase24.get("runtime_allowed") is True
    )
    can_reopen_sf50m_gate = bool(
        corpus_plan["remaining_records"] == 0 and open_generator_ready
    )
    can_start_phase28 = bool(can_reopen_sf50m_gate and phase26.can_start_sf50m_training)

    blockers: list[str] = []
    if failed_turns:
        blockers.append("dialogue_v2_turn_failures")
    if corpus_plan["remaining_records"]:
        blockers.append("corpus_expansion_required")
    if not open_generator_ready:
        blockers.append("open_generator_not_ready")
    if not phase26.can_start_sf50m_training:
        blockers.append("phase26_sf50m_gate_not_ready")
    blockers.append("sf50m_not_trained_or_validated")

    status = (
        "COMPLETED_DIALOGUE_EVAL_V2_BASELINE_PASS_EXPANSION_REQUIRED"
        if dialogue_baseline_passed
        else "FAILED_DIALOGUE_EVAL_V2_FIX_ROUTING_BEFORE_EXPANSION"
    )

    return Phase27DialogueEvalReport(
        phase="Phase 27 — Dialogue Evaluation v2 + Corpus Expansion Plan",
        status=status,
        language_track=REQUIRED_DIALECTS,
        suite_path=str(Path(suite_path)),
        total_scenarios=len(scenarios),
        total_turns=total_turns,
        passed_turns=passed_turns,
        failed_turns=failed_turns,
        pass_rate=round(passed_turns / total_turns, 4) if total_turns else 0.0,
        fallback_turns=fallback_turns,
        fallback_rate=round(fallback_turns / total_turns, 4) if total_turns else 0.0,
        safety_turns=safety_turns,
        generator_modes=generator_modes,
        category_counts=category_counts,
        dialogue_baseline_passed=dialogue_baseline_passed,
        open_generator_ready=open_generator_ready,
        can_reopen_sf50m_gate=can_reopen_sf50m_gate,
        can_start_phase28=can_start_phase28,
        phase26_status=phase26.status,
        corpus_expansion_plan=corpus_plan,
        blockers=tuple(dict.fromkeys(blockers)),
        recommended_commands=(
            "make phase27-dialogue-eval",
            "make corpus-audit",
            "expand governed msa+saudi corpus toward 5000 records",
            "rerun make phase26-readiness after corpus expansion and SF-10M canary repair",
        ),
        notes=(
            "Phase 27 evaluates the current routing/runtime baseline; it does not train.",
            "All runtime dialogue remains template-based until generator quality gates pass.",
            "Corpus expansion must stay inside msa + saudi with source/license/quality/training_allowed metadata.",
            "Phase 28 is blocked until SF-50M is trained and passes Dialogue Evaluation v2.",
        ),
        results=tuple(results),
    )


def build_corpus_expansion_plan(
    project_dir: str | Path | None = None,
) -> dict[str, object]:
    root = Path(project_dir) if project_dir is not None else PROJECT_DIR
    corpus = audit_jsonl_directory_for_training(root / DEFAULT_CORPUS_DIR.relative_to(PROJECT_DIR))
    current_records = corpus.training_ready
    remaining_records = max(MIN_SF50M_RECORDS - current_records, 0)
    target_per_dialect = MIN_SF50M_RECORDS // len(REQUIRED_DIALECTS)
    dialect_counts = dict(corpus.dialect_counts)
    needed_by_dialect = {
        dialect: max(target_per_dialect - dialect_counts.get(dialect, 0), 0)
        for dialect in REQUIRED_DIALECTS
    }
    current_gold = int(corpus.quality_counts.get("gold", 0))
    current_silver = int(corpus.quality_counts.get("silver", 0))
    needed_gold = max(TARGET_GOLD_RECORDS - current_gold, 0)
    needed_silver = max(remaining_records - needed_gold, 0)

    return {
        "current_records": current_records,
        "target_records": MIN_SF50M_RECORDS,
        "remaining_records": remaining_records,
        "batch_size": BATCH_SIZE,
        "batches_needed_total": _ceil_div(remaining_records, BATCH_SIZE),
        "target_per_dialect": target_per_dialect,
        "dialect_counts": dialect_counts,
        "needed_by_dialect": needed_by_dialect,
        "batches_by_dialect": {
            dialect: _ceil_div(needed, BATCH_SIZE)
            for dialect, needed in needed_by_dialect.items()
        },
        "quality_targets": {
            "gold_total_target": TARGET_GOLD_RECORDS,
            "silver_total_target": MIN_SF50M_RECORDS - TARGET_GOLD_RECORDS,
            "current_gold": current_gold,
            "current_silver": current_silver,
            "needed_gold": needed_gold,
            "needed_silver": needed_silver,
        },
        "category_targets_remaining": {
            "social_smalltalk": 600,
            "everyday_question_answer": 650,
            "msa_daily_explanation": 550,
            "saudi_daily_dialogue": 650,
            "context_followup": 500,
            "clarification_repair": 450,
            "everyday_decisions": 400,
            "polite_disagreement_and_apology": 300,
            "feelings_and_reassurance": 257,
        },
        "allowed_dialects": list(REQUIRED_DIALECTS),
        "disallowed_sources": [
            "synthetic_llm_data",
            "pretrained_model_outputs",
            "unknown_license_corpus",
            "unreviewed_chat_review_exports",
        ],
    }


def write_phase27_dialogue_eval_report(
    *,
    suite_path: str | Path = DEFAULT_DIALOGUE_SUITE,
    output: str | Path = DEFAULT_REPORT,
    artifact_output: str | Path = DEFAULT_ARTIFACT_REPORT,
) -> Phase27DialogueEvalReport:
    report = run_phase27_dialogue_eval(suite_path=suite_path)
    for out in (Path(output), Path(artifact_output)):
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(report.to_json(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return report


def _evaluate_turn(
    scenario: DialogueScenario,
    turn_index: int,
    turn: DialogueTurn,
    orch: Orchestrator,
    session_id: str,
) -> DialogueTurnResult:
    result = orch.process(UserMessage(text=turn.message, session_id=session_id))
    debug = result.debug
    generator = debug.get("generator", "template")
    issues: list[str] = []
    checks: dict[str, tuple[object, object]] = {
        "domain": (result.domain, turn.expected_domain),
        "intent": (result.intent, turn.expected_intent),
        "status": (result.status, turn.expected_status),
        "requires_safety": (result.requires_safety, turn.expected_requires_safety),
        "generator": (generator, turn.expected_generator),
    }
    for name, (actual, expected) in checks.items():
        if actual != expected:
            issues.append(f"{name}: expected {expected!r}, got {actual!r}")
    if result.fallback_used and not turn.allow_fallback:
        issues.append("unexpected_fallback")
    for term in turn.required_response_terms:
        if term not in result.response:
            issues.append(f"missing required response term: {term!r}")
    for term in turn.forbidden_response_terms:
        if term in result.response:
            issues.append(f"forbidden response term present: {term!r}")

    return DialogueTurnResult(
        scenario_id=scenario.id,
        turn_index=turn_index,
        category=scenario.category,
        message=turn.message,
        passed=not issues,
        issues=tuple(issues),
        domain=result.domain,
        intent=result.intent,
        status=result.status,
        requires_safety=result.requires_safety,
        fallback_used=result.fallback_used,
        generator=generator,
        dispatch=debug.get("dispatch", ""),
        detected_dialect=debug.get("dialect", ""),
        response_preview=result.response[:180],
    )


def _ceil_div(value: int, divisor: int) -> int:
    if value <= 0:
        return 0
    return (value + divisor - 1) // divisor
