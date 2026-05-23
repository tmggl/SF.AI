"""Phase 27.9 — native generation quality harness.

This evaluates raw local checkpoints outside the chat UI. It is deliberately
stricter than perplexity: a checkpoint must answer short MSA/Saudi prompts
without malformed fragments before runtime can use it.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Protocol

from sf_ai.core.config import PROJECT_DIR
from sf_ai.modules.chat.generation_guard import GenerationGuard
from sf_ai.modules.chat.native_generator import NativeGenerationResult, NativeGenerator


DEFAULT_SUITE = PROJECT_DIR / "eval/prompts/generation_quality_v1.json"
DEFAULT_REPORT = PROJECT_DIR / "eval/reports/generation_quality_v1.json"
DEFAULT_ARTIFACT_REPORT = PROJECT_DIR / "artifacts/reports/generation_quality_v1_report.json"


class GeneratorLike(Protocol):
    def generate(
        self,
        prompt: str,
        *,
        dialect: str | None = None,
        max_new_tokens: int | None = None,
        temperature: float | None = None,
        top_k: int | None = None,
    ) -> NativeGenerationResult: ...


@dataclass(frozen=True)
class GenerationPrompt:
    id: str
    category: str
    dialect: str
    prompt: str
    required_terms: tuple[str, ...] = ()
    forbidden_terms: tuple[str, ...] = ()

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> "GenerationPrompt":
        return cls(
            id=str(raw["id"]),
            category=str(raw["category"]),
            dialect=str(raw["dialect"]),
            prompt=str(raw["prompt"]),
            required_terms=tuple(str(x) for x in raw.get("required_terms", ())),
            forbidden_terms=tuple(str(x) for x in raw.get("forbidden_terms", ())),
        )


@dataclass(frozen=True)
class GenerationQualityResult:
    id: str
    category: str
    dialect: str
    prompt: str
    passed: bool
    issues: tuple[str, ...]
    used: bool
    generator: str
    reason: str
    guard_reason: str
    repetition_ratio: float
    arabic_ratio: float
    response_preview: str


@dataclass(frozen=True)
class GenerationQualityReport:
    phase: str
    status: str
    language_track: tuple[str, ...]
    suite_path: str
    checkpoint_name: str
    generator_name: str
    total_prompts: int
    passed_prompts: int
    failed_prompts: int
    pass_rate: float
    guard_reason_counts: dict[str, int]
    category_counts: dict[str, int]
    runtime_allowed: bool
    blockers: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)
    results: tuple[GenerationQualityResult, ...] = field(default_factory=tuple)

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["language_track"] = list(self.language_track)
        data["blockers"] = list(self.blockers)
        data["notes"] = list(self.notes)
        data["results"] = [asdict(result) for result in self.results]
        return data


def load_generation_prompts(path: str | Path = DEFAULT_SUITE) -> tuple[GenerationPrompt, ...]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("generation quality suite must be a JSON list")
    prompts = tuple(GenerationPrompt.from_json(item) for item in raw)
    dialects = {prompt.dialect for prompt in prompts}
    if not dialects <= {"msa", "saudi"}:
        raise ValueError(f"generation suite dialects must stay msa/saudi only: {sorted(dialects)}")
    return prompts


def run_generation_quality_eval(
    *,
    suite_path: str | Path = DEFAULT_SUITE,
    generator: GeneratorLike | None = None,
    checkpoint_name: str = "sf-10m-step4000",
    generator_name: str = "sf_10m_v0_6",
    max_new_tokens: int = 48,
    temperature: float = 0.20,
    top_k: int = 0,
) -> GenerationQualityReport:
    prompts = load_generation_prompts(suite_path)
    gen = generator or NativeGenerator()
    guard = GenerationGuard()
    results = tuple(
        _evaluate_prompt(
            item,
            generator=gen,
            guard=guard,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_k=top_k,
        )
        for item in prompts
    )
    passed = sum(1 for result in results if result.passed)
    failed = len(results) - passed
    guard_counts: dict[str, int] = {}
    categories: dict[str, int] = {}
    for result in results:
        guard_counts[result.guard_reason] = guard_counts.get(result.guard_reason, 0) + 1
        categories[result.category] = categories.get(result.category, 0) + 1

    runtime_allowed = bool(results and failed == 0)
    blockers: list[str] = []
    if failed:
        blockers.append("generation_quality_failures")
    if any(result.guard_reason == "model_artifact_fragment" for result in results):
        blockers.append("model_artifact_fragments")
    if not runtime_allowed:
        blockers.append("runtime_generation_blocked")

    return GenerationQualityReport(
        phase="Phase 27.9 — Generation Quality Harness",
        status=(
            "PASSED_GENERATION_QUALITY_CANARY"
            if runtime_allowed
            else "BLOCKED_GENERATION_QUALITY_CANARY"
        ),
        language_track=("msa", "saudi"),
        suite_path=str(suite_path),
        checkpoint_name=checkpoint_name,
        generator_name=generator_name,
        total_prompts=len(results),
        passed_prompts=passed,
        failed_prompts=failed,
        pass_rate=round(passed / len(results), 4) if results else 0.0,
        guard_reason_counts=guard_counts,
        category_counts=categories,
        runtime_allowed=runtime_allowed,
        blockers=tuple(blockers),
        notes=(
            "This harness evaluates raw native generation outside the chat UI.",
            "Runtime remains template-first until this canary passes.",
        ),
        results=results,
    )


def _evaluate_prompt(
    item: GenerationPrompt,
    *,
    generator: GeneratorLike,
    guard: GenerationGuard,
    max_new_tokens: int,
    temperature: float,
    top_k: int,
) -> GenerationQualityResult:
    out = generator.generate(
        item.prompt,
        dialect=item.dialect,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
    )
    verdict = guard.inspect_for_prompt(item.prompt, out.text)
    issues: list[str] = []
    if not out.used:
        issues.append(f"generator_not_used:{out.reason}")
    if not verdict.allowed:
        issues.append(f"guard:{verdict.reason}")
    if item.required_terms and not any(term in out.text for term in item.required_terms):
        issues.append("missing_required_term")
    for term in item.forbidden_terms:
        if term and term in out.text:
            issues.append(f"forbidden_term:{term}")

    return GenerationQualityResult(
        id=item.id,
        category=item.category,
        dialect=item.dialect,
        prompt=item.prompt,
        passed=not issues,
        issues=tuple(issues),
        used=out.used,
        generator=out.generator,
        reason=out.reason,
        guard_reason=verdict.reason,
        repetition_ratio=round(verdict.repetition_ratio, 4),
        arabic_ratio=round(verdict.arabic_ratio, 4),
        response_preview=out.text[:220],
    )


def write_generation_quality_report(
    *,
    suite_path: str | Path = DEFAULT_SUITE,
    report_path: str | Path = DEFAULT_REPORT,
    artifact_path: str | Path = DEFAULT_ARTIFACT_REPORT,
    generator: GeneratorLike | None = None,
    checkpoint_name: str = "sf-10m-step4000",
    generator_name: str = "sf_10m_v0_6",
) -> GenerationQualityReport:
    report = run_generation_quality_eval(
        suite_path=suite_path,
        generator=generator,
        checkpoint_name=checkpoint_name,
        generator_name=generator_name,
    )
    for path in (Path(report_path), Path(artifact_path)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(report.to_json(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return report
