"""ElevenLabs Conversational AI Agent Predictor for Cog."""

import os
from typing import Generator

from cog import BasePredictor

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import (
    DefaultAudioInterface,
)


class Predictor(BasePredictor):
    """Conversational AI predictor using ElevenLabs Agent."""

    def setup(self) -> None:
        """Initialize the ElevenLabs client."""
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise ValueError(
                "ELEVENLABS_API_KEY environment variable is required"
            )
        self.client = ElevenLabs(api_key=api_key)
        self.conversation_id: str | None = None

    def predict(
        self,
        agent_id: str = "agent_0201kjywpmreevjtt20xac516ww5",
        custom_instructions: str | None = None,
    ) -> Generator[str, None, None]:
        """Start a conversation with the ElevenLabs agent.

        Args:
            agent_id: ID of the ElevenLabs agent to use.
            custom_instructions: Optional custom system instructions.

        Yields:
            Status messages and conversation updates.
        """
        yield f"🎤 Starting conversation with agent: {agent_id}"

        try:
            # Create conversation
            conversation = Conversation(
                self.client,
                agent_id=agent_id,
                requires_auth=False,
                audio_interface=DefaultAudioInterface(),
            )

            # Set custom instructions if provided
            if custom_instructions:
                yield f"📝 Using custom instructions: {custom_instructions}"

            # Start session
            yield "🔗 Connecting to ElevenLabs..."
            conversation.start_session()
            yield "✓ Connected! Speak to interact with the agent."

            # Wait for session to end
            yield "⏳ Conversation in progress... (Press Ctrl+C to exit)"
            self.conversation_id = conversation.wait_for_session_end()

            yield f"✓ Conversation ended"
            yield f"📊 Conversation ID: {self.conversation_id}"

        except KeyboardInterrupt:
            yield "⏹️  Conversation interrupted by user"
        except Exception as e:
            yield f"❌ Error: {str(e)}"
            raise
