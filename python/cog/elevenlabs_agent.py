"""ElevenLabs Conversational AI Agent Integration for Cog."""

import os
from typing import Any, Generator

try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs.conversational_ai.conversation import Conversation
except ImportError:
    raise ImportError(
        "Please install elevenlabs: pip install 'elevenlabs[pyaudio]'"
    )


class ElevenLabsAgent:
    """Wrapper for ElevenLabs Conversational AI Agent."""

    def __init__(
        self,
        agent_id: str = "agent_0201kjywpmreevjtt20xac516ww5",
        api_key: str | None = None,
    ) -> None:
        """Initialize ElevenLabs Agent.

        Args:
            agent_id: The ID of the ElevenLabs agent to use.
            api_key: ElevenLabs API key. If None, uses ELEVENLABS_API_KEY env var.
        """
        self.agent_id = agent_id
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")

        if not self.api_key:
            raise ValueError(
                "ELEVENLABS_API_KEY not found. "
                "Set it as environment variable or pass as argument."
            )

        self.client = ElevenLabs(api_key=self.api_key)
        self.conversation: Conversation | None = None
        self.conversation_id: str | None = None

    def start_conversation(self) -> dict[str, Any]:
        """Start a new conversation session.

        Returns:
            Dictionary with conversation status and ID.
        """
        from elevenlabs.conversational_ai.default_audio_interface import (
            DefaultAudioInterface,
        )

        self.conversation = Conversation(
            self.client,
            agent_id=self.agent_id,
            requires_auth=False,
            audio_interface=DefaultAudioInterface(),
        )

        self.conversation.start_session()

        return {
            "status": "started",
            "agent_id": self.agent_id,
            "message": "Conversation started. Speak to interact with the agent.",
        }

    def end_conversation(self) -> dict[str, Any]:
        """End the current conversation session.

        Returns:
            Dictionary with conversation status and ID.
        """
        if self.conversation is None:
            return {"status": "error", "message": "No active conversation"}

        try:
            self.conversation_id = self.conversation.wait_for_session_end()
            return {
                "status": "ended",
                "conversation_id": self.conversation_id,
                "message": "Conversation ended successfully.",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_conversation_id(self) -> str | None:
        """Get the ID of the current conversation."""
        return self.conversation_id

    def is_active(self) -> bool:
        """Check if conversation is active."""
        return self.conversation is not None and self.conversation_id is None


def create_elevenlabs_predictor(
    agent_id: str = "agent_0201kjywpmreevjtt20xac516ww5",
) -> type:
    """Factory function to create a Cog predictor for ElevenLabs Agent.

    Args:
        agent_id: The ElevenLabs agent ID to use.

    Returns:
        A Cog Predictor class configured with the given agent ID.
    """

    from cog import BasePredictor

    class ElevenLabsPredictor(BasePredictor):
        """Cog predictor for ElevenLabs Conversational AI Agent."""

        def setup(self) -> None:
            """Set up the ElevenLabs agent."""
            self.agent = ElevenLabsAgent(agent_id=agent_id)

        def predict(
            self, mode: str = "interactive"
        ) -> Generator[str, None, None]:
            """Run ElevenLabs agent conversation.

            Args:
                mode: Either 'interactive' for real-time conversation
                      or 'batch' for non-interactive mode.

            Yields:
                Status messages about the conversation.
            """
            if mode == "interactive":
                yield "Starting interactive conversation with ElevenLabs agent..."

                status = self.agent.start_conversation()
                yield f"Status: {status['message']}"

                try:
                    # Wait for conversation to complete
                    result = self.agent.end_conversation()
                    yield f"Result: {result['message']}"

                    if result["status"] == "ended":
                        yield f"Conversation ID: {result['conversation_id']}"
                except KeyboardInterrupt:
                    yield "Conversation interrupted by user."
                except Exception as e:
                    yield f"Error: {str(e)}"
            else:
                yield "Batch mode not yet implemented for ElevenLabs agent."

    return ElevenLabsPredictor
