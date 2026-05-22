"""Loads `default_registry.yaml` and exposes domains/intents to the router."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from sf_ai.core.config import DEFAULT_REGISTRY_PATH
from sf_ai.core.index.domain_manifest import (
    DomainManifest,
    IntentSpec,
    RegistryFallback,
    RegistryMeta,
)


class CapabilityRegistry:
    """Read-only view over the global registry."""

    def __init__(self, domains: dict[str, DomainManifest], meta: RegistryMeta) -> None:
        self._domains = domains
        self._meta = meta

    # ----- domain access -----

    def all_domains(self) -> list[DomainManifest]:
        return list(self._domains.values())

    def domain_names(self) -> list[str]:
        return list(self._domains.keys())

    def get_domain(self, name: str) -> DomainManifest | None:
        return self._domains.get(name)

    def active_domains(self) -> list[DomainManifest]:
        return [d for d in self._domains.values() if d.status == "active"]

    def skeleton_domains(self) -> list[DomainManifest]:
        return [d for d in self._domains.values() if d.status == "skeleton_only"]

    def safety_domains(self) -> list[DomainManifest]:
        return [d for d in self._domains.values() if d.requires_safety]

    # ----- meta -----

    @property
    def meta(self) -> RegistryMeta:
        return self._meta

    @property
    def fallback(self) -> RegistryFallback:
        return self._meta.fallback


def _parse_intent(name: str, raw: dict[str, Any] | None) -> IntentSpec:
    raw = raw or {}
    return IntentSpec(
        name=name,
        description=str(raw.get("description", "")),
        phrases=tuple(raw.get("phrases") or ()),
        keywords=tuple(raw.get("keywords") or ()),
        fallback=bool(raw.get("fallback", False)),
    )


def _parse_domain(name: str, raw: dict[str, Any]) -> DomainManifest:
    intents_raw = raw.get("intents") or {}
    intents: tuple[IntentSpec, ...] = tuple(
        _parse_intent(intent_name, intent_body)
        for intent_name, intent_body in intents_raw.items()
    )
    return DomainManifest(
        name=name,
        description=str(raw.get("description", "")),
        status=str(raw.get("status", "skeleton_only")),
        requires_safety=bool(raw.get("requires_safety", False)),
        phrases=tuple(raw.get("phrases") or ()),
        keywords=tuple(raw.get("keywords") or ()),
        intents=intents,
        allowed_tools=tuple(raw.get("allowed_tools") or ()),
        limitations=tuple(raw.get("limitations") or ()),
        notes=str(raw.get("notes", "")),
    )


def _parse_meta(raw: dict[str, Any] | None) -> RegistryMeta:
    raw = raw or {}
    fb_raw = raw.get("fallback") or {}
    fallback = RegistryFallback(
        domain=str(fb_raw.get("domain", "chat")),
        intent=str(fb_raw.get("intent", "chat.general")),
        response_style=str(fb_raw.get("response_style", "arabic_formal")),
    )
    return RegistryMeta(
        version=str(raw.get("version", "0.2")),
        schema_version=str(raw.get("schema_version", "phase2")),
        generated_at=str(raw.get("generated_at", "")),
        fallback=fallback,
    )


def load_registry_from_path(path: Path) -> CapabilityRegistry:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Invalid registry file: {path} (expected mapping)")
    meta = _parse_meta(data.get("meta"))
    domains_raw = data.get("domains") or {}
    domains = {name: _parse_domain(name, body) for name, body in domains_raw.items()}
    return CapabilityRegistry(domains=domains, meta=meta)


def load_default_registry() -> CapabilityRegistry:
    return load_registry_from_path(DEFAULT_REGISTRY_PATH)
