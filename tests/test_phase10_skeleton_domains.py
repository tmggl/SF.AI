"""Phase 10 — later domain skeleton manifests and module contracts."""

from __future__ import annotations

import importlib
from pathlib import Path

import yaml

from sf_ai.core.config import PROJECT_DIR
from sf_ai.core.index import load_default_registry
from sf_ai.modules._skeleton import SkeletonDomainModule, SkeletonRequest


PHASE10_DOMAINS = (
    "coding",
    "data",
    "files",
    "legal",
    "medical",
    "finance",
    "education",
    "religion",
    "social",
    "productivity",
    "writing",
    "translation",
    "image",
    "audio",
    "security",
    "business",
    "ecommerce",
)

SENSITIVE = {"legal", "medical", "finance", "security", "religion"}

CLASS_NAMES = {
    "coding": "CodingModule",
    "data": "DataModule",
    "files": "FilesModule",
    "legal": "LegalModule",
    "medical": "MedicalModule",
    "finance": "FinanceModule",
    "education": "EducationModule",
    "religion": "ReligionModule",
    "social": "SocialModule",
    "productivity": "ProductivityModule",
    "writing": "WritingModule",
    "translation": "TranslationModule",
    "image": "ImageModule",
    "audio": "AudioModule",
    "security": "SecurityModule",
    "business": "BusinessModule",
    "ecommerce": "EcommerceModule",
}


def _manifest_path(domain: str) -> Path:
    return PROJECT_DIR / "sf_ai" / "modules" / domain / "manifest.yaml"


def _load_manifest(domain: str) -> dict:
    with _manifest_path(domain).open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    assert isinstance(data, dict)
    return data


def test_phase10_domains_have_manifest_and_module_files() -> None:
    for domain in PHASE10_DOMAINS:
        base = PROJECT_DIR / "sf_ai" / "modules" / domain
        assert (base / "__init__.py").exists(), f"missing __init__ for {domain}"
        assert (base / "module.py").exists(), f"missing module.py for {domain}"
        assert (base / "manifest.yaml").exists(), f"missing manifest.yaml for {domain}"


def test_phase10_manifests_are_skeleton_only() -> None:
    for domain in PHASE10_DOMAINS:
        manifest = _load_manifest(domain)
        assert manifest["domain"] == domain
        assert manifest["phase"] == "Phase 10"
        assert manifest["status"] == "skeleton_only"
        assert manifest["allowed_tools"] == []
        assert isinstance(manifest["limitations"], list)
        assert manifest["limitations"], f"{domain} must declare limitations"
        assert bool(manifest["requires_safety"]) is (domain in SENSITIVE)


def test_phase10_modules_are_non_executing_skeletons() -> None:
    for domain in PHASE10_DOMAINS:
        mod = importlib.import_module(f"sf_ai.modules.{domain}.module")
        cls = getattr(mod, CLASS_NAMES[domain])
        instance = cls()
        assert isinstance(instance, SkeletonDomainModule)
        assert instance.domain == domain
        assert instance.status == "skeleton_only"
        assert instance.requires_safety is (domain in SENSITIVE)
        response = instance.handle(SkeletonRequest(text="test", intent=f"{domain}.general"))
        assert response.domain == domain
        assert response.status == "skeleton_only"
        assert response.requires_safety is (domain in SENSITIVE)
        assert response.allowed_tools == ()
        assert response.limitations


def test_registry_still_keeps_phase10_domains_inactive() -> None:
    reg = load_default_registry()
    for domain in PHASE10_DOMAINS:
        manifest = reg.get_domain(domain)
        assert manifest is not None
        assert manifest.status == "skeleton_only"
        assert manifest.requires_safety is (domain in SENSITIVE)

    assert [d.name for d in reg.active_domains()] == ["chat"]
