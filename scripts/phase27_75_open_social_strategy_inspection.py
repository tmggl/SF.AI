#!/usr/bin/env python3
"""Phase 27.75 open_social failure strategy inspection.

This phase does not train. It inspects Phase 27.74 failures, audits tokenizer
v8 around the observed fragments, and records the next strategy: tokenizer v9
open_social boundary probe before any more LM fine-tuning.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.models.tokenizer import BPETokenizer  # noqa: E402
from sf_ai.models.tokenizer.policy_audit import load_plain_terms, load_tokenization_rules  # noqa: E402


SOURCE_REPORT = ROOT / "artifacts/reports/phase27_74_open_social_semantic_collapse_repair_report.json"
TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v8_phase27_65"
RULES = ROOT / "resources/tokenization/tokenization_rules.yaml"
PROTECTED_PACK = ROOT / "resources/tokenization/protected_phrases_phase27_75.txt"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_75_open_social_strategy_inspection_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_75_open_social_strategy_inspection.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_75_OPEN_SOCIAL_STRATEGY_INSPECTION_REPORT.md"


TOKENIZATION_PROBES: tuple[tuple[str, str], ...] = (
    ("word_salfah", "سالفة"),
    ("word_bisalfah", "بسالفة"),
    ("artifact_bis_alfah", "بس الفة"),
    ("word_sawalif", "سوالف"),
    ("phrase_topic_an", "موضوعًا عن"),
    ("phrase_topic_an_plain", "موضوع عن"),
    ("artifact_topic_glue", "موضوعاموضوععن"),
    ("phrase_light_talk", "كلام خفيف"),
    ("sentence_salfah", "خلنا نبدأ بسالفة قصيرة وخفيفة"),
    ("sentence_topic", "نختار موضوعًا عن شيء خفيف"),
)


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_source() -> dict[str, Any]:
    if not SOURCE_REPORT.exists():
        raise FileNotFoundError(f"missing source report: {SOURCE_REPORT}")
    return json.loads(SOURCE_REPORT.read_text(encoding="utf-8"))


def _selected_failures(source: dict[str, Any]) -> list[dict[str, Any]]:
    return list(source["selected_candidate"].get("failures") or ())


def _failure_summary(failures: list[dict[str, Any]]) -> dict[str, Any]:
    by_family: Counter[str] = Counter(str(row["family"]) for row in failures)
    by_reason: Counter[str] = Counter(str(row["reason"]) for row in failures)
    by_guard: Counter[str] = Counter(str(row.get("guard_reason")) for row in failures)
    prompts: dict[str, list[str]] = defaultdict(list)
    for row in failures:
        prompts[str(row["prompt"])].append(str(row["response"]))
    return {
        "total": len(failures),
        "by_family": dict(by_family),
        "by_reason": dict(by_reason),
        "by_guard_reason": dict(by_guard),
        "prompt_to_responses": dict(sorted(prompts.items())),
    }


def _tokenization_rows(tokenizer: BPETokenizer) -> list[dict[str, Any]]:
    inv = {idx: tok for tok, idx in tokenizer.vocab.items()}
    rows: list[dict[str, Any]] = []
    for probe_id, text in TOKENIZATION_PROBES:
        ids = tokenizer.encode(text)
        tokens = [inv.get(idx, "<missing>") for idx in ids]
        decoded = tokenizer.decode(ids)
        rows.append(
            {
                "id": probe_id,
                "text": text,
                "piece_count": len(ids),
                "tokens": tokens,
                "decoded": decoded,
                "roundtrip_ok": decoded == text,
            }
        )
    return rows


def _protected_pack_rows(tokenizer: BPETokenizer) -> list[dict[str, Any]]:
    inv = {idx: tok for tok, idx in tokenizer.vocab.items()}
    rows: list[dict[str, Any]] = []
    for phrase in load_plain_terms(PROTECTED_PACK):
        ids = tokenizer.encode(phrase)
        rows.append(
            {
                "phrase": phrase,
                "piece_count_v8": len(ids),
                "tokens_v8": [inv.get(idx, "<missing>") for idx in ids],
                "decoded_v8": tokenizer.decode(ids),
                "roundtrip_ok_v8": tokenizer.decode(ids) == phrase,
            }
        )
    return rows


def build_report() -> dict[str, Any]:
    source = _load_source()
    tokenizer = BPETokenizer.load(TOKENIZER)
    rules = load_tokenization_rules(RULES)
    failures = _selected_failures(source)
    token_rows = _tokenization_rows(tokenizer)
    protected_rows = _protected_pack_rows(tokenizer)
    protected_paths = rules["protected_phrases"]["active_paths"]
    v8_roundtrip_failures = [row for row in token_rows if not row["roundtrip_ok"]]
    salfah_problem = next(row for row in token_rows if row["id"] == "word_bisalfah")
    topic_glue_problem = next(row for row in token_rows if row["id"] == "artifact_topic_glue")
    selected = source["selected_candidate"]
    return {
        "phase": "Phase 27.75",
        "name": "Open-Social Strategy Inspection",
        "status": "COMPLETED_OPEN_SOCIAL_STRATEGY_INSPECTION_RUNTIME_BLOCKED",
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": False,
        "training_scope": "no training; tokenizer and failure strategy inspection only",
        "source_report": _rel(SOURCE_REPORT),
        "tokenizer": _rel(TOKENIZER),
        "protected_pack": _rel(PROTECTED_PACK),
        "protected_pack_active_in_rules": _rel(PROTECTED_PACK) in protected_paths,
        "source_selected_candidate": {
            "candidate": selected["candidate"],
            "phase27_69": selected["phase27_69_summary"]["passed"],
            "phase27_67": selected["phase27_67_summary"]["passed"],
            "phase27_60": selected["phase27_60_summary"]["passed"],
        },
        "failure_summary": _failure_summary(failures),
        "tokenization_probes": token_rows,
        "protected_pack_v8_rows": protected_rows,
        "diagnosis": {
            "primary": "tokenizer_v8_open_social_boundary_fragments",
            "bisalfah_decodes_as": salfah_problem["decoded"],
            "topic_glue_decodes_as": topic_glue_problem["decoded"],
            "v8_roundtrip_failure_count": len(v8_roundtrip_failures),
            "why_no_more_lm_repair_now": (
                "Phase 27.74 already showed that more LM pressure on the same "
                "tokenizer reproduces fragments; fix token boundaries first."
            ),
        },
        "decisions": {
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
            "training_allowed_next": True,
            "tokenizer_v9_required_next": True,
            "lm_repair_allowed_before_tokenizer_v9": False,
            "repair_required_before_runtime": True,
        },
        "decision": (
            "Keep runtime blocked. Do not repeat LM-only open_social repair on "
            "tokenizer v8. Promote the Phase 27.75 protected open_social phrases "
            "into a tokenizer v9 boundary probe, then re-run bounded alignment."
        ),
        "next_phase": (
            "Phase 27.76 — tokenizer v9 open_social boundary probe before LM repair"
        ),
    }


def _write_json(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_samples(path: Path, report: dict[str, Any]) -> None:
    lines = ["# Phase 27.75 Open-Social Strategy Inspection", ""]
    lines.extend(
        [
            f"- selected candidate: `{report['source_selected_candidate']['candidate']}`",
            f"- failure total: `{report['failure_summary']['total']}`",
            f"- protected pack active: `{report['protected_pack_active_in_rules']}`",
            f"- next: {report['next_phase']}",
            "",
            "## Tokenization Probes",
            "",
        ]
    )
    for row in report["tokenization_probes"]:
        lines.extend(
            [
                f"### {row['id']}",
                "",
                f"- text: {row['text']}",
                f"- decoded: {row['decoded']}",
                f"- piece_count: `{row['piece_count']}`",
                f"- roundtrip_ok: `{row['roundtrip_ok']}`",
                f"- tokens: `{row['tokens']}`",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    diagnosis = report["diagnosis"]
    lines = [
        "# Phase 27.75 — Open-Social Strategy Inspection",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة فحص استراتيجية فقط. لم يبدأ تدريب جديد.",
        "",
        f"- status: `{report['status']}`",
        f"- source: `{report['source_report']}`",
        f"- tokenizer: `{report['tokenizer']}`",
        f"- protected pack: `{report['protected_pack']}`",
        f"- protected pack active: `{report['protected_pack_active_in_rules']}`",
        f"- runtime switch allowed: `{report['decisions']['runtime_switch_allowed']}`",
        "",
        "## التشخيص",
        "",
        f"- primary: `{diagnosis['primary']}`",
        f"- `بسالفة` decodes as: `{diagnosis['bisalfah_decodes_as']}`",
        f"- `موضوعاموضوععن` decodes as: `{diagnosis['topic_glue_decodes_as']}`",
        f"- v8 roundtrip failures: `{diagnosis['v8_roundtrip_failure_count']}`",
        "",
        "## القرار",
        "",
        report["decision"],
        "",
        "## التالي",
        "",
        report["next_phase"],
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    report = build_report()
    _write_json(DEFAULT_REPORT, report)
    _write_samples(DEFAULT_SAMPLES, report)
    _write_doc(DEFAULT_DOC, report)
    print("SF.AI — Phase 27.75 open_social strategy inspection")
    print(f"  status      : {report['status']}")
    print(f"  failures    : {report['failure_summary']['total']}")
    print(f"  tokenizer   : {report['tokenizer']}")
    print(f"  protected   : {report['protected_pack']}")
    print(f"  runtime     : blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
