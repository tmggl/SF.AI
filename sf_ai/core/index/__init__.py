"""sf_ai.core.index — Global capability registry and domain manifests."""

from sf_ai.core.index.capability_registry import CapabilityRegistry, load_default_registry
from sf_ai.core.index.domain_manifest import DomainManifest, IntentSpec

__all__ = [
    "CapabilityRegistry",
    "DomainManifest",
    "IntentSpec",
    "load_default_registry",
]
