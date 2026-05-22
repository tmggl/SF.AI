"""Shared FastAPI dependencies and app-level configuration.

Phase 1: minimal — only the settings object. More dependencies (DB sessions,
auth, rate limiting, NLP pipeline) are added in their respective phases.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Project-wide settings loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="SF_",
        extra="ignore",
    )

    project_name: str = Field(default="SF.AI")
    env: str = Field(default="development")

    api_host: str = Field(default="127.0.0.1")
    api_port: int = Field(default=8000)
    api_log_level: str = Field(default="info")

    # auto | cpu | mps | cuda — used from Phase 5.5 onward.
    training_device: str = Field(default="auto")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached settings accessor."""
    return Settings()
