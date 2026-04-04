"""TLDV (TL;DV) integration for Cog via Composio."""

from typing import Any, Dict, Optional

from .client import ComposioClient


class TLDVIntegration:
    """Integration with TLDV (TL;DV) for meeting transcription and recording."""

    TLDV_APP_NAME = "tldv"

    def __init__(
        self,
        composio_client: Optional[ComposioClient] = None,
        api_key: Optional[str] = None,
    ) -> None:
        """
        Initialize TLDV integration.

        Args:
            composio_client: Existing ComposioClient instance. If not provided,
                a new one will be created using api_key.
            api_key: Composio API key if composio_client is not provided.
        """
        self.client = composio_client or ComposioClient(api_key=api_key)
        self._verify_tldv_available()

    def _verify_tldv_available(self) -> None:
        """Verify that TLDV is available in Composio."""
        try:
            available_apps = self.client.get_available_apps()
            if self.TLDV_APP_NAME not in available_apps:
                raise RuntimeError(
                    f"TLDV is not available in Composio. "
                    f"Available apps: {', '.join(available_apps[:10])}..."
                )
        except Exception as e:
            raise RuntimeError(f"Failed to verify TLDV availability: {e}")

    def get_available_actions(self) -> list[str]:
        """Get available TLDV actions."""
        return self.client.get_app_actions(self.TLDV_APP_NAME)

    def authenticate(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        """
        Authenticate with TLDV.

        Args:
            credentials: TLDV credentials (typically API key).

        Returns:
            Authentication response.
        """
        return self.client.authenticate_app(self.TLDV_APP_NAME, credentials)

    def get_recordings(self, **params: Any) -> Dict[str, Any]:
        """
        Get list of TLDV recordings.

        Args:
            **params: Additional parameters for the API call.

        Returns:
            List of recordings.
        """
        return self.client.execute_action(
            self.TLDV_APP_NAME, "get_recordings", params
        )

    def get_transcript(
        self, recording_id: str, **params: Any
    ) -> Dict[str, Any]:
        """
        Get transcript for a TLDV recording.

        Args:
            recording_id: ID of the recording.
            **params: Additional parameters.

        Returns:
            Transcript data.
        """
        params["recording_id"] = recording_id
        return self.client.execute_action(
            self.TLDV_APP_NAME, "get_transcript", params
        )

    def get_summary(self, recording_id: str, **params: Any) -> Dict[str, Any]:
        """
        Get AI-generated summary of a TLDV recording.

        Args:
            recording_id: ID of the recording.
            **params: Additional parameters.

        Returns:
            Summary data.
        """
        params["recording_id"] = recording_id
        return self.client.execute_action(
            self.TLDV_APP_NAME, "get_summary", params
        )

    def get_meeting_details(
        self, recording_id: str, **params: Any
    ) -> Dict[str, Any]:
        """
        Get detailed information about a TLDV meeting.

        Args:
            recording_id: ID of the recording.
            **params: Additional parameters.

        Returns:
            Meeting details.
        """
        params["recording_id"] = recording_id
        return self.client.execute_action(
            self.TLDV_APP_NAME, "get_meeting_details", params
        )

    def create_action_items(
        self, recording_id: str, **params: Any
    ) -> Dict[str, Any]:
        """
        Create action items from a TLDV recording.

        Args:
            recording_id: ID of the recording.
            **params: Additional parameters.

        Returns:
            Created action items.
        """
        params["recording_id"] = recording_id
        return self.client.execute_action(
            self.TLDV_APP_NAME, "create_action_items", params
        )

    def share_recording(
        self, recording_id: str, email: str, **params: Any
    ) -> Dict[str, Any]:
        """
        Share a TLDV recording with someone.

        Args:
            recording_id: ID of the recording.
            email: Email address to share with.
            **params: Additional parameters.

        Returns:
            Share response.
        """
        params["recording_id"] = recording_id
        params["email"] = email
        return self.client.execute_action(
            self.TLDV_APP_NAME, "share_recording", params
        )
