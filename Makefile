# SF.AI — Makefile
# Phase 1 set of operational commands.

.PHONY: help check-env install test lint type api web docker-up docker-down phase-status server-status server-start import-mo3jam-saudi source-inventory corpus-audit tokenization-audit phase12-readiness train-bpe train-lm eval-lm eval-phase16

PY ?= .venv/bin/python
UVICORN ?= uvicorn

help:
	@echo "SF.AI — available commands:"
	@echo "  make check-env     Check Python and tooling versions"
	@echo "  make install       Install package + dev dependencies"
	@echo "  make test          Run pytest"
	@echo "  make lint          Run ruff"
	@echo "  make type          Run mypy"
	@echo "  make api           Run FastAPI dev server (uvicorn --reload)"
	@echo "  make web           Run frontend (placeholder — Phase 9)"
	@echo "  make docker-up     Start docker-compose services"
	@echo "  make docker-down   Stop docker-compose services"
	@echo "  make phase-status  Print current phase status"
	@echo "  make server-status Check port 8123 without restart/stop"
	@echo "  make server-start  Start API detached only if 8123 is not running"
	@echo "  make import-mo3jam-saudi  Run the Phase 3.5 Saudi-dialect importer"
	@echo "                            (dry-run by default; ARGS to override)"
	@echo "  make source-inventory     Show all local data/reference sources"
	@echo "  make corpus-audit         Audit JSONL corpus before Phase 12"
	@echo "  make tokenization-audit   Audit tokenization policy before Phase 12"
	@echo "  make phase12-readiness    Read-only Phase 12 decision: ready vs allowed"
	@echo "  make train-bpe ARGS=...   Train SF-BPE tokenizer (requires Phase 12 confirmation flag)"
	@echo "  make train-lm ARGS=...    Train SF native LM (Phase 6)"
	@echo "  make eval-lm ARGS=...     Evaluate a SF.AI checkpoint"
	@echo "  make eval-phase16         Run Phase 16 chat/safety/style gate"

check-env:
	@echo "Python: $$($(PY) --version 2>&1)"
	@command -v $(UVICORN) >/dev/null 2>&1 && echo "uvicorn: $$($(UVICORN) --version)" || echo "uvicorn: not installed"
	@command -v pytest >/dev/null 2>&1 && echo "pytest: $$(pytest --version 2>&1 | head -n1)" || echo "pytest: not installed"
	@command -v docker >/dev/null 2>&1 && echo "docker: $$(docker --version)" || echo "docker: not installed"

install:
	$(PY) -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

type:
	mypy sf_ai apps

api:
	bash scripts/run_chat_server.sh --reload

web:
	@echo "Phase 9 — frontend not implemented yet."

docker-up:
	docker compose up -d

docker-down:
	docker compose down

phase-status:
	@echo "----- docs/PHASE_STATUS.md -----"
	@head -n 30 docs/PHASE_STATUS.md

server-status:
	bash scripts/server_status.sh

server-start:
	bash scripts/start_chat_server_detached.sh

# Phase 3.5 — import Mo3jam Saudi-dialect lexicon.
# Default: dry-run. To go live, override with:
#   make import-mo3jam-saudi ARGS="--no-dry-run --confirm-user-permission"
# Source: معجم — اللهجة السعودية / https://ar.mo3jam.com/dialect/Saudi
import-mo3jam-saudi:
	$(PY) scripts/import_mo3jam_saudi.py $(ARGS)

# Phase 12 preflight — refuses readiness when no approved Saudi/MSA JSONL exists.
source-inventory:
	$(PY) scripts/source_inventory.py

corpus-audit:
	$(PY) scripts/audit_training_corpus.py $(ARGS)

tokenization-audit:
	$(PY) scripts/audit_tokenization_policy.py $(ARGS)

phase12-readiness:
	$(PY) scripts/phase12_readiness.py

# Phase 12 — train SF-BPE tokenizer.
# Requires explicit Sami approval and --confirm-phase12-permission.
# Example after approval only:
#   make train-bpe ARGS="--confirm-phase12-permission --corpus data/corpus/chat/jsonl --out artifacts/tokenizers/sf_bpe/v1"
train-bpe:
	$(PY) -m sf_ai.training.train_tokenizer $(ARGS)

# Phase 6 — train SF native LM.
# Example: make train-lm ARGS="--tokenizer artifacts/tokenizers/sf_bpe/v1 \
#                              --corpus data/corpus/chat/jsonl --size sf-10m --steps 50"
train-lm:
	$(PY) -m sf_ai.training.train_tiny_lm $(ARGS)

# Phase 6 — evaluate a checkpoint.
eval-lm:
	$(PY) -m sf_ai.training.evaluate_tiny_lm $(ARGS)

# Phase 16 — runtime gate before native generation can answer users.
eval-phase16:
	$(PY) scripts/run_phase16_eval.py $(ARGS)
