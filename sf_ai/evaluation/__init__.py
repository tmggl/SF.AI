"""SF.AI evaluation harnesses.

Phase 16 introduces prompt-suite evaluation before any native generator can be
activated in runtime chat.
"""

from sf_ai.evaluation.phase16 import (
    EvalCase,
    EvalCaseResult,
    Phase16Report,
    load_eval_cases,
    run_phase16_eval,
    write_phase16_report,
)
from sf_ai.evaluation.phase27 import (
    DialogueScenario,
    DialogueTurn,
    DialogueTurnResult,
    Phase27DialogueEvalReport,
    build_corpus_expansion_plan,
    load_dialogue_scenarios,
    run_phase27_dialogue_eval,
    write_phase27_dialogue_eval_report,
)
from sf_ai.evaluation.generation_quality import (
    GenerationPrompt,
    GenerationQualityReport,
    GenerationQualityResult,
    load_generation_prompts,
    run_generation_quality_eval,
    write_generation_quality_report,
)

__all__ = [
    "EvalCase",
    "EvalCaseResult",
    "Phase16Report",
    "load_eval_cases",
    "run_phase16_eval",
    "write_phase16_report",
    "DialogueScenario",
    "DialogueTurn",
    "DialogueTurnResult",
    "Phase27DialogueEvalReport",
    "build_corpus_expansion_plan",
    "load_dialogue_scenarios",
    "run_phase27_dialogue_eval",
    "write_phase27_dialogue_eval_report",
    "GenerationPrompt",
    "GenerationQualityReport",
    "GenerationQualityResult",
    "load_generation_prompts",
    "run_generation_quality_eval",
    "write_generation_quality_report",
]
