#!/usr/bin/env bash
# SF.AI — start chat server in a detached screen session if it is not running.
#
# Safety:
# - If port 8123 is already listening, this script exits without touching it.
# - It never kills, restarts, or replaces a running server.
# - It uses screen because background child processes launched by some agents
#   may be cleaned up when the command session exits.

set -u

cd "$(dirname "$0")/.." || exit 1

HOST="${SF_HOST:-127.0.0.1}"
PORT="${SF_PORT:-8123}"
SESSION="${SF_SCREEN_SESSION:-sfai8123}"

if command -v lsof >/dev/null 2>&1 && lsof -iTCP:"$PORT" -sTCP:LISTEN -n -P >/dev/null 2>&1; then
  echo "SF.AI server already listening on $HOST:$PORT; leaving it untouched."
  exit 0
fi

if ! command -v screen >/dev/null 2>&1; then
  echo "error: screen is required for detached server start" >&2
  exit 1
fi

screen -dmS "$SESSION" bash -lc "cd '$PWD' && bash scripts/run_chat_server.sh > /tmp/sfai_uvicorn.log 2>&1"
sleep 2

echo "SF.AI server requested in detached screen session: $SESSION"
bash scripts/server_status.sh
