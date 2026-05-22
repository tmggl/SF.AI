#!/usr/bin/env python3
"""SF.AI — audit tokenization policy before Phase 12.

This script is read-only. It never trains a tokenizer and never writes
artifacts.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.models.tokenizer.policy_audit import audit_tokenization_policy  # noqa: E402


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Audit SF.AI tokenization policy")
    parser.add_argument("--corpus", default="data/corpus/chat/jsonl")
    parser.add_argument(
        "--protected-terms",
        default=None,
    )
    parser.add_argument(
        "--preferred-merges",
        default=None,
    )
    parser.add_argument(
        "--rules",
        default="resources/tokenization/tokenization_rules.yaml",
    )
    parser.add_argument("--show-missing", action="store_true")
    args = parser.parse_args(argv)

    report = audit_tokenization_policy(
        corpus=args.corpus,
        protected_terms_path=args.protected_terms,
        preferred_merges_path=args.preferred_merges,
        rules_path=args.rules,
    )

    print("SF.AI — tokenization policy audit")
    print(f"  status                  : {report.status}")
    print(f"  corpus                  : {report.corpus}")
    print(f"  corpus_files            : {report.corpus_files}")
    print(f"  messages_seen           : {report.messages_seen}")
    print(f"  protected_terms_total   : {report.protected_terms_total}")
    print(f"  protected_terms_covered : {report.protected_terms_covered}")
    print(f"  coverage_ratio          : {report.coverage_ratio:.2%}")
    print(f"  protected_terms_path    : {report.protected_terms_path}")
    print(
        "  protected_terms_paths   : "
        + ", ".join(str(path) for path in report.protected_terms_paths)
    )
    print(f"  preferred_merges_path   : {report.preferred_merges_path}")
    print(
        "  preferred_merges_paths  : "
        + ", ".join(str(path) for path in report.preferred_merges_paths)
    )
    print(f"  rules_path              : {report.rules_path}")
    print()

    print("covered protected terms:")
    if report.protected_hits:
        for hit in report.protected_hits:
            print(f"  - {hit.term}: {hit.count}")
    else:
        print("  - none")

    if args.show_missing:
        print()
        print("missing protected terms:")
        if report.missing_terms:
            for term in report.missing_terms:
                print(f"  - {term}")
        else:
            print("  - none")

    if report.warnings:
        print()
        print("warnings:")
        for warning in report.warnings:
            print(f"  - {warning}")

    print()
    print("note: no tokenizer training was started and no artifacts were written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
