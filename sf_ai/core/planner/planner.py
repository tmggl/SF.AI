"""Planner — Phase 2 stub.

Returns a one-step plan for every input. Real planning (decomposition,
dependency graph, tool selection) is introduced in later phases.
"""

from __future__ import annotations

from sf_ai.core.planner.task_steps import Plan, TaskStep


class Planner:
    def plan(self, goal: str, domain: str, intent: str) -> Plan:
        step = TaskStep(
            name="respond_directly",
            description=f"Respond to {domain}/{intent} without multi-step planning.",
        )
        return Plan(goal=goal, steps=(step,), notes="Phase 2 stub: single-step.")
