"""Phase 16 evaluation harness.

This harness evaluates the current runtime contract, not an external model:

- Arabic-first / Saudi-aware prompt suites.
- Safety and skeleton-domain gates.
- Generator metadata stays `template` until a future gate allows otherwise.
- Phase 14 generation samples are checked for repetition so the report can
  explicitly block runtime activation.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

from sf_ai.core.index import load_default_registry
from sf_ai.core.orchestrator import Orchestrator, UserMessage


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CHAT_PROMPTS = ROOT / "eval/prompts/saudi_msa_chat_v1.jsonl"
DEFAULT_SAFETY_PROMPTS = ROOT / "eval/prompts/safety_v1.jsonl"
DEFAULT_REPORT = ROOT / "eval/reports/sf_10m_eval_v1.json"
DEFAULT_GENERATION_SAMPLE = ROOT / "artifacts/samples/sf_10m_generations.md"

ALLOWED_RUNTIME_DIALECTS = ("msa", "saudi")
LEXICON_POLICY = {
    "runtime_focus": ["msa", "saudi"],
    "base_lexicons": [
        "resources/lexicons/dialects_gulf.yaml (Saudi-labeled runtime seed)",
        "resources/lexicons/intents.yaml",
        "resources/lexicons/safety_terms.yaml",
    ],
    "user_authored_reference": "resources/lexicons/imported/saudi_seed_v1/",
    "tokenization_policy": "resources/tokenization/",
    "wider_dialects_runtime": False,
}


@dataclass(frozen=True)
class EvalCase:
    id: str
    suite: str
    message: str
    category: str
    dialect: str
    expected_domain: str
    expected_intent: str
    expected_status: str
    expected_generator: str = "template"
    expected_requires_safety: bool = False
    required_response_terms: tuple[str, ...] = ()
    forbidden_response_terms: tuple[str, ...] = ()

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> "EvalCase":
        return cls(
            id=str(raw["id"]),
            suite=str(raw["suite"]),
            message=str(raw["message"]),
            category=str(raw["category"]),
            dialect=str(raw["dialect"]),
            expected_domain=str(raw["expected_domain"]),
            expected_intent=str(raw["expected_intent"]),
            expected_status=str(raw["expected_status"]),
            expected_generator=str(raw.get("expected_generator", "template")),
            expected_requires_safety=bool(raw.get("expected_requires_safety", False)),
            required_response_terms=tuple(raw.get("required_response_terms") or ()),
            forbidden_response_terms=tuple(raw.get("forbidden_response_terms") or ()),
        )


@dataclass(frozen=True)
class EvalCaseResult:
    id: str
    suite: str
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
class Phase16Report:
    phase: str
    status: str
    total_cases: int
    passed_cases: int
    failed_cases: int
    pass_rate: float
    runtime_activation_allowed: bool
    generator_gate: dict[str, Any]
    lexicon_policy: dict[str, Any]
    suites: dict[str, int]
    results: tuple[EvalCaseResult, ...] = field(default_factory=tuple)

    def to_json(self) -> dict[str, Any]:
        return {
            "phase": self.phase,
            "status": self.status,
            "total_cases": self.total_cases,
            "passed_cases": self.passed_cases,
            "failed_cases": self.failed_cases,
            "pass_rate": self.pass_rate,
            "runtime_activation_allowed": self.runtime_activation_allowed,
            "generator_gate": self.generator_gate,
            "lexicon_policy": self.lexicon_policy,
            "suites": self.suites,
            "results": [asdict(r) for r in self.results],
        }


def load_eval_cases(paths: Iterable[str | Path]) -> list[EvalCase]:
    cases: list[EvalCase] = []
    for p in paths:
        path = Path(p)
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSONL at {path}:{line_no}") from exc
            cases.append(EvalCase.from_json(raw))
    return cases


def run_phase16_eval(
    cases: Iterable[EvalCase],
    *,
    orchestrator: Orchestrator | None = None,
    generation_sample_path: str | Path = DEFAULT_GENERATION_SAMPLE,
) -> Phase16Report:
    orch = orchestrator or Orchestrator(registry=load_default_registry())
    results = tuple(_evaluate_case(case, orch) for case in cases)
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    sample_gate = _generation_sample_gate(Path(generation_sample_path))
    runtime_activation_allowed = failed == 0 and sample_gate["activation_allowed"] is True

    suites: dict[str, int] = {}
    for r in results:
        suites[r.suite] = suites.get(r.suite, 0) + 1

    return Phase16Report(
        phase="Phase 16 — Evaluation, Safety, and Saudi/MSA Style Harness",
        status="PASS_WITH_RUNTIME_BLOCKED" if failed == 0 else "FAIL",
        total_cases=total,
        passed_cases=passed,
        failed_cases=failed,
        pass_rate=round(passed / total, 4) if total else 0.0,
        runtime_activation_allowed=runtime_activation_allowed,
        generator_gate=sample_gate,
        lexicon_policy=LEXICON_POLICY,
        suites=suites,
        results=results,
    )


def write_phase16_report(
    *,
    chat_prompts: str | Path = DEFAULT_CHAT_PROMPTS,
    safety_prompts: str | Path = DEFAULT_SAFETY_PROMPTS,
    output: str | Path = DEFAULT_REPORT,
) -> Phase16Report:
    cases = load_eval_cases([chat_prompts, safety_prompts])
    report = run_phase16_eval(cases)
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(report.to_json(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report


def _evaluate_case(case: EvalCase, orch: Orchestrator) -> EvalCaseResult:
    result = orch.process(UserMessage(text=case.message, session_id=f"eval-{case.id}"))
    issues: list[str] = []
    debug = result.debug
    generator = debug.get("generator", "template")
    detected_dialect = debug.get("dialect", "")

    checks = {
        "domain": (result.domain, case.expected_domain),
        "intent": (result.intent, case.expected_intent),
        "status": (result.status, case.expected_status),
        "generator": (generator, case.expected_generator),
        "requires_safety": (result.requires_safety, case.expected_requires_safety),
    }
    for name, (actual, expected) in checks.items():
        if actual != expected:
            issues.append(f"{name}: expected {expected!r}, got {actual!r}")

    if case.dialect not in ALLOWED_RUNTIME_DIALECTS:
        issues.append(f"case dialect {case.dialect!r} is outside allowed runtime dialects")
    if detected_dialect and detected_dialect not in ALLOWED_RUNTIME_DIALECTS:
        issues.append(f"detected dialect {detected_dialect!r} is outside allowed runtime dialects")

    for term in case.required_response_terms:
        if term not in result.response:
            issues.append(f"missing required response term: {term!r}")
    for term in case.forbidden_response_terms:
        if term in result.response:
            issues.append(f"forbidden response term present: {term!r}")

    return EvalCaseResult(
        id=case.id,
        suite=case.suite,
        category=case.category,
        message=case.message,
        passed=not issues,
        issues=tuple(issues),
        domain=result.domain,
        intent=result.intent,
        status=result.status,
        requires_safety=result.requires_safety,
        fallback_used=result.fallback_used,
        generator=generator,
        dispatch=debug.get("dispatch", ""),
        detected_dialect=detected_dialect,
        response_preview=result.response[:180],
    )


def _generation_sample_gate(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    repeated_markers = (
        text.count("المعنى:") >= 3
        or text.count("المعنى") >= 5
        or "must not replace ChatModule" in text
    )
    return {
        "candidate": "sf_10m_v0_1",
        "sample_path": str(path.relative_to(ROOT)) if path.exists() else str(path),
        "sample_exists": path.exists(),
        "repetition_detected": repeated_markers,
        "activation_allowed": False,
        "reason": (
            "Phase 14 generation is non-empty but repetitive; keep generator=template"
            if repeated_markers
            else "Activation still requires explicit Phase 16+ quality approval"
        ),
    }
