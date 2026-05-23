"""GET /health — basic liveness probe."""

from __future__ import annotations

from fastapi import APIRouter

from apps.api.schemas.system import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", project="SF.AI", phase="Phase 27.35")
