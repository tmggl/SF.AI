#!/usr/bin/env bash
# SF.AI — launch the chat server with the recommended runtime flags.
#
# Why a separate script: setting env vars at import-time inside main.py
# poisons test isolation. The flags below are runtime-only concerns and
# belong here, next to the launch command.

set -u

cd "$(dirname "$0")/.." || exit 1

# Enable the user-authored Saudi Seed v1 lexicon (516 entries, runtime-safe
# subset ~300) inside DialectMapper. Override by exporting false beforehand.
export ENABLE_SAUDI_SEED_V1_LEXICON="${ENABLE_SAUDI_SEED_V1_LEXICON:-true}"

# Mo3jam stays OFF by default — it ships dry-run-only and the user opts in
# via the importer CLI rather than the chat server.
export ENABLE_MO3JAM_SAUDI_LEXICON="${ENABLE_MO3JAM_SAUDI_LEXICON:-false}"

# Keep normal UI/export traffic on the stable template path. The raw SF-10M
# generator is a lab probe only; enable broad non-sensitive generation by
# explicitly exporting SF_LAB_GENERATION_FOR_NON_SENSITIVE=true.
export SF_LAB_GENERATION_FOR_NON_SENSITIVE="${SF_LAB_GENERATION_FOR_NON_SENSITIVE:-false}"

HOST="${SF_HOST:-127.0.0.1}"
PORT="${SF_PORT:-8123}"

echo "SF.AI — chat server"
echo "  host                              : $HOST"
echo "  port                              : $PORT"
echo "  ENABLE_SAUDI_SEED_V1_LEXICON      : $ENABLE_SAUDI_SEED_V1_LEXICON"
echo "  ENABLE_MO3JAM_SAUDI_LEXICON       : $ENABLE_MO3JAM_SAUDI_LEXICON"
echo "  SF_ENABLE_NATIVE_GENERATOR        : ${SF_ENABLE_NATIVE_GENERATOR:-false}"
echo "  SF_NATIVE_GENERATOR_EXPERIMENTAL  : ${SF_NATIVE_GENERATOR_EXPERIMENTAL:-false}"
echo "  SF_GUARDED_RUNTIME_TRIAL          : request-scoped via generator_trial=true"
echo "  SF_LAB_GENERATION_FOR_NON_SENSITIVE: $SF_LAB_GENERATION_FOR_NON_SENSITIVE"
echo "  UI                                : http://$HOST:$PORT/ui/chat"
echo

exec .venv/bin/uvicorn apps.api.main:app --host "$HOST" --port "$PORT" "$@"
