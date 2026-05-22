"""sf_ai.core.composer — final response assembly.

Phase 2 composes Arabic responses that explain the routing decision. Phase 4
will move chat-specific copy into the ChatModule's ChatResponseBuilder; the
Composer keeps only style/format concerns.
"""

from sf_ai.core.composer.response_composer import ComposedReply, ResponseComposer
from sf_ai.core.composer.styles import ResponseStyle

__all__ = ["ComposedReply", "ResponseComposer", "ResponseStyle"]
