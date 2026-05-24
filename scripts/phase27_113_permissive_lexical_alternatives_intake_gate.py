#!/usr/bin/env python3
"""Phase 27.113 — permissive lexical alternatives intake gate, no training.

Qabas is reference-only after Phase 27.112. This phase searches for safer
lexical alternatives and classifies them by license/provenance without
importing entries into corpus, tokenizer, or runtime.
"""

from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"

MANIFEST = RESOURCE_DIR / "phase27_113_permissive_lexical_alternatives_manifest.json"
EVIDENCE = RESOURCE_DIR / "phase27_113_lexical_alternatives_evidence.json"
REPORT = REPORT_DIR / "phase27_113_permissive_lexical_alternatives_intake_gate_report.json"
DECISION = REPORT_DIR / "PHASE27_113_PERMISSIVE_LEXICAL_ALTERNATIVES_INTAKE_GATE_DECISION.json"
DOC = ROOT / "docs/PHASE27_113_PERMISSIVE_LEXICAL_ALTERNATIVES_INTAKE_GATE_REPORT.md"

SINALAB_RESOURCES = "https://sina.birzeit.edu/resources/"
LINGUIST_AWN4 = "https://linguistlist.org/issues/37/321/"
OMW_V1 = "https://omwn.org/omw1.html"
SALMA_HF = "https://huggingface.co/datasets/SinaLab/SALMA-Arabic_Sense_Annotated_Corpus/tree/main"


@dataclass(frozen=True)
class Candidate:
    source_id: str
    name: str
    url: str
    source_type: str
    observed_license: str
    primary_signal: str
    lane: str
    decision: str
    lexical_import_allowed_next: bool
    training_text_allowed_next: bool
    tokenizer_vocab_allowed_next: bool
    eval_allowed_next: bool
    why: str
    required_gates: tuple[str, ...]


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "SF.AI local lexical intake"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def _strip_html(text: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _snippet(text: str, needle: str, *, window: int = 180) -> str:
    clean = _strip_html(text)
    idx = clean.lower().find(needle.lower())
    if idx < 0:
        return ""
    return clean[max(0, idx - window) : min(len(clean), idx + len(needle) + window)]


def _build_evidence() -> dict[str, Any]:
    sinalab = _fetch_text(SINALAB_RESOURCES)
    linguist = _fetch_text(LINGUIST_AWN4)
    omw = _fetch_text(OMW_V1)
    salma = _fetch_text(SALMA_HF)
    return {
        "sources": [
            {
                "id": "sinalab_resources",
                "url": SINALAB_RESOURCES,
                "snippets": {
                    "arabic_ontology": _snippet(sinalab, "Arabic Ontology"),
                    "salma_wsd": _snippet(sinalab, "Salma WSD"),
                    "synonyms": _snippet(sinalab, "Synonyms dataset"),
                    "qabas_reference_block": _snippet(sinalab, "Qabas Lexicon"),
                },
            },
            {
                "id": "arabic_wordnet_v4_linguist",
                "url": LINGUIST_AWN4,
                "snippets": {
                    "license": _snippet(linguist, "CC BY 4.0"),
                    "methodology": _snippet(linguist, "using Gemini 3 Pro Preview"),
                },
            },
            {
                "id": "omw_v1",
                "url": OMW_V1,
                "snippets": {
                    "redistribution": _snippet(omw, "license that allows redistribution"),
                    "arabic_awn_v2": _snippet(omw, "Arabic WordNet (AWN v2)"),
                },
            },
            {
                "id": "salma_huggingface",
                "url": SALMA_HF,
                "snippets": {
                    "license": _snippet(salma, "cc-by-4.0"),
                },
            },
        ],
    }


def _candidates() -> list[Candidate]:
    return [
        Candidate(
            source_id="arabic_ontology",
            name="Arabic Ontology",
            url=SINALAB_RESOURCES,
            source_type="ontology_lexical_semantics",
            observed_license="CC-BY-4.0",
            primary_signal="SinaLab resources listing marks Arabic Ontology as CC-BY-4.0.",
            lane="permissive_candidate_metadata_only",
            decision="allow_phase27_114_source_card_and_license_matrix_no_import",
            lexical_import_allowed_next=False,
            training_text_allowed_next=False,
            tokenizer_vocab_allowed_next=False,
            eval_allowed_next=True,
            why="Potentially useful for concept/topic coverage, but needs a source card and artifact license capture first.",
            required_gates=(
                "capture_primary_download_license",
                "artifact_checksum",
                "field_mapping_design",
                "no_tokenizer_vocab_import",
                "dedupe_against_saudi_seed_v1",
            ),
        ),
        Candidate(
            source_id="sinalab_synonyms",
            name="SinaLab Arabic Synonyms Dataset",
            url=SINALAB_RESOURCES,
            source_type="synonym_dataset",
            observed_license="CC-BY-4.0",
            primary_signal="SinaLab resources listing marks Synonyms dataset as CC-BY-4.0.",
            lane="permissive_candidate_metadata_only",
            decision="allow_phase27_114_source_card_and_license_matrix_no_import",
            lexical_import_allowed_next=False,
            training_text_allowed_next=False,
            tokenizer_vocab_allowed_next=False,
            eval_allowed_next=True,
            why="Good candidate for semantic alternatives/eval; still not dialogue corpus and not tokenizer vocab.",
            required_gates=(
                "capture_primary_download_license",
                "artifact_checksum",
                "separate_synonym_eval_from_training",
                "no_template_masking",
            ),
        ),
        Candidate(
            source_id="salma_wsd",
            name="SALMA Arabic Sense Annotated Corpus",
            url=SALMA_HF,
            source_type="sense_annotated_corpus",
            observed_license="CC-BY-4.0",
            primary_signal="SinaLab/HuggingFace pages show CC-BY-4.0.",
            lane="eval_candidate_not_lexicon",
            decision="eval_only_until_text_lane_gate",
            lexical_import_allowed_next=False,
            training_text_allowed_next=False,
            tokenizer_vocab_allowed_next=False,
            eval_allowed_next=True,
            why="Useful for WSD/eval, but it is text/corpus-like and must not enter dialogue training here.",
            required_gates=(
                "text_lane_separation",
                "privacy_and_quality_sample",
                "no_dialogue_corpus_contamination",
            ),
        ),
        Candidate(
            source_id="arabic_wordnet_v4",
            name="Arabic WordNet 4.0",
            url=LINGUIST_AWN4,
            source_type="wordnet",
            observed_license="CC-BY-4.0",
            primary_signal="LINGUIST announcement says CC-BY-4.0, but methodology says Gemini 3 Pro Preview.",
            lane="blocked_model_derived",
            decision="block_import_due_to_external_model_derived_content",
            lexical_import_allowed_next=False,
            training_text_allowed_next=False,
            tokenizer_vocab_allowed_next=False,
            eval_allowed_next=False,
            why="Large and permissively licensed, but generated through external AI, so it conflicts with SF-native data purity.",
            required_gates=("do_not_import_into_sf_native_brain", "reference_only_if_needed"),
        ),
        Candidate(
            source_id="omw_arabic_wordnet_v2",
            name="Open Multilingual Wordnet Arabic WordNet v2",
            url=OMW_V1,
            source_type="wordnet",
            observed_license="CC-BY-SA-3.0",
            primary_signal="OMW lists Arabic WordNet v2 as CC BY SA 3.0.",
            lane="restricted_sharealike",
            decision="reference_or_eval_only_until_sharealike_policy",
            lexical_import_allowed_next=False,
            training_text_allowed_next=False,
            tokenizer_vocab_allowed_next=False,
            eval_allowed_next=True,
            why="Redistributable, but share-alike is not clean enough for unrestricted SF lexicon import.",
            required_gates=("sharealike_policy_decision", "license_compatibility_review"),
        ),
        Candidate(
            source_id="qabas",
            name="Qabas Lexicon",
            url="https://sina.birzeit.edu/qabas",
            source_type="lexicon",
            observed_license="CC-BY-ND-4.0 primary signal",
            primary_signal="Phase 27.112 resolved Qabas as reference-only.",
            lane="reference_only",
            decision="blocked_from_import_use_only_for_discovery",
            lexical_import_allowed_next=False,
            training_text_allowed_next=False,
            tokenizer_vocab_allowed_next=False,
            eval_allowed_next=False,
            why="No-derivatives and conflicting metadata block raw entries and derived candidate terms.",
            required_gates=("do_not_import",),
        ),
    ]


def _build_decision(rows: list[dict[str, Any]]) -> dict[str, Any]:
    allowed_source_cards = [
        row["source_id"]
        for row in rows
        if row["decision"] == "allow_phase27_114_source_card_and_license_matrix_no_import"
    ]
    return {
        "decision_id": "PHASE27_113_PERMISSIVE_LEXICAL_ALTERNATIVES_INTAKE_GATE_DECISION",
        "engineering_decision": "ALLOW_PHASE27_114_SOURCE_CARDS_FOR_ARABIC_ONTOLOGY_AND_SYNONYMS_NO_IMPORT",
        "allowed_source_card_candidates": allowed_source_cards,
        "qabas_import_allowed": False,
        "arabic_wordnet_v4_import_allowed": False,
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "next_phase": "Phase 27.114 — Arabic Ontology/Synonyms Source Cards and License Matrix, no training",
    }


def _write_doc(report: dict[str, Any]) -> None:
    decision = report["decision"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.113 — Permissive Lexical Alternatives Intake Gate",
                "",
                "## الخلاصة",
                "",
                "بعد حجب Qabas، صُنفت بدائل lexical مرخصة أو محتملة بدون أي import.",
                "",
                "## القرار",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## المرشحون المسموحون للمرحلة التالية فقط",
                "",
                "- `arabic_ontology`: source card/license matrix فقط.",
                "- `sinalab_synonyms`: source card/license matrix فقط.",
                "",
                "## المحجوب أو المقيد",
                "",
                "- `qabas`: reference-only بسبب `CC-BY-ND-4.0`.",
                "- `arabic_wordnet_v4`: محجوب لأنه model-derived عبر Gemini رغم CC-BY-4.0.",
                "- `omw_arabic_wordnet_v2`: مقيد ShareAlike.",
                "- `salma_wsd`: eval/text-lane فقط، وليس lexicon import.",
                "",
                "## الممنوع",
                "",
                "- لا corpus.",
                "- لا tokenizer vocab أو merges.",
                "- لا تدريب.",
                "- لا runtime release.",
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


def build_report() -> dict[str, Any]:
    evidence = _build_evidence()
    rows = [asdict(candidate) for candidate in _candidates()]
    decision = _build_decision(rows)
    report = {
        "phase": "Phase 27.113",
        "status": "PHASE27_113_PERMISSIVE_LEXICAL_ALTERNATIVES_READY_NO_IMPORT",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "evidence": evidence,
        "candidates": rows,
        "decision": decision,
        "training_started": False,
        "runtime_changed": False,
        "external_entries_imported": False,
    }
    _write_json(EVIDENCE, evidence)
    _write_json(MANIFEST, rows)
    _write_json(REPORT, report)
    _write_json(DECISION, decision)
    _write_doc(report)
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PHASE27_113_PERMISSIVE_LEXICAL_ALTERNATIVES_READY_NO_IMPORT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
