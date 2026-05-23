#!/usr/bin/env python3
"""Phase 27.20 tokenizer/protected-phrase strategy.

This phase does not enable runtime generation and does not train a larger LM.
It proves the tokenizer can preserve diagnostic failure phrases as explicit
policy-owned units before a future tokenizer v3 + SF-10M retrain.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sf_ai.models.tokenizer import BPETokenizer, TokenizerConfig
from sf_ai.models.tokenizer.policy_audit import load_plain_terms


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v2"
DEFAULT_PHRASES = ROOT / "resources/tokenization/protected_phrases_phase27_20.txt"
DEFAULT_HYGIENE_REPORT = ROOT / "artifacts/reports/phase27_18_tokenization_hygiene_report.json"
DEFAULT_CORPUS = ROOT / "data/corpus/chat/jsonl"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_20_tokenizer_strategy_report.json"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 27.20 tokenizer strategy audit")
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--phrases", type=Path, default=DEFAULT_PHRASES)
    p.add_argument("--hygiene-report", type=Path, default=DEFAULT_HYGIENE_REPORT)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return p.parse_args()


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _corpus_hits(corpus_root: Path, phrase: str) -> int:
    hits = 0
    for path in sorted(corpus_root.glob("*.jsonl")):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        hits += text.count(phrase)
    return hits


def _piece_row(tokenizer: BPETokenizer, phrase: str) -> dict[str, Any]:
    ids = tokenizer.encode(phrase)
    decoded = tokenizer.decode(ids)
    return {
        "phrase": phrase,
        "piece_count": len(ids),
        "token_ids": ids,
        "decoded": decoded,
        "roundtrip_ok": decoded == phrase,
    }


def _build_strategy_tokenizer(phrases: list[str]) -> BPETokenizer:
    tok = BPETokenizer(
        TokenizerConfig(
            vocab_size=512,
            min_frequency=1,
            protected_terms=tuple(phrases),
        )
    )
    # Diagnostic-only training text. These phrases are project-authored policy
    # terms from SF.AI failure reports, not imported or external corpus.
    tok.train(phrases + phrases)
    return tok


def build_report(
    *,
    tokenizer_path: Path = DEFAULT_TOKENIZER,
    phrases_path: Path = DEFAULT_PHRASES,
    hygiene_report_path: Path = DEFAULT_HYGIENE_REPORT,
    corpus_root: Path = DEFAULT_CORPUS,
) -> dict[str, Any]:
    phrases = load_plain_terms(phrases_path)
    current = BPETokenizer.load(tokenizer_path)
    current_rows = [_piece_row(current, phrase) for phrase in phrases]

    strategy_tokenizer = _build_strategy_tokenizer(phrases)
    strategy_rows = [_piece_row(strategy_tokenizer, phrase) for phrase in phrases]

    hygiene_report = _load_json(hygiene_report_path)
    hygiene_focus = list(hygiene_report.get("aggressive_split_terms") or [])
    missing_from_policy = [term for term in hygiene_focus if term not in phrases]
    unexpected_policy = [term for term in phrases if term not in hygiene_focus]
    corpus_coverage = {
        phrase: _corpus_hits(corpus_root, phrase)
        for phrase in phrases
    }

    current_max = max((row["piece_count"] for row in current_rows), default=0)
    strategy_max = max((row["piece_count"] for row in strategy_rows), default=0)
    strategy_single_piece = all(row["piece_count"] == 1 for row in strategy_rows)
    strategy_roundtrip = all(row["roundtrip_ok"] for row in strategy_rows)
    policy_matches_hygiene = not missing_from_policy and not unexpected_policy

    status = (
        "COMPLETED_PROTECTED_PHRASE_STRATEGY_READY_FOR_TOKENIZER_V3"
        if strategy_single_piece and strategy_roundtrip and policy_matches_hygiene
        else "NEEDS_REVIEW_BEFORE_TOKENIZER_V3"
    )

    return {
        "phase": "Phase 27.20",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "tokenizer_current": _rel(tokenizer_path),
        "protected_phrases_path": _rel(phrases_path),
        "hygiene_report_path": _rel(hygiene_report_path),
        "protected_phrases_total": len(phrases),
        "protected_phrases": phrases,
        "hygiene_focus_terms": hygiene_focus,
        "missing_from_policy": missing_from_policy,
        "unexpected_policy_terms": unexpected_policy,
        "corpus_coverage": corpus_coverage,
        "current_v2_behavior": {
            "max_pieces": current_max,
            "rows": current_rows,
        },
        "protected_phrase_strategy_behavior": {
            "max_pieces": strategy_max,
            "all_single_piece": strategy_single_piece,
            "all_roundtrip_ok": strategy_roundtrip,
            "rows": strategy_rows,
        },
        "sovereignty": {
            "external_llm_api_used": False,
            "pretrained_weights_used": False,
            "pretrained_embeddings_used": False,
            "pretrained_tokenizer_used": False,
            "pretrained_vocab_used": False,
            "policy_terms_from_sf_ai_diagnostics": True,
        },
        "runtime_allowed": False,
        "sf50m_allowed": False,
        "decision": (
            "Protected-phrase tokenizer support is now implemented. Next: train "
            "a tokenizer v3 artifact with these policy phrases, then rerun the "
            "Phase 27.17/27.19 micro-probe before any runtime or SF-50M scaling."
        ),
        "next_phase": "Phase 27.21 — Tokenizer v3 protected-phrase retrain + micro-probe",
    }


def main() -> int:
    args = parse_args()
    report = build_report(
        tokenizer_path=args.tokenizer,
        phrases_path=args.phrases,
        hygiene_report_path=args.hygiene_report,
        corpus_root=args.corpus,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("SF.AI — Phase 27.20 tokenizer/protected-phrase strategy")
    print(f"  status                    : {report['status']}")
    print(f"  protected_phrases_total   : {report['protected_phrases_total']}")
    print(
        "  current_v2_max_pieces     : "
        f"{report['current_v2_behavior']['max_pieces']}"
    )
    print(
        "  strategy_max_pieces       : "
        f"{report['protected_phrase_strategy_behavior']['max_pieces']}"
    )
    print(f"  runtime_allowed           : {str(report['runtime_allowed']).lower()}")
    print(f"  sf50m_allowed             : {str(report['sf50m_allowed']).lower()}")
    print(f"  report                    : {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
