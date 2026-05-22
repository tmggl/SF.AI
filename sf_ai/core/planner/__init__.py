"""sf_ai.core.planner — task decomposition.

Phase 2 ships a minimal stub: a planner that returns a single-step plan
("respond directly"). Phase 7+ will use this layer to split web research
into sub-tasks (search → fetch → extract → summarize → cite).
"""

from sf_ai.core.planner.planner import Planner
from sf_ai.core.planner.task_steps import Plan, TaskStep

__all__ = ["Plan", "Planner", "TaskStep"]
