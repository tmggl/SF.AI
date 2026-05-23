#!/usr/bin/env python3
"""SF.AI — finalize and audit Phase 23 tokenizer v2 artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.training.phase23_tokenizer import write_phase23_artifact_files  # noqa: E402


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Audit SF.AI tokenizer v2")
    parser.add_argument("--artifact", default="artifacts/tokenizers/sf_bpe/v2")
    parser.add_argument("--previous", default="artifacts/tokenizers/sf_bpe/v1")
    parser.add_argument("--corpus", default="data/corpus/chat/jsonl")
    parser.add_argument(
        "--required-flag-used",
        default="--confirm-phase23-tokenizer",
    )
    args = parser.parse_args(argv)

    audit = write_phase23_artifact_files(
        artifact_dir=args.artifact,
        previous_artifact_dir=args.previous,
        corpus_root=args.corpus,
        required_flag_used=args.required_flag_used,
    )

    print("SF.AI — Phase 23 tokenizer v2 audit")
    print(f"  phase                         : {audit.phase}")
    print(f"  status                        : {audit.status}")
    print(f"  artifact                      : {audit.artifact_dir}")
    print(f"  previous                      : {audit.previous_artifact_dir}")
    print(f"  vocab_size                    : {audit.tokenizer['vocab_size']}")
    print(f"  merges                        : {audit.tokenizer['merges']}")
    print(f"  words_seen                    : {audit.tokenizer['words_seen']}")
    print(f"  unique_words                  : {audit.tokenizer['unique_words']}")
    print(f"  corpus_records                : {audit.corpus['training_ready']}")
    print(f"  dialects                      : {audit.corpus['dialects']}")
    print(
        "  protected_terms_covered       : "
        f"{audit.tokenization_policy['protected_terms_covered']}/"
        f"{audit.tokenization_policy['protected_terms_total']}"
    )
    print(
        "  protected_avg_tokens_v1_to_v2 : "
        f"{audit.protected_terms_behavior['average_v1_tokens']} -> "
        f"{audit.protected_terms_behavior['average_v2_tokens']}"
    )
    print(f"  sf_origin                     : {str(audit.sovereignty['sf_origin']).lower()}")
    print()
    print("decision:")
    for key, value in audit.decision.items():
        print(f"  - {key}: {value}")

    return 0 if audit.status == "COMPLETED_READY_FOR_PHASE24" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
