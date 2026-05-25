"""Local reference-layer adapters.

Reference layers are not training corpora and are not runtime chat features by
default. They expose local, inspectable helper contracts that stay gated until a
phase explicitly allows wiring.
"""

from sf_ai.reference_layers.sinalab_synonyms import (
    SinaLabSynonymsReferenceAdapter,
    SynonymLookupResult,
    SynonymReferenceRecord,
)

__all__ = [
    "SinaLabSynonymsReferenceAdapter",
    "SynonymLookupResult",
    "SynonymReferenceRecord",
]
