"""sf_ai.modules.chat — First active module: general chat.

Phase 4 wires the chat domain end-to-end:
    NLPAnalysis → ChatModule.handle() → ModuleResponse → final text

No external LLM. No pretrained model. Responses are built by
ChatResponseBuilder from a small set of well-formed Arabic patterns. Phase 15
adds a native-generator adapter, but runtime generation stays disabled until
evaluation approves it.
"""

from sf_ai.modules.chat.conversation_state import ConversationState, ConversationStore
from sf_ai.modules.chat.generation_policy import GenerationDecision, GenerationPolicy
from sf_ai.modules.chat.module import ChatModule, ModuleResponse, get_default_chat_module
from sf_ai.modules.chat.native_generator import (
    NativeGenerationResult,
    NativeGenerator,
    NativeGeneratorConfig,
    NativeGeneratorStatus,
)
from sf_ai.modules.chat.chat_response_builder import ChatResponseBuilder

__all__ = [
    "ChatModule",
    "ChatResponseBuilder",
    "ConversationState",
    "ConversationStore",
    "GenerationDecision",
    "GenerationPolicy",
    "ModuleResponse",
    "NativeGenerationResult",
    "NativeGenerator",
    "NativeGeneratorConfig",
    "NativeGeneratorStatus",
    "get_default_chat_module",
]
