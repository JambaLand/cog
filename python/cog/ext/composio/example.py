"""Example usage of Composio plugin with TLDV integration."""

from cog import BasePredictor, Input, Output

from cog.ext.composio import ComposioClient, TLDVIntegration


class TLDVTranscriber(BasePredictor):
    """Example predictor that uses TLDV for meeting transcription."""

    def setup(self) -> None:
        """Initialize TLDV integration."""
        # Initialize Composio client (API key from COMPOSIO_API_KEY env var)
        composio_client = ComposioClient()

        # Initialize TLDV integration
        self.tldv = TLDVIntegration(composio_client=composio_client)

    def predict(
        self, recording_id: str = Input(description="TLDV recording ID")
    ) -> Output[str]:
        """
        Get transcript and summary from a TLDV recording.

        Args:
            recording_id: The ID of the TLDV recording to transcribe.

        Returns:
            Formatted transcript and summary.
        """
        try:
            # Get transcript
            transcript_data = self.tldv.get_transcript(recording_id)
            transcript = transcript_data.get("text", "")

            # Get summary
            summary_data = self.tldv.get_summary(recording_id)
            summary = summary_data.get("summary", "")

            # Combine results
            result = f"## Meeting Transcript\n\n{transcript}\n\n## Summary\n\n{summary}"

            return result

        except Exception as e:
            return f"Error retrieving recording: {e}"


class MeetingAnalyzer(BasePredictor):
    """Example predictor that analyzes TLDV meetings."""

    def setup(self) -> None:
        """Initialize TLDV integration."""
        self.tldv = TLDVIntegration()

    def predict(
        self, recording_id: str = Input(description="TLDV recording ID")
    ) -> Output[dict]:
        """
        Analyze a meeting and extract action items.

        Args:
            recording_id: The ID of the TLDV recording to analyze.

        Returns:
            Dictionary with meeting details and action items.
        """
        try:
            # Get meeting details
            details = self.tldv.get_meeting_details(recording_id)

            # Create action items
            action_items = self.tldv.create_action_items(recording_id)

            return {
                "meeting_details": details,
                "action_items": action_items,
                "status": "success",
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}
