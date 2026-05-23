# SF.AI — Makefile
# Phase 1 set of operational commands.

.PHONY: help check-env install test lint type api web docker-up docker-down phase-status server-status server-start import-mo3jam-saudi source-inventory corpus-audit tokenization-audit build-dialogue-split phase12-readiness phase19-readiness phase20-gates phase22-readiness phase22-plan phase22-next-batch phase22-completion-gate phase22-review-intake phase23-tokenizer-audit phase26-readiness phase27-dialogue-eval phase27-generation-quality phase27-objective-probe phase27-eos-probe phase27-quality-tooling phase27-social-lexical-curriculum phase27-prompt-answer-probe phase27-hygiene-audit phase27-hygiene-repair-probe phase27-tokenizer-strategy phase27-tokenizer-v3-probe phase27-spacing-boundary-repair prepare-dialogue-batch train-bpe train-lm eval-lm eval-phase16

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
	@echo "  make build-dialogue-split Build fixed train/eval split manifest"
	@echo "  make phase12-readiness    Read-only Phase 12 decision: ready vs allowed"
	@echo "  make phase19-readiness    Read-only Phase 19 decision before SF-50M"
	@echo "  make phase20-gates        Read-only Phase 20 domain activation gates"
	@echo "  make phase22-readiness    Read-only Phase 22 Gold Dialogue Corpus v2 gate"
	@echo "  make phase22-plan         Read-only Phase 22 corpus collection plan"
	@echo "  make phase22-next-batch   Show the immediate Phase 22 authoring task"
	@echo "  make phase22-completion-gate Strict Phase 22 completion gate before Phase 23"
	@echo "  make phase22-review-intake Scan review exports before corpus conversion"
	@echo "  make phase23-tokenizer-audit Finalize/audit Phase 23 tokenizer v2"
	@echo "  make phase26-readiness    Read-only Phase 26 scaling gate before SF-50M"
	@echo "  make phase27-dialogue-eval Run Phase 27 dialogue eval v2 + corpus plan"
	@echo "  make phase27-generation-quality Run native generation quality canary"
	@echo "  make phase27-objective-probe Run Phase 27.11 gold overfit/stop-boundary probe"
	@echo "  make phase27-eos-probe Run Phase 27.12 boundary/EOS probe"
	@echo "  make phase27-quality-tooling Run Phase 27.14 sovereign quality tooling decision"
	@echo "  make phase27-social-lexical-curriculum Write Phase 27.15 social/lexical repair batch"
	@echo "  make phase27-prompt-answer-probe Run Phase 27.17 prompt-answer micro-probe"
	@echo "  make phase27-hygiene-audit Run Phase 27.18 tokenization/decoding hygiene audit"
	@echo "  make phase27-hygiene-repair-probe Run Phase 27.19 hygiene repair probe"
	@echo "  make phase27-tokenizer-strategy Run Phase 27.20 protected-phrase strategy"
	@echo "  make phase27-tokenizer-v3-probe Run Phase 27.21 tokenizer v3 + micro-probe"
	@echo "  make phase27-spacing-boundary-repair Run Phase 27.22 spacing/boundary repair"
	@echo "  make prepare-dialogue-batch ARGS=...  Prepare reviewed chat exports (Phase 18)"
	@echo "  make train-bpe ARGS=...   Train SF-BPE tokenizer (requires phase confirmation flag)"
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

build-dialogue-split:
	$(PY) scripts/build_dialogue_split.py $(ARGS)

phase12-readiness:
	$(PY) scripts/phase12_readiness.py

phase19-readiness:
	$(PY) scripts/phase19_readiness.py

phase20-gates:
	$(PY) scripts/phase20_gates.py

phase22-readiness:
	$(PY) scripts/phase22_readiness.py

phase22-plan:
	$(PY) scripts/phase22_collection_plan.py $(ARGS)

phase22-next-batch:
	$(PY) scripts/phase22_next_batch.py $(ARGS)

phase22-completion-gate:
	$(PY) scripts/phase22_completion_gate.py $(ARGS)

phase22-review-intake:
	$(PY) scripts/phase22_review_intake.py $(ARGS)

phase23-tokenizer-audit:
	$(PY) scripts/phase23_tokenizer_audit.py $(ARGS)

phase26-readiness:
	$(PY) scripts/phase26_readiness.py $(ARGS)

phase27-dialogue-eval:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_dialogue_eval.py $(ARGS)

phase27-generation-quality:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_9_generation_quality_eval.py $(ARGS)

phase27-objective-probe:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_11_objective_probe.py $(ARGS)

phase27-eos-probe:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_11_objective_probe.py \
		--phase "Phase 27.12 — Assistant Boundary/EOS Repair" \
		--work-dir artifacts/eval/phase27_12_eos_probe \
		--report artifacts/reports/phase27_12_eos_probe_report.json \
		--samples artifacts/samples/phase27_12_eos_probe_generations.md \
		$(ARGS)

phase27-quality-tooling:
	$(PY) scripts/phase27_14_quality_tooling.py $(ARGS)

phase27-social-lexical-curriculum:
	$(PY) scripts/phase27_15_write_social_lexical_curriculum.py $(ARGS)

phase27-prompt-answer-probe:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_17_prompt_answer_micro_probe.py $(ARGS)

phase27-hygiene-audit:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_18_hygiene_audit.py $(ARGS)

phase27-hygiene-repair-probe:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_19_hygiene_repair_probe.py $(ARGS)

phase27-tokenizer-strategy:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_20_tokenizer_strategy.py $(ARGS)

phase27-tokenizer-v3-probe:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_21_tokenizer_v3_micro_probe.py $(ARGS)

phase27-spacing-boundary-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_22_spacing_boundary_repair.py $(ARGS)

prepare-dialogue-batch:
	$(PY) scripts/prepare_dialogue_batch.py $(ARGS)

# Phase 12/23 — train SF-BPE tokenizer.
# Requires explicit phase approval flag.
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
