"""sf_ai.modules.chat — First active module: general chat.

Phase 4 wires the chat domain end-to-end:
    NLPAnalysis → ChatModule.handle() → ModuleResponse → final text

No LLM. No pretrained model. Responses are built by ChatResponseBuilder
from a small set of well-formed Arabic patterns. Phase 6 will route here
to a SF.AI native LM once one exists.
"""

from sf_ai.modules.chat.conversation_state import ConversationState, ConversationStore
from sf_ai.modules.chat.module import ChatModule, ModuleResponse, get_default_chat_module
from sf_ai.modules.chat.chat_response_builder import ChatResponseBuilder

__all__ = [
    "ChatModule",
    "ChatResponseBuilder",
    "ConversationState",
    "ConversationStore",
    "ModuleResponse",
    "get_default_chat_module",
]
