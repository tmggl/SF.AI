#!/usr/bin/env python3
"""Phase 27.18 tokenization/decoding hygiene audit.

Read-only diagnostic. It inspects tokenizer behavior on terms that appeared in
Phase 27.17 prompt-answer failures and records guard fragments that must block
runtime until the model stops producing them.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sf_ai.models.tokenizer import BPETokenizer
from sf_ai.models.tokenizer.policy_audit import load_plain_terms
from sf_ai.modules.chat.generation_guard import GenerationGuard


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TERMS = ROOT / "resources/tokenization/hygiene_terms_phase27_18.txt"
DEFAULT_TOKENIZER = ROOT / "artifacts/tokenizers/sf_bpe/v2"
DEFAULT_REPORT = ROOT / "artifacts/reports/phase27_18_tokenization_hygiene_report.json"

OBSERVED_BAD_FRAGMENTS: tuple[str, ...] = (
    "وعليكأهلًا",
    "التعاعاون",
    "القراد. ءة",
    "تحتاججج",
    "ججبعيادة",
    "هوش تحتاجججبعيادة",
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase 27.18 tokenization hygiene audit")
    p.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    p.add_argument("--tokenizer", type=Path, default=DEFAULT_TOKENIZER)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--max-good-pieces", type=int, default=4)
    return p.parse_args()


def _tokenizer_meta(path: Path) -> dict[str, Any]:
    meta_path = path / "meta.json"
    return json.loads(meta_path.read_text(encoding="utf-8"))


def build_report(
    *,
    terms_path: Path = DEFAULT_TERMS,
    tokenizer_path: Path = DEFAULT_TOKENIZER,
    max_good_pieces: int = 4,
) -> dict[str, Any]:
    terms = load_plain_terms(terms_path)
    tokenizer = BPETokenizer.load(tokenizer_path)
    meta = _tokenizer_meta(tokenizer_path)

    term_rows: list[dict[str, Any]] = []
    roundtrip_failures: list[str] = []
    aggressive_split_terms: list[str] = []
    total_pieces = 0
    for term in terms:
        ids = tokenizer.encode(term)
        decoded = tokenizer.decode(ids)
        piece_count = len(ids)
        total_pieces += piece_count
        roundtrip_ok = decoded == term
        aggressive = piece_count > max_good_pieces
        if not roundtrip_ok:
            roundtrip_failures.append(term)
        if aggressive:
            aggressive_split_terms.append(term)
        term_rows.append(
            {
                "term": term,
                "piece_count": piece_count,
                "token_ids": ids,
                "decoded": decoded,
                "roundtrip_ok": roundtrip_ok,
                "aggressive_split": aggressive,
            }
        )

    guard = GenerationGuard(min_chars=4)
    fragment_rows = []
    for fragment in OBSERVED_BAD_FRAGMENTS:
        verdict = guard.inspect(fragment)
        fragment_rows.append(
            {
                "fragment": fragment,
                "guard_allowed": verdict.allowed,
                "guard_reason": verdict.reason,
            }
        )

    uncovered_fragments = [
        row["fragment"] for row in fragment_rows if row["guard_allowed"] is True
    ]
    status = (
        "COMPLETED_HYGIENE_AUDIT_WITH_BLOCKERS"
        if aggressive_split_terms or roundtrip_failures or uncovered_fragments
        else "COMPLETED_HYGIENE_AUDIT_READY_FOR_REPAIR_TRAINING"
    )

    return {
        "phase": "Phase 27.18",
        "status": status,
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1",
        "tokenizer": {
            "path": str(tokenizer_path.relative_to(ROOT)),
            "sf_origin": bool(meta.get("sf_origin")),
            "vocab_size": meta.get("vocab_size"),
            "tokenizer_type": meta.get("tokenizer_type"),
        },
        "terms_path": str(terms_path.relative_to(ROOT)),
        "terms_total": len(terms),
        "max_good_pieces": max_good_pieces,
        "average_pieces": round(total_pieces / max(1, len(terms)), 4),
        "roundtrip_failures": roundtrip_failures,
        "aggressive_split_terms": aggressive_split_terms,
        "observed_bad_fragments": fragment_rows,
        "uncovered_bad_fragments": uncovered_fragments,
        "runtime_allowed": False,
        "sf50m_allowed": False,
        "decision": (
            "Do not enable runtime or scaling. Add hygiene-focused corpus/protected terms and rerun micro-probes."
            if status == "COMPLETED_HYGIENE_AUDIT_WITH_BLOCKERS"
            else "Hygiene audit is clean; next train a hygiene repair probe before runtime."
        ),
        "terms": term_rows,
    }


def main() -> int:
    args = parse_args()
    report = build_report(
        terms_path=args.terms,
        tokenizer_path=args.tokenizer,
        max_good_pieces=args.max_good_pieces,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("SF.AI — Phase 27.18 tokenization/decoding hygiene audit")
    print(f"  status                  : {report['status']}")
    print(f"  terms_total             : {report['terms_total']}")
    print(f"  average_pieces          : {report['average_pieces']}")
    print(f"  aggressive_split_terms  : {len(report['aggressive_split_terms'])}")
    print(f"  roundtrip_failures      : {len(report['roundtrip_failures'])}")
    print(f"  uncovered_bad_fragments : {len(report['uncovered_bad_fragments'])}")
    print(f"  runtime_allowed         : {str(report['runtime_allowed']).lower()}")
    print(f"  report                  : {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
