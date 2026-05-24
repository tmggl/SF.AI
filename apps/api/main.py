"""SF.AI FastAPI entrypoint.

Endpoints:
- GET  /                 root info
- GET  /health           liveness probe
- GET  /system/status    phase + sovereign flags + components
- GET  /system/phase12-readiness  read-only training readiness + permission gate
- GET  /system/phase20-gates      read-only domain activation gates
- POST /chat/message     orchestrator dispatch (Phase 4 chat module)
- GET  /ui/chat          minimal Arabic-RTL chat UI (Phase 9)

No external AI APIs. No pretrained dependencies. See PROJECT_PRINCIPLES.md.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from apps.api.routers import chat, health, system, ui

# NOTE: SF.AI lexicons that need explicit env flags (e.g.
# ENABLE_SAUDI_SEED_V1_LEXICON) are turned on by the runtime launcher
# (`scripts/run_chat_server.sh` or `make api`), not by this module.
# Keeping `main.py` free of import-time side effects keeps test isolation
# clean — DialectMapper, NLPPipeline and Orchestrator pick up env flags at
# their first construction.

app = FastAPI(
    title="SF.AI API",
    version="0.1.0",
    description=(
        "SF.AI — Sovereign AI platform. Phase 9 chat UI mounted at /ui/chat. "
        "Phase 27.103 authored the topic prototype contrastive curriculum pack; runtime remains blocked. "
        "No pretrained models, no external AI APIs."
    ),
)

app.include_router(health.router)
app.include_router(system.router)
app.include_router(chat.router)
app.include_router(ui.router)


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {
        "project": "SF.AI",
        "phase": "Phase 27.103 — Topic Prototype Contrastive Curriculum Pack",
        "ui": "/ui/chat",
        "docs": "/docs",
    }


@app.get("/chat", include_in_schema=False)
def chat_redirect() -> RedirectResponse:
    """Convenience: visiting /chat in a browser opens the UI."""
    return RedirectResponse(url="/ui/chat", status_code=307)
