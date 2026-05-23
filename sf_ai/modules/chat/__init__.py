"""sf_ai.modules.chat — First active module: general chat.

Phase 4 wires the chat domain end-to-end:
    NLPAnalysis → ChatModule.handle() → ModuleResponse → final text

No external LLM. No pretrained model. Responses are built by
ChatResponseBuilder from a small set of well-formed Arabic patterns. Phase 15
adds a native-generator adapter, but runtime generation stays disabled until
evaluation approves it.
"""

from sf_ai.modules.chat.chat_response_builder import ChatResponseBuilder
from sf_ai.modules.chat.context_builder import BuiltContext, ContextBuilder, LocalContextSnippet
from sf_ai.modules.chat.conversation_state import ConversationState, ConversationStore
from sf_ai.modules.chat.generation_guard import GenerationGuard, GenerationGuardVerdict
from sf_ai.modules.chat.generation_policy import GenerationDecision, GenerationPolicy
from sf_ai.modules.chat.module import ChatModule, ModuleResponse, get_default_chat_module
from sf_ai.modules.chat.native_generator import (
    NativeGenerationResult,
    NativeGenerator,
    NativeGeneratorConfig,
    NativeGeneratorStatus,
)
from sf_ai.modules.chat.rag_bridge import ChatRagBridge, RagBridgeConfig

__all__ = [
    "ChatModule",
    "ChatRagBridge",
    "ChatResponseBuilder",
    "ConversationState",
    "ConversationStore",
    "BuiltContext",
    "ContextBuilder",
    "GenerationDecision",
    "GenerationGuard",
    "GenerationGuardVerdict",
    "GenerationPolicy",
    "LocalContextSnippet",
    "ModuleResponse",
    "NativeGenerationResult",
    "NativeGenerator",
    "NativeGeneratorConfig",
    "NativeGeneratorStatus",
    "RagBridgeConfig",
    "get_default_chat_module",
]
