#!/usr/bin/env python3
"""Phase 27.65 tokenizer v8 topic-protection probe.

This phase trains a tokenizer only. It does not train or run an LM.

Phase 27.64 proved that tokenizer v7 regressed `التعاون` and `الاحترام`
from single-piece protected terms into multi-piece terms. This phase trains
tokenizer v8 with the Phase 27.64 protected topic pack and runs a bounded
topic-tokenization probe before any model repair is allowed.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase27_26_heldout_objective_repair import _rel  # noqa: E402
from sf_ai.models.tokenizer import BPETokenizer, TokenizerConfig, train_bpe_from_corpus  # noqa: E402
from sf_ai.models.tokenizer.policy_audit import load_plain_terms, load_tokenization_rules  # noqa: E402


DEFAULT_CORPUS = ROOT / "data/corpus/chat/jsonl"
DEFAULT_TOKENIZER_OUT = ROOT / "artifacts/tokenizers/sf_bpe/v8_phase27_65"
DEFAULT_PHASE27_64_REPORT = ROOT / "artifacts/reports/phase27_64_topic_lexical_tokenizer_inspection_report.json"
DEFAULT_RULES = ROOT / "resources/tokenization/tokenization_rules.yaml"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_65_tokenizer_v8_topic_probe_report.json"
DEFAULT_DOC = ROOT / "docs/PHASE27_65_TOKENIZER_V8_TOPIC_PROBE_REPORT.md"

TOPIC_TERMS: tuple[str, ...] = (
    "التعاون",
    "الاحترام",
    "الصبر",
    "الوفاء",
    "الصداقة",
    "الشجاعة",
    "الصدق",
    "الهدوء",
)
CRITICAL_TERMS: tuple[str, ...] = ("التعاون", "الاحترام")
BOUNDARY_PROBES: tuple[str, ...] = (
    "وش معنى التعاون",
    "التعاون يعني نساعد بعض وننجز سوا.",
    "ما معنى الاحترام",
    "الاحترام يعني تقدير الناس بالكلام والتصرف.",
    "الاحترام وش هو",
    "ما المقصود بالتعاون",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train tokenizer v8 and run bounded topic-tokenization probe")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--tokenizer-out", type=Path, default=DEFAULT_TOKENIZER_OUT)
    parser.add_argument("--phase27-64-report", type=Path, default=DEFAULT_PHASE27_64_REPORT)
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    parser.add_argument("--vocab-size", type=int, default=9000)
    parser.add_argument("--min-frequency", type=int, default=2)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--reuse-existing", action="store_true")
    return parser.parse_args()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _policy_terms(rules_path: Path) -> list[str]:
    rules = load_tokenization_rules(rules_path)
    paths: list[str] = []
    for section in ("protected_terms", "protected_phrases"):
        raw = rules.get(section) or {}
        paths.extend(str(path) for path in raw.get("active_paths", ()))
    terms: list[str] = []
    seen: set[str] = set()
    for raw_path in paths:
        path = ROOT / raw_path
        for term in load_plain_terms(path):
            if term not in seen:
                seen.add(term)
                terms.append(term)
    return terms


def _extra_texts(terms: list[str]) -> list[str]:
    topic_examples = [
        "التعاون يعني نساعد بعض وننجز سوا.",
        "الاحترام يعني تقدير الناس بالكلام والتصرف.",
        "الصبر ثبات وهدوء وقت الصعوبة.",
        "الوفاء حفظ للعهد وثبات في الود.",
        "الصداقة رفقة طيبة واهتمام وقت الحاجة.",
        "الشجاعة فعل الصواب مع وجود الخوف.",
        "الصدق أن تقول الحقيقة وتلتزم بها.",
        "الهدوء سكينة تساعدك على التفكير بوضوح.",
    ]
    # Repeat policy terms and topic examples so protected vocabulary stays
    # present even if corpus frequency shifts. These are project-authored terms.
    return [*terms, *terms, *terms, *topic_examples, *topic_examples]


def _tokenizer_row(tokenizer: BPETokenizer, term: str) -> dict[str, Any]:
    ids = tokenizer.encode(term)
    decoded = tokenizer.decode(ids)
    meta_protected = set(str(x) for x in tokenizer.config.protected_terms)
    return {
        "term": term,
        "piece_count": len(ids),
        "ids": ids,
        "decoded": decoded,
        "roundtrip_ok": decoded == term,
        "protected_in_config": term in meta_protected,
        "single_piece": len(ids) == 1,
    }


def _boundary_row(tokenizer: BPETokenizer, text: str) -> dict[str, Any]:
    ids = tokenizer.encode(text)
    decoded = tokenizer.decode(ids)
    contains_critical = [term for term in CRITICAL_TERMS if term in text]
    critical_piece_counts = {
        term: len(tokenizer.encode(term))
        for term in contains_critical
    }
    return {
        "text": text,
        "piece_count": len(ids),
        "decoded": decoded,
        "roundtrip_ok": decoded == text,
        "critical_terms": contains_critical,
        "critical_piece_counts": critical_piece_counts,
    }


def _train_or_load(args: argparse.Namespace, terms: list[str]) -> BPETokenizer:
    if args.reuse_existing and (args.tokenizer_out / "meta.json").exists():
        return BPETokenizer.load(args.tokenizer_out)
    if args.tokenizer_out.exists():
        shutil.rmtree(args.tokenizer_out)
    cfg = TokenizerConfig(
        vocab_size=args.vocab_size,
        min_frequency=args.min_frequency,
        protected_terms=tuple(terms),
    )
    return train_bpe_from_corpus(
        corpus_root=args.corpus,
        output_dir=args.tokenizer_out,
        config=cfg,
        extra_texts=_extra_texts(terms),
        name="sf_bpe_v8_phase27_65_topic_protected",
    )


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    if not args.phase27_64_report.exists():
        raise FileNotFoundError(args.phase27_64_report)
    p2764 = _load_json(args.phase27_64_report)
    terms = _policy_terms(args.rules)
    tokenizer = _train_or_load(args, terms)
    topic_rows = [_tokenizer_row(tokenizer, term) for term in TOPIC_TERMS]
    critical_rows = {
        row["term"]: row
        for row in topic_rows
        if row["term"] in CRITICAL_TERMS
    }
    boundary_rows = [_boundary_row(tokenizer, text) for text in BOUNDARY_PROBES]
    critical_pass = all(
        row["single_piece"] and row["roundtrip_ok"] and row["protected_in_config"]
        for row in critical_rows.values()
    )
    topic_pass = all(row["single_piece"] and row["roundtrip_ok"] for row in topic_rows)
    boundary_pass = all(row["roundtrip_ok"] for row in boundary_rows)
    passed = critical_pass and topic_pass and boundary_pass
    status = (
        "PASSED_TOKENIZER_V8_TOPIC_PROBE_READY_FOR_BOUNDED_LM_TOPIC_REPAIR_RUNTIME_BLOCKED"
        if passed
        else "FAILED_TOKENIZER_V8_TOPIC_PROBE_RUNTIME_BLOCKED"
    )
    meta = _load_json(args.tokenizer_out / "meta.json")
    return {
        "phase": "Phase 27.65",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "tokenizer-only v8 training; no LM training; no runtime switch",
        "lm_training_started": False,
        "tokenizer": _rel(args.tokenizer_out),
        "tokenizer_vocab_size": meta["vocab_size"],
        "tokenizer_merges": meta["merges"],
        "protected_terms_total": len(terms),
        "phase27_64_status": p2764["status"],
        "topic_rows": topic_rows,
        "critical_rows": critical_rows,
        "boundary_rows": boundary_rows,
        "summary": {
            "topic_terms_single_piece": sum(1 for row in topic_rows if row["single_piece"]),
            "topic_terms_total": len(topic_rows),
            "critical_terms_single_piece": sum(1 for row in critical_rows.values() if row["single_piece"]),
            "critical_terms_total": len(critical_rows),
            "boundary_roundtrip_passed": sum(1 for row in boundary_rows if row["roundtrip_ok"]),
            "boundary_roundtrip_total": len(boundary_rows),
            "avg_topic_piece_count": round(mean(row["piece_count"] for row in topic_rows), 4),
        },
        "decisions": {
            "tokenizer_v8_passed": passed,
            "bounded_lm_topic_repair_allowed_next": passed,
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
        },
        "decision": (
            "Tokenizer v8 passed bounded topic protection. Next phase may train a bounded LM topic repair only."
            if passed
            else "Tokenizer v8 did not pass topic protection. Fix tokenizer policy before any LM repair."
        ),
        "next_phase": (
            "Phase 27.66 — bounded LM topic repair on tokenizer v8, then broader canary"
            if passed
            else "Repeat tokenizer v8 policy repair before LM training"
        ),
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    summary = report["summary"]
    lines = [
        "# Phase 27.65 — Tokenizer v8 Topic Probe",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة tokenizer فقط. لا تدريب LM ولا فتح واجهة.",
        "",
        f"- status: `{report['status']}`",
        f"- tokenizer: `{report['tokenizer']}`",
        f"- vocab: `{report['tokenizer_vocab_size']}`",
        f"- protected terms: `{report['protected_terms_total']}`",
        f"- critical single-piece: `{summary['critical_terms_single_piece']}/{summary['critical_terms_total']}`",
        f"- topic single-piece: `{summary['topic_terms_single_piece']}/{summary['topic_terms_total']}`",
        f"- boundary roundtrip: `{summary['boundary_roundtrip_passed']}/{summary['boundary_roundtrip_total']}`",
        "",
        "## المصطلحات الحرجة",
        "",
    ]
    for term, row in report["critical_rows"].items():
        lines.append(
            f"- `{term}`: pieces=`{row['piece_count']}`, protected=`{row['protected_in_config']}`, roundtrip=`{row['roundtrip_ok']}`"
        )
    lines.extend(
        [
            "",
            "## القرار",
            "",
            report["decision"],
            "",
            "## التالي",
            "",
            report["next_phase"],
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    report = build_report(args)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_doc(report, args.doc)
    summary = report["summary"]
    print("SF.AI — Phase 27.65 tokenizer v8 topic probe")
    print(f"  status       : {report['status']}")
    print(f"  tokenizer    : {report['tokenizer']}")
    print(f"  critical     : {summary['critical_terms_single_piece']}/{summary['critical_terms_total']}")
    print(f"  topic terms  : {summary['topic_terms_single_piece']}/{summary['topic_terms_total']}")
    print(f"  boundary     : {summary['boundary_roundtrip_passed']}/{summary['boundary_roundtrip_total']}")
    print(f"  next allowed : {report['decisions']['bounded_lm_topic_repair_allowed_next']}")
    print(f"  report       : {_rel(args.report)}")
    print(f"  doc          : {_rel(args.doc)}")
    print("  runtime      : blocked")
    return 0 if report["status"].startswith("PASSED") else 2


if __name__ == "__main__":
    raise SystemExit(main())
