"""GET /ui/chat — minimal Arabic RTL chat UI for testing the system.

Single-file HTML served from `apps/api/static/chat.html`. Designed to be
loaded directly from a browser pointed at the running FastAPI server —
no Node, no build step, no external CDNs.

This is Phase 9's offline-ready chat surface. A richer Next.js client
remains an optional follow-up under `apps/web/`.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse

router = APIRouter(prefix="/ui", tags=["ui"])

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
CHAT_HTML = STATIC_DIR / "chat.html"


@router.get("/chat", response_class=HTMLResponse)
def chat_page() -> FileResponse:
    return FileResponse(CHAT_HTML, media_type="text/html; charset=utf-8")
