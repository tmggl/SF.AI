# SF.AI — Makefile
# Phase 1 set of operational commands.

.PHONY: help check-env install test lint type api web docker-up docker-down phase-status server-status server-start import-mo3jam-saudi source-inventory corpus-audit tokenization-audit build-dialogue-split phase12-readiness phase19-readiness phase20-gates phase22-readiness phase22-plan phase22-next-batch phase22-completion-gate phase22-review-intake phase23-tokenizer-audit phase26-readiness phase27-dialogue-eval phase27-generation-quality phase27-objective-probe phase27-eos-probe phase27-quality-tooling phase27-social-lexical-curriculum phase27-prompt-answer-probe phase27-hygiene-audit phase27-hygiene-repair-probe phase27-tokenizer-strategy phase27-tokenizer-v3-probe phase27-spacing-boundary-repair phase27-semantic-lexical-repair phase27-minimal-lexical-stabilization phase27-heldout-generation-canary phase27-heldout-objective-repair phase27-broader-heldout-repair phase27-intent-conditioned-repair phase27-topic-definition-repair phase27-fresh-mixed-shadow phase27-natural-intent-topic-dataset phase27-balanced-natural-calibration phase27-advice-micro-stabilization phase27-guarded-runtime-trial phase27-live-ui-trial phase27-live-ui-triage phase27-supported-topic-expansion phase27-targeted-topic-curriculum phase27-topic-isolation-repair phase27-tokenizer-context-repair phase27-guarded-runtime-switch phase27-live-ui-broader-probes phase27-guarded-data-backed-expansion phase27-tokenizer-curriculum-repair phase27-semantic-topic-balance-repair phase27-core-dialogue-stabilization phase27-new-topic-conditioning-repair phase27-guarded-runtime-switch-47 phase27-broader-live-ui-probes-47 phase27-generator-only-ui-gate phase27-open-dialogue-generalization-audit phase27-natural-dialogue-objective-repair phase27-natural-dialogue-diversity-expansion phase27-tokenizer-bounded-alignment-probe phase27-bounded-alignment-repair phase27-broader-natural-dialogue-canary phase27-broader-generalization-repair phase27-open-social-repair phase27-candidate-selection phase27-stability-first-repair prepare-dialogue-batch train-bpe train-lm eval-lm eval-phase16

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
	@echo "  make phase27-semantic-lexical-repair Run Phase 27.23 semantic/lexical repair"
	@echo "  make phase27-minimal-lexical-stabilization Run Phase 27.24 minimal lexical stabilization"
	@echo "  make phase27-heldout-generation-canary Run Phase 27.25 held-out generation canary"
	@echo "  make phase27-heldout-objective-repair Run Phase 27.26 held-out objective repair"
	@echo "  make phase27-broader-heldout-repair Run Phase 27.27 broader held-out repair"
	@echo "  make phase27-intent-conditioned-repair Run Phase 27.28 intent-conditioned repair"
	@echo "  make phase27-topic-definition-repair Run Phase 27.29 topic-conditioned definition repair"
	@echo "  make phase27-fresh-mixed-shadow Run Phase 27.30 fresh mixed shadow canary"
	@echo "  make phase27-natural-intent-topic-dataset Run Phase 27.31 natural intent/topic dataset"
	@echo "  make phase27-balanced-natural-calibration Run Phase 27.32 balanced natural calibration"
	@echo "  make phase27-advice-micro-stabilization Run Phase 27.33 advice + micro stabilization"
	@echo "  make phase27-guarded-runtime-trial Run Phase 27.34 guarded runtime trial"
	@echo "  make phase27-live-ui-trial Run Phase 27.35 live UI trial observations"
	@echo "  make phase27-live-ui-triage Run Phase 27.36 live UI triage + quality floor"
	@echo "  make phase27-supported-topic-expansion Run Phase 27.37 supported topic expansion"
	@echo "  make phase27-targeted-topic-curriculum Run Phase 27.38 targeted topic curriculum/probe"
	@echo "  make phase27-topic-isolation-repair Run Phase 27.39 topic-isolation repair"
	@echo "  make phase27-tokenizer-context-repair Run Phase 27.40 tokenizer/context repair"
	@echo "  make phase27-guarded-runtime-switch Run Phase 27.41 guarded runtime switch"
	@echo "  make phase27-live-ui-broader-probes Run Phase 27.42 broader live UI probes"
	@echo "  make phase27-guarded-data-backed-expansion Run Phase 27.43 weak-lane repair probe"
	@echo "  make phase27-tokenizer-curriculum-repair Run Phase 27.44 tokenizer/curriculum repair"
	@echo "  make phase27-semantic-topic-balance-repair Run Phase 27.45 semantic topic balance repair"
	@echo "  make phase27-core-dialogue-stabilization Run Phase 27.46 core dialogue stabilization"
	@echo "  make phase27-new-topic-conditioning-repair Run Phase 27.47 new-topic conditioning repair"
	@echo "  make phase27-guarded-runtime-switch-47 Run Phase 27.48 guarded runtime switch"
	@echo "  make phase27-broader-live-ui-probes-47 Run Phase 27.49 broader live UI/API probes"
	@echo "  make phase27-generator-only-ui-gate Run Phase 27.50 generator-only UI/API gate"
	@echo "  make phase27-open-dialogue-generalization-audit Run Phase 27.51 no-keyword open dialogue audit"
	@echo "  make phase27-natural-dialogue-objective-repair Run Phase 27.52 doubled SF-10M natural dialogue repair"
	@echo "  make phase27-natural-dialogue-diversity-expansion Run Phase 27.53 large natural dialogue diversity training"
	@echo "  make phase27-tokenizer-bounded-alignment-probe Run Phase 27.58 tokenizer v7 + bounded alignment probe"
	@echo "  make phase27-bounded-alignment-repair Run Phase 27.59 bounded family-alignment repair"
	@echo "  make phase27-broader-natural-dialogue-canary Run Phase 27.60 broader natural-dialogue canary"
	@echo "  make phase27-broader-generalization-repair Run Phase 27.61 broader natural-dialogue repair"
	@echo "  make phase27-candidate-selection Run Phase 27.71 candidate selection/stability gate"
	@echo "  make phase27-stability-first-repair Run Phase 27.72 stability-first micro repair"
	@echo "  make phase27-open-social-failure-inspection Run Phase 27.73 open_social failure inspection"
	@echo "  make phase27-open-social-semantic-collapse-repair Run Phase 27.74 semantic-collapse repair"
	@echo "  make phase27-open-social-strategy-inspection Run Phase 27.75 open_social tokenizer strategy inspection"
	@echo "  make phase27-tokenizer-v9-open-social-boundary-probe Run Phase 27.76 tokenizer v9 boundary probe"
	@echo "  make phase27-v9-bounded-open-social-lm-repair Run Phase 27.77 bounded LM repair on tokenizer v9"
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

phase27-semantic-lexical-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_23_semantic_lexical_repair.py $(ARGS)

phase27-minimal-lexical-stabilization:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_24_minimal_lexical_stabilization.py $(ARGS)

phase27-heldout-generation-canary:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_25_heldout_generation_canary.py $(ARGS)

phase27-heldout-objective-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_26_heldout_objective_repair.py $(ARGS)

phase27-broader-heldout-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_27_broader_heldout_repair.py $(ARGS)

phase27-intent-conditioned-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_28_intent_conditioned_repair.py $(ARGS)

phase27-topic-definition-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_29_topic_conditioned_definition_repair.py $(ARGS)

phase27-fresh-mixed-shadow:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_30_fresh_mixed_shadow_canary.py $(ARGS)

phase27-natural-intent-topic-dataset:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_31_natural_intent_topic_dataset.py $(ARGS)

phase27-balanced-natural-calibration:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_32_balanced_natural_calibration.py $(ARGS)

phase27-advice-micro-stabilization:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_33_advice_micro_stabilization.py $(ARGS)

phase27-guarded-runtime-trial:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_34_guarded_runtime_trial.py $(ARGS)

phase27-live-ui-trial:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_35_live_ui_trial_observations.py $(ARGS)

phase27-live-ui-triage:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_36_live_ui_triage.py $(ARGS)

phase27-supported-topic-expansion:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_37_supported_topic_expansion.py $(ARGS)

phase27-targeted-topic-curriculum:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_38_targeted_topic_curriculum_probe.py $(ARGS)

phase27-topic-isolation-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_39_topic_isolation_repair.py $(ARGS)

phase27-tokenizer-context-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_40_tokenizer_context_repair.py $(ARGS)

phase27-guarded-runtime-switch:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_41_guarded_runtime_switch.py $(ARGS)

phase27-live-ui-broader-probes:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_42_live_ui_broader_probes.py $(ARGS)

phase27-guarded-data-backed-expansion:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_43_guarded_data_backed_expansion.py $(ARGS)

phase27-tokenizer-curriculum-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_44_tokenizer_curriculum_repair.py $(ARGS)

phase27-semantic-topic-balance-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_45_semantic_topic_balance_repair.py $(ARGS)

phase27-core-dialogue-stabilization:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_46_core_dialogue_stabilization.py $(ARGS)

phase27-new-topic-conditioning-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_47_new_topic_conditioning_repair.py $(ARGS)

phase27-guarded-runtime-switch-47:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_48_guarded_runtime_switch.py $(ARGS)

phase27-broader-live-ui-probes-47:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_49_broader_live_ui_probes.py $(ARGS)

phase27-generator-only-ui-gate:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_50_generator_only_ui_gate.py $(ARGS)

phase27-open-dialogue-generalization-audit:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_51_open_dialogue_generalization_audit.py $(ARGS)

phase27-natural-dialogue-objective-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_52_natural_dialogue_objective_repair.py $(ARGS)

phase27-natural-dialogue-diversity-expansion:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_53_natural_dialogue_diversity_expansion.py $(ARGS)

phase27-capacity-objectivity-gate:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_54_capacity_objectivity_gate.py $(ARGS)

phase27-sf50m-diagnostic-micro-probe:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_55_sf50m_diagnostic_micro_probe.py $(ARGS)

phase27-objective-format-tokenizer-diagnosis:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_56_objective_format_tokenizer_diagnosis.py $(ARGS)

phase27-tokenizer-eval-format-repair-pack:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_57_tokenizer_eval_format_repair_pack.py $(ARGS)

phase27-tokenizer-bounded-alignment-probe:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_58_tokenizer_bounded_alignment_probe.py $(ARGS)

phase27-bounded-alignment-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_59_bounded_alignment_repair.py $(ARGS)

phase27-broader-natural-dialogue-canary:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_60_broader_natural_dialogue_canary.py $(ARGS)

phase27-broader-generalization-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_61_broader_generalization_repair.py $(ARGS)

phase27-family-balance-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_62_family_balance_repair.py $(ARGS)

phase27-interleaved-family-curriculum:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_63_interleaved_family_curriculum.py $(ARGS)

phase27-topic-lexical-tokenizer-inspection:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_64_topic_lexical_tokenizer_inspection.py $(ARGS)

phase27-tokenizer-v8-topic-probe:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_65_tokenizer_v8_topic_probe.py $(ARGS)

phase27-v8-bounded-topic-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_66_v8_bounded_topic_repair.py $(ARGS)

phase27-fresh-shadow-canary:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_67_fresh_shadow_canary.py $(ARGS)

phase27-shadow-failure-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_68_shadow_failure_repair.py $(ARGS)

phase27-new-fresh-shadow-canary:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_69_new_fresh_shadow_canary.py $(ARGS)

phase27-open-social-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_70_open_social_repair.py $(ARGS)

phase27-candidate-selection:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_71_candidate_selection.py $(ARGS)

phase27-stability-first-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_72_stability_first_repair.py $(ARGS)

phase27-open-social-failure-inspection:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_73_open_social_failure_inspection.py $(ARGS)

phase27-open-social-semantic-collapse-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_74_open_social_semantic_collapse_repair.py $(ARGS)

phase27-open-social-strategy-inspection:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_75_open_social_strategy_inspection.py $(ARGS)

phase27-tokenizer-v9-open-social-boundary-probe:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_76_tokenizer_v9_open_social_boundary_probe.py $(ARGS)

phase27-v9-bounded-open-social-lm-repair:
	ENABLE_SAUDI_SEED_V1_LEXICON=true $(PY) scripts/phase27_77_v9_bounded_open_social_lm_repair.py $(ARGS)

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
