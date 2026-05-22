#!/usr/bin/env python3
"""SF.AI — Import Saudi-dialect lexicon from Mo3jam (Phase 3.5).

Source : معجم — اللهجة السعودية (https://ar.mo3jam.com/dialect/Saudi)
Permission: confirmed verbally by the user. credit_required=true on every
record produced.

Dry-run is the default. A real import requires:
    --confirm-user-permission

Example (real run):
    python scripts/import_mo3jam_saudi.py \\
        --confirm-user-permission \\
        --rate-limit 2.0 \\
        --resume

Example (sanity check, no network):
    python scripts/import_mo3jam_saudi.py --dry-run

Politeness:
- 2 s default delay between requests
- User-Agent: "SF.AI Research Importer - permission confirmed by user"
- No parallel crawl
- Resume from existing JSONL
- robots.txt checked before the first live request
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets.dialects import (  # noqa: E402
    DialectLexiconMeta,
    build_dialect_yaml,
)
from sf_ai.tools.web.mo3jam_importer import (  # noqa: E402
    EXPECTED_TERMS,
    Mo3jamImportConfig,
    Mo3jamImporter,
    SOURCE_NAME,
    SOURCE_ROOT,
)


DEFAULT_OUTPUT = Path("data/corpus/dialects/saudi/jsonl/mo3jam_saudi_terms.jsonl")
DEFAULT_RAW = Path("data/corpus/dialects/saudi/raw/mo3jam")
DEFAULT_REPORT = Path("data/corpus/dialects/saudi/reports/mo3jam_import_report.md")
DEFAULT_FAILED = Path("data/corpus/dialects/saudi/reports/mo3jam_failed_urls.txt")
DEFAULT_YAML = Path("resources/lexicons/imported/mo3jam/saudi_dialect_terms.yaml")


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Import Mo3jam Saudi-dialect lexicon")
    p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                   help="JSONL output path")
    p.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW,
                   help="Where to save raw HTML pages")
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT,
                   help="Markdown report path")
    p.add_argument("--failed-urls", type=Path, default=DEFAULT_FAILED,
                   help="File for any failed URLs")
    p.add_argument("--yaml-output", type=Path, default=DEFAULT_YAML,
                   help="SF lexicon YAML output path")
    p.add_argument("--rate-limit", type=float, default=2.0,
                   help="Seconds to sleep between requests (>=0)")
    p.add_argument("--limit", type=int, default=None,
                   help="Cap on terms imported (useful for sampling)")
    p.add_argument("--resume", action="store_true", default=True,
                   help="Skip terms already present in the JSONL (default)")
    p.add_argument("--no-resume", action="store_false", dest="resume",
                   help="Start fresh; ignore existing JSONL")
    p.add_argument("--dry-run", action="store_true", default=True,
                   help="Plan only — no network, no writes (default)")
    p.add_argument("--no-dry-run", action="store_false", dest="dry_run",
                   help="Disable dry-run (still requires --confirm-user-permission)")
    p.add_argument("--confirm-user-permission", action="store_true",
                   help="Acknowledge that the user has obtained verbal permission "
                        "from Mo3jam (required for live crawling)")
    p.add_argument("--skip-yaml", action="store_true",
                   help="Skip building the SF lexicon YAML after import")
    args = p.parse_args(argv)

    # Live mode requires both --no-dry-run AND --confirm-user-permission.
    live = (not args.dry_run) and args.confirm_user_permission
    if (not args.dry_run) and (not args.confirm_user_permission):
        print(
            "error: live crawl requires --confirm-user-permission. "
            "Re-run with --dry-run, or pass --no-dry-run --confirm-user-permission.",
            file=sys.stderr,
        )
        return 2

    cfg = Mo3jamImportConfig(
        output_jsonl=args.output,
        raw_dir=args.raw_dir,
        report_path=args.report,
        failed_urls_path=args.failed_urls,
        rate_limit_seconds=args.rate_limit,
        limit=args.limit,
        resume=args.resume,
        dry_run=not live,
        user_permission_confirmed=args.confirm_user_permission,
    )

    print(f"SF.AI — Mo3jam Saudi-dialect import")
    print(f"  source   : {SOURCE_NAME}")
    print(f"  url      : {SOURCE_ROOT}")
    print(f"  mode     : {'LIVE' if live else 'DRY-RUN'}")
    print(f"  output   : {cfg.output_jsonl}")
    print(f"  rate-lim : {cfg.rate_limit_seconds}s")
    if cfg.limit is not None:
        print(f"  limit    : {cfg.limit}")
    print(f"  expected : {EXPECTED_TERMS} terms")
    print()

    importer = Mo3jamImporter(cfg)

    if live:
        allowed = importer.check_robots()
        if not allowed:
            print("error: robots.txt does not permit fetching the source root.",
                  file=sys.stderr)
            return 1

    pairs = importer.crawl_listing()
    if live:
        imported = importer.crawl_terms(pairs)
        importer.write_failed_urls()
        report_path = importer.write_report()
        print(f"\nimported: {imported} terms")
        print(f"report  : {report_path}")
        print(f"jsonl   : {cfg.output_jsonl}")

        if not args.skip_yaml:
            meta = DialectLexiconMeta(
                source_name=SOURCE_NAME,
                source_url=SOURCE_ROOT,
                permission_status="allowed_with_user_confirmed_permission",
                credit_required=True,
                expected_terms=EXPECTED_TERMS,
            )
            n = build_dialect_yaml(cfg.output_jsonl, args.yaml_output, meta=meta)
            print(f"yaml    : {args.yaml_output} ({n} terms)")
    else:
        # Dry-run: show plan and exit.
        report = importer.report
        print("dry-run summary:")
        print(f"  letters that would be fetched : {report.letters_seen or len(cfg.letters)}")
        print(f"  expected terms                : {EXPECTED_TERMS}")
        print(f"  output JSONL                  : {cfg.output_jsonl}")
        print(f"  raw HTML dir                  : {cfg.raw_dir}")
        print("\nTo run for real:")
        print(
            f"  python scripts/import_mo3jam_saudi.py --no-dry-run "
            f"--confirm-user-permission --rate-limit {cfg.rate_limit_seconds}"
        )

    print()
    print("Attribution (always include in derived outputs):")
    print("مصدر اللهجات السعودية:")
    print(SOURCE_NAME)
    print(SOURCE_ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
