"""Plan/TaskStep dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TaskStep:
    name: str
    description: str = ""
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()


@dataclass(frozen=True)
class Plan:
    goal: str
    steps: tuple[TaskStep, ...] = field(default_factory=tuple)
    notes: str = ""

    @property
    def is_single_step(self) -> bool:
        return len(self.steps) <= 1
