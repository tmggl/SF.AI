"""Server status helper must remain read-only."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_server_status_script_is_read_only() -> None:
    script = ROOT / "scripts/server_status.sh"
    text = script.read_text(encoding="utf-8")
    assert "pkill" not in text
    assert "kill -" not in text
    assert "run_chat_server" not in text
    assert "uvicorn" not in text
    assert "nohup" not in text
    assert "/health" in text
    assert "lsof" in text
