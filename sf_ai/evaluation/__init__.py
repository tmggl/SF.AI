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

__all__ = [
    "EvalCase",
    "EvalCaseResult",
    "Phase16Report",
    "load_eval_cases",
    "run_phase16_eval",
    "write_phase16_report",
]
