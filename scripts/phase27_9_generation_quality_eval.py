#!/usr/bin/env python
"""Run Phase 27.9 native generation quality canary."""

from __future__ import annotations

import argparse
from pathlib import Path

from sf_ai.evaluation.generation_quality import (
    DEFAULT_ARTIFACT_REPORT,
    DEFAULT_REPORT,
    DEFAULT_SUITE,
    write_generation_quality_report,
)
from sf_ai.modules.chat.native_generator import NativeGenerator, NativeGeneratorConfig


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase 27.9 generation quality canary")
    p.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT_REPORT)
    p.add_argument("--tokenizer", type=Path, default=Path("artifacts/tokenizers/sf_bpe/v2"))
    p.add_argument("--checkpoints", type=Path, default=Path("artifacts/checkpoints/sf_10m_v0_8"))
    p.add_argument("--checkpoint-name", type=str, default="sf-10m-step6000")
    p.add_argument("--generator-name", type=str, default="sf_10m_v0_8")
    p.add_argument("--model-size", type=str, default="sf-10m")
    p.add_argument("--seq-len", type=int, default=64)
    p.add_argument("--max-new-tokens", type=int, default=48)
    p.add_argument("--temperature", type=float, default=0.20)
    p.add_argument("--top-k", type=int, default=0)
    p.add_argument("--device", type=str, default="auto")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=args.tokenizer,
            checkpoints_root=args.checkpoints,
            checkpoint_name=args.checkpoint_name,
            generator_name=args.generator_name,
            model_size=args.model_size,
            seq_len=args.seq_len,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            top_k=args.top_k,
            device=args.device,
            dialogue_prompt=True,
        )
    )
    report = write_generation_quality_report(
        suite_path=args.suite,
        report_path=args.report,
        artifact_path=args.artifact,
        generator=generator,
        checkpoint_name=args.checkpoint_name,
        generator_name=args.generator_name,
    )
    print("SF.AI — Phase 27.9 generation quality canary")
    print(f"  status          : {report.status}")
    print(f"  generator       : {report.generator_name}")
    print(f"  checkpoint      : {report.checkpoint_name}")
    print(f"  prompts         : {report.passed_prompts}/{report.total_prompts}")
    print(f"  pass_rate       : {report.pass_rate:.2%}")
    print(f"  runtime_allowed : {str(report.runtime_allowed).lower()}")
    print(f"  guard_reasons   : {report.guard_reason_counts}")
    if report.blockers:
        print("\nblockers:")
        for blocker in report.blockers:
            print(f"  - {blocker}")
    print(f"\noutput: {args.report}")
    print(f"artifact: {args.artifact}")
    # A blocked generator is a valid quality-gate decision, not a CLI failure.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
