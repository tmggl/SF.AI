"""Phase 20 — read-only domain activation gates.

The gates do not activate domains. They answer one question: if a future
agent wants to turn a skeleton domain into runtime behavior, what blocks it?
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path

from sf_ai.core.config import PROJECT_DIR
from sf_ai.core.index import load_default_registry
from sf_ai.datasets.corpus_governance import audit_jsonl_directory_for_training
from sf_ai.training.phase19_readiness import build_phase19_readiness_decision


TEXT_GENERATION_DOMAINS = frozenset(
    {
        "coding",
        "data",
        "files",
        "education",
        "social",
        "writing",
        "translation",
        "business",
        "ecommerce",
    }
)
SENSITIVE_DOMAINS = frozenset({"legal", "medical", "finance", "security", "religion"})
MEDIA_DOMAINS = frozenset({"image", "audio"})
OFFLINE_READY_DOMAINS = frozenset({"web", "research"})
ALLOWED_RUNTIME_STATUSES = frozenset({"active", "ready_offline", "skeleton_only"})


@dataclass(frozen=True)
class DomainGateResult:
    domain: str
    current_status: str
    requires_safety: bool
    manifest_present: bool
    registry_present: bool
    data_ready: bool
    safety_policy_ready: bool
    tests_ready: bool
    ui_indication_ready: bool
    fallback_path_ready: bool
    allowed_tools_declared: bool
    can_activate_now: bool
    recommended_status: str
    action: str
    blockers: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["blockers"] = list(self.blockers)
        data["notes"] = list(self.notes)
        return data


@dataclass(frozen=True)
class DomainActivationDecision:
    phase: str
    status: str
    language_track: tuple[str, ...]
    lexicon_track: str
    total_domains: int
    active_domains: tuple[str, ...]
    ready_offline_domains: tuple[str, ...]
    candidate_domains: tuple[str, ...]
    blocked_domains: tuple[str, ...]
    sensitive_domains: tuple[str, ...]
    can_activate_any_domain: bool
    gates: tuple[DomainGateResult, ...]
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["language_track"] = list(self.language_track)
        data["active_domains"] = list(self.active_domains)
        data["ready_offline_domains"] = list(self.ready_offline_domains)
        data["candidate_domains"] = list(self.candidate_domains)
        data["blocked_domains"] = list(self.blocked_domains)
        data["sensitive_domains"] = list(self.sensitive_domains)
        data["gates"] = [gate.to_json() for gate in self.gates]
        data["notes"] = list(self.notes)
        return data


def build_phase20_activation_gates(
    project_dir: str | Path | None = None,
) -> DomainActivationDecision:
    root = Path(project_dir) if project_dir is not None else PROJECT_DIR
    registry = load_default_registry()
    corpus = audit_jsonl_directory_for_training(root / "data/corpus/chat/jsonl")
    phase19 = build_phase19_readiness_decision(root)
    system_router = root / "apps/api/routers/system.py"
    composer = root / "sf_ai/core/composer/response_composer.py"

    gates: list[DomainGateResult] = []
    for domain in registry.all_domains():
        manifest_path = root / "sf_ai/modules" / domain.name / "manifest.yaml"
        test_path = root / "tests" / f"test_{domain.name}.py"
        manifest_present = manifest_path.exists() or domain.name == "chat"
        registry_present = domain.name in registry.domain_names()
        allowed_tools_declared = domain.status == "active" or domain.allowed_tools == ()
        fallback_path_ready = composer.exists() and (
            domain.status != "active" or domain.name == "chat"
        )
        ui_indication_ready = _file_contains(system_router, f"{domain.name}_module") or (
            domain.name in {"chat", "web", "research"}
        )
        tests_ready = _domain_tests_ready(root, domain.name, test_path)
        data_ready = _domain_data_ready(
            domain.name,
            training_records=corpus.training_ready,
            sf50_ready=phase19.can_start_training,
        )
        safety_policy_ready = _safety_policy_ready(root, domain.name, domain.requires_safety)

        blockers = _collect_blockers(
            current_status=domain.status,
            manifest_present=manifest_present,
            registry_present=registry_present,
            data_ready=data_ready,
            safety_policy_ready=safety_policy_ready,
            tests_ready=tests_ready,
            ui_indication_ready=ui_indication_ready,
            fallback_path_ready=fallback_path_ready,
            allowed_tools_declared=allowed_tools_declared,
        )
        can_activate = domain.status == "active" or not blockers
        recommended_status = _recommended_status(domain.name, domain.status, can_activate)
        action = _action_for(domain.name, domain.status, blockers)

        gates.append(
            DomainGateResult(
                domain=domain.name,
                current_status=domain.status,
                requires_safety=domain.requires_safety,
                manifest_present=manifest_present,
                registry_present=registry_present,
                data_ready=data_ready,
                safety_policy_ready=safety_policy_ready,
                tests_ready=tests_ready,
                ui_indication_ready=ui_indication_ready,
                fallback_path_ready=fallback_path_ready,
                allowed_tools_declared=allowed_tools_declared,
                can_activate_now=can_activate,
                recommended_status=recommended_status,
                action=action,
                blockers=blockers,
                notes=_notes_for(domain.name, domain.status),
            )
        )

    active = tuple(g.domain for g in gates if g.current_status == "active")
    ready_offline = tuple(g.domain for g in gates if g.domain in OFFLINE_READY_DOMAINS)
    candidates = tuple(
        g.domain for g in gates if g.can_activate_now and g.current_status != "active"
    )
    blocked = tuple(g.domain for g in gates if not g.can_activate_now)

    return DomainActivationDecision(
        phase="Phase 20 — Domain Activation Gates",
        status="PHASE20_GATES_ACTIVE_NO_DOMAIN_AUTO_ACTIVATED",
        language_track=("msa", "saudi"),
        lexicon_track="Saudi Seed v1 + governed MSA/Saudi corpus only",
        total_domains=len(gates),
        active_domains=active,
        ready_offline_domains=ready_offline,
        candidate_domains=candidates,
        blocked_domains=blocked,
        sensitive_domains=tuple(sorted(SENSITIVE_DOMAINS)),
        can_activate_any_domain=bool(candidates),
        gates=tuple(sorted(gates, key=lambda g: (g.domain != "chat", g.domain))),
        notes=(
            "This decision is read-only and never changes registry status.",
            "Phase 20 prevents silent activation of skeleton domains.",
            "Arabic MSA + Saudi remain the only active language track.",
        ),
    )


def _domain_data_ready(domain: str, *, training_records: int, sf50_ready: bool) -> bool:
    if domain == "chat":
        return True
    if domain in OFFLINE_READY_DOMAINS:
        return True
    if domain in SENSITIVE_DOMAINS:
        return False
    if domain in MEDIA_DOMAINS:
        return False
    if domain in TEXT_GENERATION_DOMAINS:
        return sf50_ready and training_records >= 5_000
    return False


def _safety_policy_ready(root: Path, domain: str, requires_safety: bool) -> bool:
    if not requires_safety:
        return True
    policy = root / "docs/domain_policies" / f"{domain}.md"
    return policy.exists()


def _domain_tests_ready(root: Path, domain: str, direct_test_path: Path) -> bool:
    if domain == "chat":
        return True
    if direct_test_path.exists():
        return True
    if domain in OFFLINE_READY_DOMAINS:
        return (root / "tests/test_web_extractor.py").exists() and (
            root / "tests/test_research_summarizer.py"
        ).exists()
    return False


def _collect_blockers(
    *,
    current_status: str,
    manifest_present: bool,
    registry_present: bool,
    data_ready: bool,
    safety_policy_ready: bool,
    tests_ready: bool,
    ui_indication_ready: bool,
    fallback_path_ready: bool,
    allowed_tools_declared: bool,
) -> tuple[str, ...]:
    if current_status == "active":
        return ()
    blockers: list[str] = []
    if current_status not in ALLOWED_RUNTIME_STATUSES:
        blockers.append("invalid_domain_status")
    if not manifest_present:
        blockers.append("manifest_missing")
    if not registry_present:
        blockers.append("registry_entry_missing")
    if not data_ready:
        blockers.append("data_or_model_not_ready")
    if not safety_policy_ready:
        blockers.append("safety_policy_missing")
    if not tests_ready:
        blockers.append("domain_activation_tests_missing")
    if not ui_indication_ready:
        blockers.append("ui_status_indication_missing")
    if not fallback_path_ready:
        blockers.append("fallback_path_missing")
    if not allowed_tools_declared:
        blockers.append("allowed_tools_policy_missing")
    return tuple(blockers)


def _recommended_status(domain: str, current_status: str, can_activate: bool) -> str:
    if current_status == "active":
        return "keep_active"
    if domain in OFFLINE_READY_DOMAINS:
        return "keep_ready_offline_until_explicit_domain_activation"
    if can_activate:
        return "eligible_for_explicit_activation_review"
    return "keep_skeleton_only"


def _action_for(domain: str, current_status: str, blockers: tuple[str, ...]) -> str:
    if current_status == "active":
        return "KEEP_ACTIVE"
    if domain in OFFLINE_READY_DOMAINS:
        return "KEEP_OFFLINE_READY_AND_ADD_EXPLICIT_ACTIVATION_TESTS"
    if blockers:
        return "KEEP_SKELETON_AND_CLOSE_BLOCKERS"
    return "OPEN_EXPLICIT_ACTIVATION_REVIEW"


def _notes_for(domain: str, current_status: str) -> tuple[str, ...]:
    if domain == "chat":
        return ("Primary runtime domain; social replies stay template-first until native generation improves.",)
    if domain in SENSITIVE_DOMAINS:
        return ("Sensitive domain: must stay safety-first and specialist-bounded.",)
    if domain in MEDIA_DOMAINS:
        return ("Media generation needs a separate sovereign data/model plan.",)
    if current_status == "ready_offline":
        return ("Implementation exists offline, but runtime activation still needs an explicit gate decision.",)
    return ("Skeleton domain; no runtime execution should be promised.",)


def _file_contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    try:
        return needle in path.read_text(encoding="utf-8")
    except OSError:
        return False
