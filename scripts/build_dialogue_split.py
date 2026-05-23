#!/usr/bin/env python3
"""Build deterministic train/eval split manifest for SF.AI dialogue corpus."""

from __future__ import annotations

import argparse
from pathlib import Path

from sf_ai.datasets.splits import write_split_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build fixed dialogue train/eval split")
    parser.add_argument("--corpus", default="data/corpus/chat/jsonl")
    parser.add_argument("--out", default="data/corpus/chat/splits/dialogue_split_v1.json")
    parser.add_argument("--eval-ratio", type=float, default=0.10)
    parser.add_argument("--salt", default="sf-ai-dialogue-v1")
    args = parser.parse_args()

    manifest = write_split_manifest(
        Path(args.corpus),
        Path(args.out),
        eval_ratio=args.eval_ratio,
        salt=args.salt,
    )
    print("SF.AI — dialogue split manifest")
    print(f"  corpus        : {args.corpus}")
    print(f"  out           : {args.out}")
    print(f"  total_records : {manifest['total_records']}")
    print(f"  counts        : {manifest['counts']}")
    print(f"  dialects      : {manifest['dialects']}")
    print(f"  qualities     : {manifest['qualities']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
