#!/usr/bin/env python3
"""Phase 27.76 tokenizer v9 open_social boundary probe.

Tokenizer-only phase. It trains a fresh sovereign SF-BPE tokenizer with the
Phase 27.75 open_social protected pack and verifies that the boundary fragments
observed in Phase 27.74 are fixed before any new LM repair is allowed.
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
DEFAULT_TOKENIZER_OUT = ROOT / "artifacts/tokenizers/sf_bpe/v9_phase27_76"
DEFAULT_RULES = ROOT / "resources/tokenization/tokenization_rules.yaml"
DEFAULT_SOURCE_REPORT = ROOT / "artifacts/reports/phase27_75_open_social_strategy_inspection_report.json"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_76_tokenizer_v9_open_social_boundary_probe_report.json"
DEFAULT_SAMPLES = ROOT / "artifacts/samples/phase27_76_tokenizer_v9_open_social_boundary_probe.md"
DEFAULT_DOC = ROOT / "docs/PHASE27_76_TOKENIZER_V9_OPEN_SOCIAL_BOUNDARY_PROBE_REPORT.md"

OPEN_SOCIAL_PROBES: tuple[str, ...] = (
    "سالفة",
    "بسالفة",
    "السالفة",
    "سوالف",
    "سوالف بسيطة",
    "موضوع سوالف",
    "موضوعًا عن",
    "موضوع عن",
    "نختار موضوعًا",
    "نفتح موضوعًا",
    "كلام خفيف",
    "حديث خفيف",
    "سالفة خفيفة",
    "خلنا نبدأ بسالفة",
    "خلنا نبدأ بسالفة قصيرة وخفيفة",
    "نختار موضوعًا عن شيء خفيف",
    "وش نقدر نسولف عنه",
)

CRITICAL_TOPIC_TERMS: tuple[str, ...] = (
    "التعاون",
    "الاحترام",
    "الصبر",
    "الوفاء",
    "الصداقة",
    "الشجاعة",
    "الصدق",
    "الهدوء",
)

ARTIFACT_PROBES: tuple[str, ...] = (
    "بس الفة",
    "موضوعاموضوععن",
    "أكموضوع",
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Train tokenizer v9 and run open_social boundary probe")
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--tokenizer-out", type=Path, default=DEFAULT_TOKENIZER_OUT)
    p.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    p.add_argument("--source-report", type=Path, default=DEFAULT_SOURCE_REPORT)
    p.add_argument("--vocab-size", type=int, default=9500)
    p.add_argument("--min-frequency", type=int, default=2)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    p.add_argument("--reuse-existing", action="store_true")
    return p.parse_args()


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
    open_social_examples = [
        "خلنا نبدأ بسالفة قصيرة وخفيفة.",
        "أبشر، نسولف بسالفة خفيفة عن يومك.",
        "نختار موضوعًا عن شيء خفيف.",
        "نفتح موضوعًا هادئًا ونتحدث عنه ببساطة.",
        "وش نقدر نسولف عنه؟",
        "موضوع سوالف خفيف: نسولف عن يومك.",
        "هات سالفة خفيفة تمشي الوقت.",
    ]
    topic_examples = [
        "التعاون مشاركة الجهد بين الناس.",
        "الاحترام تقدير الناس بالكلام والتصرف.",
        "الصبر ثبات وهدوء وقت الصعوبة.",
        "الوفاء حفظ للعهد وثبات في الود.",
        "الصداقة رفقة طيبة واهتمام وقت الحاجة.",
        "الشجاعة فعل الصواب مع وجود الخوف.",
        "الصدق أن تقول الحقيقة وتلتزم بها.",
        "الهدوء سكينة تساعدك على التفكير بوضوح.",
    ]
    return [
        *terms,
        *terms,
        *terms,
        *open_social_examples,
        *open_social_examples,
        *open_social_examples,
        *topic_examples,
        *topic_examples,
    ]


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
        name="sf_bpe_v9_phase27_76_open_social_boundary_protected",
    )


def _row(tokenizer: BPETokenizer, text: str) -> dict[str, Any]:
    inv = {idx: tok for tok, idx in tokenizer.vocab.items()}
    ids = tokenizer.encode(text)
    decoded = tokenizer.decode(ids)
    return {
        "text": text,
        "piece_count": len(ids),
        "ids": ids,
        "tokens": [inv.get(idx, "<missing>") for idx in ids],
        "decoded": decoded,
        "roundtrip_ok": decoded == text,
        "single_piece": len(ids) == 1,
        "protected_in_config": text in set(str(x) for x in tokenizer.config.protected_terms),
    }


def _artifact_row(tokenizer: BPETokenizer, text: str) -> dict[str, Any]:
    row = _row(tokenizer, text)
    row["protected_in_config"] = text in set(str(x) for x in tokenizer.config.protected_terms)
    return row


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    if not args.source_report.exists():
        raise FileNotFoundError(args.source_report)
    source = _load_json(args.source_report)
    terms = _policy_terms(args.rules)
    tokenizer = _train_or_load(args, terms)
    meta = _load_json(args.tokenizer_out / "meta.json")
    open_rows = [_row(tokenizer, text) for text in OPEN_SOCIAL_PROBES]
    topic_rows = [_row(tokenizer, text) for text in CRITICAL_TOPIC_TERMS]
    artifact_rows = [_artifact_row(tokenizer, text) for text in ARTIFACT_PROBES]
    protected_pack = "resources/tokenization/protected_phrases_phase27_75.txt"
    protected_pack_terms = load_plain_terms(ROOT / protected_pack)
    pack_rows = [_row(tokenizer, text) for text in protected_pack_terms]
    open_pass = all(row["roundtrip_ok"] for row in open_rows)
    pack_pass = all(
        row["roundtrip_ok"] and row["single_piece"] and row["protected_in_config"]
        for row in pack_rows
    )
    topic_pass = all(row["roundtrip_ok"] and row["single_piece"] for row in topic_rows)
    critical_topic_pass = all(
        row["roundtrip_ok"] and row["single_piece"] and row["protected_in_config"]
        for row in topic_rows
        if row["text"] in {"التعاون", "الاحترام"}
    )
    artifact_policy_pass = all(not row["protected_in_config"] for row in artifact_rows)
    passed = open_pass and pack_pass and topic_pass and critical_topic_pass and artifact_policy_pass
    status = (
        "PASSED_TOKENIZER_V9_OPEN_SOCIAL_BOUNDARY_PROBE_READY_FOR_BOUNDED_LM_REPAIR_RUNTIME_BLOCKED"
        if passed
        else "FAILED_TOKENIZER_V9_OPEN_SOCIAL_BOUNDARY_PROBE_RUNTIME_BLOCKED"
    )
    return {
        "phase": "Phase 27.76",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "training_started": True,
        "training_scope": "tokenizer-only v9 training; no LM training; no runtime switch",
        "lm_training_started": False,
        "source_report": _rel(args.source_report),
        "source_status": source["status"],
        "tokenizer": _rel(args.tokenizer_out),
        "tokenizer_vocab_size": meta["vocab_size"],
        "tokenizer_merges": meta["merges"],
        "protected_terms_total": len(terms),
        "protected_pack": protected_pack,
        "open_social_rows": open_rows,
        "protected_pack_rows": pack_rows,
        "topic_rows": topic_rows,
        "artifact_rows": artifact_rows,
        "summary": {
            "open_social_roundtrip_passed": sum(1 for row in open_rows if row["roundtrip_ok"]),
            "open_social_roundtrip_total": len(open_rows),
            "protected_pack_single_piece": sum(1 for row in pack_rows if row["single_piece"]),
            "protected_pack_total": len(pack_rows),
            "topic_single_piece": sum(1 for row in topic_rows if row["single_piece"]),
            "topic_total": len(topic_rows),
            "critical_topic_protected": sum(
                1
                for row in topic_rows
                if row["text"] in {"التعاون", "الاحترام"} and row["protected_in_config"]
            ),
            "critical_topic_total": 2,
            "artifact_not_protected": sum(1 for row in artifact_rows if not row["protected_in_config"]),
            "artifact_total": len(artifact_rows),
            "avg_open_social_piece_count": round(mean(row["piece_count"] for row in open_rows), 4),
        },
        "decisions": {
            "tokenizer_v9_passed": passed,
            "bounded_lm_open_social_repair_allowed_next": passed,
            "lm_training_started": False,
            "runtime_switch_allowed": False,
            "ui_open_allowed": False,
            "sf50m_allowed": False,
            "phase28_allowed": False,
            "repair_required_before_runtime": True,
        },
        "decision": (
            "Tokenizer v9 passed open_social boundary protection. Next phase may run a bounded LM repair on tokenizer v9."
            if passed
            else "Tokenizer v9 did not pass open_social boundary protection. Fix tokenizer policy before LM repair."
        ),
        "next_phase": (
            "Phase 27.77 — bounded LM open_social repair on tokenizer v9"
            if passed
            else "Repeat tokenizer v9 policy repair before LM training"
        ),
    }


def _write_json(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_samples(path: Path, report: dict[str, Any]) -> None:
    lines = ["# Phase 27.76 Tokenizer v9 Open-Social Boundary Probe", ""]
    lines.extend(
        [
            f"- status: `{report['status']}`",
            f"- tokenizer: `{report['tokenizer']}`",
            f"- open_social roundtrip: `{report['summary']['open_social_roundtrip_passed']}/{report['summary']['open_social_roundtrip_total']}`",
            f"- protected pack single-piece: `{report['summary']['protected_pack_single_piece']}/{report['summary']['protected_pack_total']}`",
            "",
            "## Open Social Rows",
            "",
        ]
    )
    for row in report["open_social_rows"]:
        lines.extend(
            [
                f"### {row['text']}",
                "",
                f"- decoded: {row['decoded']}",
                f"- piece_count: `{row['piece_count']}`",
                f"- single_piece: `{row['single_piece']}`",
                f"- roundtrip_ok: `{row['roundtrip_ok']}`",
                f"- tokens: `{row['tokens']}`",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# Phase 27.76 — Tokenizer v9 Open-Social Boundary Probe",
        "",
        "## الخلاصة",
        "",
        "هذه مرحلة tokenizer فقط. لا تدريب LM ولا فتح واجهة.",
        "",
        f"- status: `{report['status']}`",
        f"- tokenizer: `{report['tokenizer']}`",
        f"- vocab: `{report['tokenizer_vocab_size']}`",
        f"- protected terms total: `{report['protected_terms_total']}`",
        f"- open_social roundtrip: `{summary['open_social_roundtrip_passed']}/{summary['open_social_roundtrip_total']}`",
        f"- protected pack single-piece: `{summary['protected_pack_single_piece']}/{summary['protected_pack_total']}`",
        f"- topic single-piece: `{summary['topic_single_piece']}/{summary['topic_total']}`",
        f"- critical topic protected: `{summary['critical_topic_protected']}/{summary['critical_topic_total']}`",
        f"- runtime switch allowed: `{report['decisions']['runtime_switch_allowed']}`",
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
    args = parse_args()
    report = build_report(args)
    _write_json(args.report, report)
    _write_samples(args.samples, report)
    _write_doc(args.doc, report)
    print("SF.AI — Phase 27.76 tokenizer v9 open_social boundary probe")
    print(f"  status      : {report['status']}")
    print(f"  tokenizer   : {report['tokenizer']}")
    print(f"  open_social : {report['summary']['open_social_roundtrip_passed']}/{report['summary']['open_social_roundtrip_total']}")
    print(f"  protected   : {report['summary']['protected_pack_single_piece']}/{report['summary']['protected_pack_total']}")
    print("  runtime     : blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
