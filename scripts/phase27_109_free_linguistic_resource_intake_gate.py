#!/usr/bin/env python3
"""Phase 27.109 — free linguistic resource intake gate.

This phase accelerates SF.AI with public linguistic resources without importing
pretrained weights, vocabularies, tokenizer merges, hidden APIs, or unchecked
dialogue datasets.

It may fetch public *metadata* from Masader, but it does not download external
training text into the corpus. Every source is classified before later import.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"
DOC = ROOT / "docs/PHASE27_109_FREE_LINGUISTIC_RESOURCE_INTAKE_GATE_REPORT.md"
MANIFEST = RESOURCES_DIR / "free_linguistic_resources_manifest.json"
MASADER_SUMMARY = RESOURCES_DIR / "masader_datasets_index_summary.json"
REPORT = REPORT_DIR / "phase27_109_free_linguistic_resource_intake_gate_report.json"
DECISION = REPORT_DIR / "PHASE27_109_FREE_LINGUISTIC_RESOURCE_INTAKE_GATE_DECISION.json"

MASADER_API = "https://api.github.com/repos/ARBML/masader/contents/datasets"


@dataclass(frozen=True)
class ResourceCandidate:
    id: str
    name: str
    url: str
    resource_type: str
    language_scope: tuple[str, ...]
    dialect_scope: tuple[str, ...]
    license: str
    cost: str
    access: str
    intended_use: str
    intake_decision: str
    training_text_allowed_now: bool
    tokenizer_vocab_allowed_now: bool
    why: str
    required_next_checks: tuple[str, ...]


CURATED_SOURCES: tuple[ResourceCandidate, ...] = (
    ResourceCandidate(
        id="qabas",
        name="Qabas Arabic Lexicographic Database",
        url="https://sina.birzeit.edu/qabas",
        resource_type="lexicon",
        language_scope=("msa",),
        dialect_scope=("msa",),
        license="open-source; verify downloadable artifact license before import",
        cost="free",
        access="web/download",
        intended_use="vocabulary/topics/protected-terms bootstrap, not pretrained tokenizer",
        intake_decision="candidate_vocabulary_and_topic_bootstrap",
        training_text_allowed_now=False,
        tokenizer_vocab_allowed_now=False,
        why="Large Arabic lexicon; useful for words and topic coverage, but direct import must preserve SF tokenizer sovereignty.",
        required_next_checks=(
            "downloadable artifact license verification",
            "field mapping audit",
            "deduplicate against Saudi Seed v1",
            "vocabulary-only import plan",
        ),
    ),
    ResourceCandidate(
        id="masader",
        name="Masader Arabic NLP Dataset Catalogue",
        url="https://github.com/ARBML/masader",
        resource_type="metadata_catalogue",
        language_scope=("ar",),
        dialect_scope=("msa", "saudi", "gulf", "mixed"),
        license="GPL-3.0 for catalogue code/metadata repository",
        cost="free",
        access="github_metadata",
        intended_use="source discovery and licensing triage only",
        intake_decision="approved_metadata_catalogue_only",
        training_text_allowed_now=False,
        tokenizer_vocab_allowed_now=False,
        why="Catalogue metadata helps find licensed resources; it is not itself dialogue training text.",
        required_next_checks=(
            "filter free/licensed text resources",
            "exclude pretrained/model-derived datasets",
            "exclude external dialogue unless license/provenance is clean",
        ),
    ),
    ResourceCandidate(
        id="tashkeela",
        name="Tashkeela Arabic Diacritized Corpus",
        url="https://sourceforge.net/projects/tashkeela/",
        resource_type="msa_diacritized_corpus",
        language_scope=("msa",),
        dialect_scope=("msa",),
        license="CC BY 4.0 per paper; verify packaged files before import",
        cost="free",
        access="download",
        intended_use="MSA orthography, diacritics, tokenizer boundary audit, possible LM pretraining after cleaning",
        intake_decision="candidate_msa_text_after_license_and_cleaning_gate",
        training_text_allowed_now=False,
        tokenizer_vocab_allowed_now=False,
        why="Large clean MSA text can improve Arabic form, but it is not conversational and must be balanced against Saudi dialogue.",
        required_next_checks=(
            "download checksum and license capture",
            "domain/source filtering",
            "deduplicate",
            "conversation-vs-text curriculum separation",
        ),
    ),
    ResourceCandidate(
        id="osian",
        name="OSIAN Arabic News Corpus",
        url="https://demo.oujda-nlp-team.net/Osian.php",
        resource_type="news_corpus",
        language_scope=("msa",),
        dialect_scope=("msa",),
        license="CC BY-NC 4.0",
        cost="free",
        access="clarin/download",
        intended_use="eval-only or non-commercial research lane unless project accepts NC restriction",
        intake_decision="restricted_noncommercial_eval_or_vocabulary_only",
        training_text_allowed_now=False,
        tokenizer_vocab_allowed_now=False,
        why="Huge MSA news corpus, but non-commercial license blocks unrestricted training use.",
        required_next_checks=("commercial-intent decision", "license compatibility review"),
    ),
    ResourceCandidate(
        id="arabic_learner_corpus",
        name="Arabic Learner Corpus",
        url="https://www.arabiclearnercorpus.com/",
        resource_type="learner_msa_corpus",
        language_scope=("msa",),
        dialect_scope=("msa",),
        license="CC BY; verify download package terms",
        cost="free",
        access="download",
        intended_use="error patterns, spelling/grammar robustness, eval probes",
        intake_decision="candidate_eval_and_error_pattern_resource",
        training_text_allowed_now=False,
        tokenizer_vocab_allowed_now=False,
        why="Useful for robustness to learner errors; not a general assistant dialogue source.",
        required_next_checks=("download terms verification", "privacy scan", "error-pattern extraction plan"),
    ),
    ResourceCandidate(
        id="fr3on_arabic_dialect_corpus",
        name="fr3on Arabic Dialect Corpus",
        url="https://huggingface.co/datasets/fr3on/arabic-dialect-corpus",
        resource_type="dialect_corpus",
        language_scope=("ar",),
        dialect_scope=("saudi", "gulf", "mixed"),
        license="MIT stated on dataset page; verify data provenance and platform terms",
        cost="free",
        access="huggingface_dataset",
        intended_use="Saudi/Gulf vocabulary discovery and dialect eval after privacy/toxicity filtering",
        intake_decision="candidate_dialect_vocab_eval_only_until_provenance_gate",
        training_text_allowed_now=False,
        tokenizer_vocab_allowed_now=False,
        why="May contain Saudi dialect text, but social-media provenance requires strict privacy/toxicity/licensing checks.",
        required_next_checks=("provenance audit", "PII/toxicity filter", "dialect label audit", "license compatibility"),
    ),
    ResourceCandidate(
        id="arsyra",
        name="ArSyra Arabic Synthetic Review / Dialect Resources",
        url="https://arsyra.com/datasets.html",
        resource_type="dialect_dataset",
        language_scope=("ar",),
        dialect_scope=("saudi", "gulf", "mixed"),
        license="mixed; CC-BY-NC-SA/free tiers and commercial options",
        cost="mixed",
        access="web",
        intended_use="blocked until license lane is explicit",
        intake_decision="blocked_until_license_lane_selected",
        training_text_allowed_now=False,
        tokenizer_vocab_allowed_now=False,
        why="Potentially useful for Saudi/Gulf, but license/cost tiers are not yet compatible with unrestricted training.",
        required_next_checks=("license selection", "commercial permission if needed"),
    ),
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 27.109 free resource intake gate")
    parser.add_argument(
        "--fetch-masader",
        action="store_true",
        help="Fetch public Masader dataset metadata summary from GitHub API.",
    )
    return parser.parse_args(argv)


def _fetch_json(url: str) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": "SF.AI local resource intake"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _summarize_masader() -> dict[str, Any]:
    raw = _fetch_json(MASADER_API)
    files = [
        {
            "name": item.get("name"),
            "path": item.get("path"),
            "size": item.get("size"),
            "download_url": item.get("download_url"),
            "html_url": item.get("html_url"),
        }
        for item in raw
        if item.get("type") == "file" and str(item.get("name", "")).endswith(".json")
    ]
    candidate_terms = (
        "saudi",
        "gulf",
        "dialect",
        "conversation",
        "chat",
        "review",
        "tashkeela",
        "qabas",
        "arabic",
        "wikipedia",
        "osian",
    )
    candidates = [
        item
        for item in files
        if any(term in str(item["name"]).lower() for term in candidate_terms)
    ][:80]
    return {
        "source": MASADER_API,
        "fetched": True,
        "file_count": len(files),
        "candidate_preview_count": len(candidates),
        "candidate_preview": candidates,
        "note": "Metadata only. No external training text was imported.",
    }


def _offline_masader_summary() -> dict[str, Any]:
    return {
        "source": MASADER_API,
        "fetched": False,
        "file_count": None,
        "candidate_preview_count": 0,
        "candidate_preview": [],
        "note": "Run with --fetch-masader to refresh public metadata summary.",
    }


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_doc(report: dict[str, Any]) -> None:
    decision = report["decision"]
    counts = report["decision_counts"]
    lines = [
        "# Phase 27.109 — Free Linguistic Resource Intake Gate",
        "",
        "## الخلاصة",
        "",
        "تم اعتماد مسار تسريع مجاني سيادي يعتمد على مصادر لغوية جاهزة، لا عقول جاهزة.",
        "",
        "القرار:",
        "",
        "```text",
        decision["decision_id"],
        "```",
        "",
        "المبدأ:",
        "",
        "- مسموح: metadata، معاجم، corpora مرخصة، أدوات تنظيف وتشخيص.",
        "- ممنوع: pretrained weights، pretrained tokenizer/vocab/merges، API خارجي.",
        "- لا يدخل أي نص خارجي إلى `data/corpus` قبل gate ترخيص وتنظيف.",
        "",
        "## المرشحون",
        "",
        "```json",
        json.dumps(counts, ensure_ascii=False, indent=2),
        "```",
        "",
        "## الأفضل الآن",
        "",
        "1. Masader: فهرس مجاني لاكتشاف المصادر وتصنيف الترخيص.",
        "2. Qabas: معجم عربي كبير للموضوعات والكلمات المحمية.",
        "3. Tashkeela: فصحى مشكولة لتحسين orthography/tokenization بعد تنظيف.",
        "4. مصادر اللهجة السعودية: لا تدخل إلا بعد provenance/privacy/license gate.",
        "",
        "## التالي",
        "",
        "```text",
        decision["next_phase"],
        "```",
        "",
    ]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text("\n".join(lines), encoding="utf-8")


def build_report(*, fetch_masader: bool) -> dict[str, Any]:
    resources = [asdict(source) for source in CURATED_SOURCES]
    decision_counts = Counter(source.intake_decision for source in CURATED_SOURCES)
    ready_for_next = bool(
        any(source.id == "masader" for source in CURATED_SOURCES)
        and any(source.id == "qabas" for source in CURATED_SOURCES)
        and all(not source.training_text_allowed_now for source in CURATED_SOURCES)
        and all(not source.tokenizer_vocab_allowed_now for source in CURATED_SOURCES)
    )
    masader_summary = _summarize_masader() if fetch_masader else _offline_masader_summary()
    decision = {
        "decision_id": "PHASE27_109_FREE_LINGUISTIC_RESOURCE_INTAKE_GATE_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_110_QABAS_MASADER_TASHKEELA_LICENSED_INGESTION_DESIGN_NO_TRAINING"
            if ready_for_next
            else "BLOCK_PHASE27_110_REPAIR_RESOURCE_INTAKE_MANIFEST"
        ),
        "metadata_fetch_allowed": True,
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "pretrained_weights_allowed": False,
        "runtime_release_allowed": False,
        "next_phase": (
            "Phase 27.110 — Qabas/Masader/Tashkeela Licensed Ingestion Design"
            if ready_for_next
            else "Phase 27.109b — Free Resource Intake Manifest Repair"
        ),
    }
    return {
        "phase": "Phase 27.109",
        "status": (
            "PHASE27_109_FREE_RESOURCE_INTAKE_READY_NO_TRAINING"
            if ready_for_next
            else "PHASE27_109_FREE_RESOURCE_INTAKE_BLOCKED"
        ),
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1 + external candidates not imported",
        "training_started": False,
        "runtime_changed": False,
        "resource_count": len(resources),
        "resources": resources,
        "decision_counts": dict(decision_counts),
        "masader_metadata_summary": masader_summary,
        "decision": decision,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_report(fetch_masader=args.fetch_masader)
    _write_json(MANIFEST, report["resources"])
    _write_json(MASADER_SUMMARY, report["masader_metadata_summary"])
    _write_json(REPORT, report)
    _write_json(DECISION, report["decision"])
    _write_doc(report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PHASE27_109_FREE_RESOURCE_INTAKE_READY_NO_TRAINING" else 1


if __name__ == "__main__":
    raise SystemExit(main())
