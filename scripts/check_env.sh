#!/usr/bin/env bash
# SF.AI — environment check (Phase 1).
# Verifies presence of expected local tooling. Does NOT install anything.

set -u

echo "SF.AI — Environment Check"
echo "-------------------------"

check_cmd () {
  local name="$1"
  local cmd="$2"
  if command -v "$cmd" >/dev/null 2>&1; then
    local ver
    ver=$("$cmd" --version 2>&1 | head -n1)
    echo "  [OK]  $name: $ver"
  else
    echo "  [MISS] $name: not installed"
  fi
}

check_cmd "python3"  "python3"
check_cmd "pip3"     "pip3"
check_cmd "uvicorn"  "uvicorn"
check_cmd "pytest"   "pytest"
check_cmd "ruff"     "ruff"
check_cmd "mypy"     "mypy"
check_cmd "docker"   "docker"

echo "-------------------------"
echo "Reminder: SF.AI uses NO external AI APIs and NO pretrained models."
echo "See PROJECT_PRINCIPLES.md for the full policy."
