#!/usr/bin/env bash
# SF.AI — non-disruptive server status check.
#
# This script never starts, stops, restarts, or kills the server. It only
# reports whether port 8123 is listening and whether /health responds.

set -u

cd "$(dirname "$0")/.." || exit 1

HOST="${SF_HOST:-127.0.0.1}"
PORT="${SF_PORT:-8123}"
URL="http://$HOST:$PORT"

echo "SF.AI — server status (read-only)"
echo "  url: $URL"

echo
echo "listener:"
if command -v lsof >/dev/null 2>&1; then
  lsof -iTCP:"$PORT" -sTCP:LISTEN -n -P || true
else
  echo "  lsof: not installed"
fi

echo
echo "health:"
if command -v curl >/dev/null 2>&1; then
  curl -s "$URL/health" || true
  echo
else
  echo "  curl: not installed"
fi

echo
echo "note: this command is read-only; it does not restart or stop the server."
