#!/usr/bin/env python3
"""Phase 27.110 — licensed ingestion design for free linguistic resources.

This phase turns the Phase 27.109 candidate list into an actionable ingestion
design. It fetches selected Masader metadata files, classifies licenses, and
decides which lanes are allowed next.

No external training text is imported into data/corpus. No tokenizer vocab or
merges are imported. No training starts.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
SELECTED_DIR = RESOURCE_DIR / "selected_masader_metadata"
REPORT_DIR = ROOT / "artifacts/reports"
DESIGN = RESOURCE_DIR / "phase27_110_licensed_ingestion_design.json"
MATRIX = RESOURCE_DIR / "phase27_110_license_matrix.json"
REPORT = REPORT_DIR / "phase27_110_licensed_ingestion_design_report.json"
DECISION = REPORT_DIR / "PHASE27_110_LICENSED_INGESTION_DESIGN_DECISION.json"
DOC = ROOT / "docs/PHASE27_110_LICENSED_INGESTION_DESIGN_REPORT.md"

MASADER_RAW = "https://raw.githubusercontent.com/ARBML/masader/main/datasets/{name}"
MASADER_FILES: tuple[str, ...] = (
    "qabas.json",
    "tashkeela.json",
    "sadeed_tashkeela_arabic_diacritization_dataset.json",
    "saudi_novel_corpus.json",
    "saudinewsnet.json",
    "osian.json",
    "alc__arabic_learner_corpus.json",
    "corpora_for_egyptian_arabic_and_gulf_arabic_from_twitter.json",
    "gulf_arabic_conversational_telephone_speech,_transcripts.json",
    "open-domain_response_generation_in_arabic_dialects.json",
)


@dataclass(frozen=True)
class LicenseDecision:
    source_id: str
    masader_file: str
    name: str
    license: str
    access: str
    cost: str
    language: str
    dialect: str
    domain: Any
    volume: Any
    unit: str
    link: str
    lane: str
    decision: str
    training_text_allowed_next: bool
    vocabulary_terms_allowed_next: bool
    eval_allowed_next: bool
    why: str
    required_gates: tuple[str, ...]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build Phase 27.110 licensed ingestion design")
    p.add_argument(
        "--offline",
        action="store_true",
        help="Use previously fetched selected Masader metadata files.",
    )
    return p.parse_args(argv)


def _fetch_json(url: str) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "SF.AI local resource intake"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _load_or_fetch_selected(*, offline: bool) -> dict[str, dict[str, Any]]:
    SELECTED_DIR.mkdir(parents=True, exist_ok=True)
    out: dict[str, dict[str, Any]] = {}
    for name in MASADER_FILES:
        path = SELECTED_DIR / name
        if offline and path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
        else:
            data = _fetch_json(MASADER_RAW.format(name=name))
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        out[name] = data
    return out


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _source_id(filename: str) -> str:
    return filename.removesuffix(".json").replace("-", "_").replace(",", "").replace(" ", "_")


def _classify(filename: str, raw: dict[str, Any]) -> LicenseDecision:
    license_name = _clean(raw.get("License"))
    access = _clean(raw.get("Access"))
    cost = _clean(raw.get("Cost"))
    name = _clean(raw.get("Name"))
    lower_license = license_name.lower()
    lower_access = access.lower()
    lower_cost = cost.lower()

    lane = "blocked"
    decision = "blocked_until_license_review"
    training = False
    vocab = False
    eval_allowed = False
    why = "License/access is not suitable for immediate governed ingestion."
    gates: tuple[str, ...] = (
        "capture_source_card",
        "verify_license_from_primary_source",
        "no_pretrained_vocab_or_merges",
    )

    if filename == "qabas.json":
        lane = "lexicon_bootstrap"
        decision = "allow_vocabulary_topic_design_no_tokenizer_vocab"
        vocab = True
        eval_allowed = True
        why = (
            "Masader metadata lists Qabas as a free Apache-1.0 lexicon. Use it "
            "for topics/protected terms only; never as pretrained tokenizer vocab."
        )
        gates = (
            "capture_primary_qabas_license",
            "field_mapping_audit",
            "deduplicate_against_saudi_seed_v1",
            "protected_terms_only_no_bpe_vocab_import",
        )
    elif filename == "tashkeela.json":
        lane = "msa_text_candidate"
        decision = "block_training_until_license_conflict_resolved"
        eval_allowed = True
        why = (
            "Tashkeela is attractive for MSA, but Masader lists GPL-2.0 while the "
            "paper says CC BY 4.0. Training import waits for primary package license proof."
        )
        gates = (
            "resolve_tashkeela_license_conflict",
            "download_checksum",
            "source_cleaning_sample_audit",
            "deduplicate",
            "separate_text_lane_from_dialogue_lane",
        )
    elif "sadeed_tashkeela" in filename:
        lane = "diacritization_eval_candidate"
        decision = "eval_only_until_derivative_license_review"
        eval_allowed = True
        why = "Derivative diacritization resource; useful for eval, but not training until license chain is clear."
    elif filename in {"osian.json", "saudinewsnet.json"} or "nc" in lower_license:
        lane = "restricted_noncommercial"
        decision = "eval_or_vocabulary_only_noncommercial_restricted"
        vocab = True
        eval_allowed = True
        why = "Non-commercial/share-alike restrictions block unrestricted training use."
        gates = ("noncommercial_policy_decision", "license_compatibility_review", "no_runtime_training_import")
    elif filename == "saudi_novel_corpus.json" or "unknown" in lower_license:
        lane = "blocked_unknown_license"
        decision = "reject_training_until_license_known"
        why = "Saudi content is useful, but unknown license blocks ingestion."
    elif filename == "alc__arabic_learner_corpus.json" or "fee" in lower_access or "$" in lower_cost:
        lane = "blocked_paid_or_custom"
        decision = "reject_free_lane_with_fee_or_custom_license"
        why = "Not part of the free lane; can be reconsidered only if a paid/custom license is accepted."
    elif "mit" in lower_license or "apache" in lower_license or lower_license == "cc by":
        lane = "candidate_after_cleaning"
        decision = "candidate_after_provenance_privacy_cleaning"
        vocab = True
        eval_allowed = True
        why = "Permissive metadata signal, but raw data still needs provenance/privacy/content gates."
        gates = (
            "primary_license_capture",
            "privacy_scan",
            "toxicity_scan",
            "dialect_label_audit",
            "sample_quality_review",
        )

    return LicenseDecision(
        source_id=_source_id(filename),
        masader_file=filename,
        name=name,
        license=license_name,
        access=access,
        cost=cost,
        language=_clean(raw.get("Language")),
        dialect=_clean(raw.get("Dialect")),
        domain=raw.get("Domain"),
        volume=raw.get("Volume"),
        unit=_clean(raw.get("Unit")),
        link=_clean(raw.get("Link")),
        lane=lane,
        decision=decision,
        training_text_allowed_next=training,
        vocabulary_terms_allowed_next=vocab,
        eval_allowed_next=eval_allowed,
        why=why,
        required_gates=gates,
    )


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_doc(report: dict[str, Any]) -> None:
    decision = report["decision"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.110 — Licensed Ingestion Design",
                "",
                "## الخلاصة",
                "",
                "صُمم مسار إدخال المصادر المجانية بدون إدخال نصوص تدريب خارجية.",
                "",
                "القرار:",
                "",
                "```text",
                decision["decision_id"],
                "```",
                "",
                "## القرارات",
                "",
                "- Qabas مسموح كتصميم lexicon/topic/protected-terms فقط.",
                "- Tashkeela محجوب للتدريب حتى حل تعارض الترخيص.",
                "- Masader يبقى metadata/source-discovery فقط.",
                "- OSIAN وSaudiNewsNet مقيدان non-commercial/eval أو vocabulary-only.",
                "- أي مصدر unknown/custom/with-fee محجوب عن free lane.",
                "",
                "## الممنوع",
                "",
                "- إدخال نص خارجي إلى `data/corpus` الآن.",
                "- استيراد tokenizer vocab أو merges.",
                "- تدريب جديد أو runtime release.",
                "",
                "## التالي",
                "",
                "```text",
                decision["next_phase"],
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def build_report(*, offline: bool) -> dict[str, Any]:
    metadata = _load_or_fetch_selected(offline=offline)
    matrix = [_classify(filename, raw) for filename, raw in metadata.items()]
    rows = [asdict(row) for row in matrix]
    q_allowed = next(row for row in matrix if row.masader_file == "qabas.json")
    ready = bool(
        q_allowed.vocabulary_terms_allowed_next
        and all(not row.training_text_allowed_next for row in matrix)
        and any(row.decision == "block_training_until_license_conflict_resolved" for row in matrix)
    )
    decision = {
        "decision_id": "PHASE27_110_LICENSED_INGESTION_DESIGN_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_111_QABAS_LEXICON_BOOTSTRAP_NO_TRAINING"
            if ready
            else "BLOCK_PHASE27_111_REPAIR_LICENSED_INGESTION_DESIGN"
        ),
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "qabas_lexicon_bootstrap_design_allowed": ready,
        "tashkeela_training_allowed": False,
        "runtime_release_allowed": False,
        "new_training_allowed": False,
        "next_phase": (
            "Phase 27.111 — Qabas Lexicon Bootstrap Design, no training"
            if ready
            else "Phase 27.110b — Licensed Ingestion Design Repair"
        ),
    }
    report = {
        "phase": "Phase 27.110",
        "status": (
            "PHASE27_110_LICENSED_INGESTION_DESIGN_READY_NO_TRAINING"
            if ready
            else "PHASE27_110_LICENSED_INGESTION_DESIGN_BLOCKED"
        ),
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1 + Qabas candidate",
        "training_started": False,
        "runtime_changed": False,
        "selected_metadata_count": len(matrix),
        "selected_metadata_dir": str(SELECTED_DIR.relative_to(ROOT)),
        "license_matrix": rows,
        "decision": decision,
    }
    _write_json(DESIGN, report)
    _write_json(MATRIX, rows)
    _write_json(REPORT, report)
    _write_json(DECISION, decision)
    _write_doc(report)
    return report


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_report(offline=args.offline)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PHASE27_110_LICENSED_INGESTION_DESIGN_READY_NO_TRAINING" else 1


if __name__ == "__main__":
    raise SystemExit(main())
