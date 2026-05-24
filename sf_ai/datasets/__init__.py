"""sf_ai.datasets — dialogue dataset pipeline (Phase 5).

This package handles **input** only. It does not train, fetch, or generate
data. The user is responsible for placing dialogue files under
`data/corpus/chat/raw/` with documented provenance.

Public surface:
    Schemas       — ChatMessage, SimpleSample, StructuredSample, Provenance
    Validators    — validate_record, validate_jsonl_file
    Cleaners      — SampleCleaner (whitespace, control chars, optional NFC)
    Loaders       — iter_jsonl, iter_chat_samples
    ChatDataset   — high-level wrapper that combines the three
"""

from sf_ai.datasets.chat_dataset import ChatDataset, DatasetStats
from sf_ai.datasets.cleaners import SampleCleaner
from sf_ai.datasets.corpus_governance import (
    CorpusGovernanceReport,
    audit_jsonl_directory_for_training,
    audit_jsonl_file_for_training,
    audit_record_for_training,
    detect_training_forbidden_operational_terms,
)
from sf_ai.datasets.loaders import iter_chat_samples, iter_jsonl
from sf_ai.datasets.saudi_seed import (
    SaudiSeedEntry,
    SaudiSeedSafety,
    SaudiSeedStats,
    iter_saudi_seed_entries,
    load_saudi_seed,
    saudi_seed_stats,
)
from sf_ai.datasets.saudi_seed import (
    attribution_block as saudi_seed_attribution,
)
from sf_ai.datasets.schemas import (
    ChatMessage,
    Provenance,
    SampleType,
    SimpleSample,
    StructuredSample,
    parse_record,
)
from sf_ai.datasets.source_inventory import (
    SourceInventoryItem,
    SourceInventoryReport,
    build_source_inventory,
)
from sf_ai.datasets.splits import (
    FAMILY_ORDER,
    SplitEntry,
    assign_split,
    build_split_entries,
    iter_split_samples,
    iter_split_samples_round_robin_by_family,
    load_split_entries,
    write_split_manifest,
)
from sf_ai.datasets.validators import (
    SampleIssue,
    ValidationReport,
    validate_jsonl_file,
    validate_record,
)

__all__ = [
    "ChatDataset",
    "ChatMessage",
    "CorpusGovernanceReport",
    "DatasetStats",
    "Provenance",
    "SampleCleaner",
    "SampleIssue",
    "SampleType",
    "SimpleSample",
    "StructuredSample",
    "SaudiSeedEntry",
    "SaudiSeedSafety",
    "SaudiSeedStats",
    "SourceInventoryItem",
    "SourceInventoryReport",
    "FAMILY_ORDER",
    "SplitEntry",
    "ValidationReport",
    "assign_split",
    "build_split_entries",
    "iter_chat_samples",
    "iter_jsonl",
    "iter_saudi_seed_entries",
    "iter_split_samples",
    "iter_split_samples_round_robin_by_family",
    "load_split_entries",
    "load_saudi_seed",
    "parse_record",
    "audit_jsonl_directory_for_training",
    "audit_jsonl_file_for_training",
    "audit_record_for_training",
    "detect_training_forbidden_operational_terms",
    "saudi_seed_attribution",
    "saudi_seed_stats",
    "build_source_inventory",
    "validate_jsonl_file",
    "validate_record",
    "write_split_manifest",
]
