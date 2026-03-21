"""Example of using TLDV integration in a Cog model."""

import os
from typing import Optional

from cog import BasePredictor, Input

from cog.ext.tldv import TLDVClient, Highlights, Transcript


class Predictor(BasePredictor):
    """Example predictor that uses TLDV API to analyze meetings."""

    def setup(self) -> None:
        """Initialize TLDV client with API key from environment."""
        api_key = os.environ.get("TLDV_API_KEY")
        if not api_key:
            raise ValueError("TLDV_API_KEY environment variable not set")
        self.tldv_client = TLDVClient(api_key=api_key)

    async def predict(
        self,
        meeting_id: str = Input(description="The TLDV meeting ID to analyze"),
        analysis_type: str = Input(
            description="Type of analysis: 'transcript', 'highlights', or 'summary'",
            default="summary",
        ),
    ) -> str:
        """
        Analyze a meeting from TLDV.

        Args:
            meeting_id: ID of the meeting in TLDV
            analysis_type: Type of analysis to perform

        Returns:
            Analysis result as a string
        """
        try:
            if analysis_type == "transcript":
                return await self._get_transcript_analysis(meeting_id)
            elif analysis_type == "highlights":
                return await self._get_highlights(meeting_id)
            else:  # "summary"
                return await self._get_summary(meeting_id)
        except Exception as e:
            return f"Error analyzing meeting: {str(e)}"

    async def _get_transcript_analysis(self, meeting_id: str) -> str:
        """Get and format transcript."""
        transcript = await self.tldv_client.get_transcript(meeting_id)
        if not transcript.entries:
            return "No transcript available for this meeting."

        formatted = "Meeting Transcript:\n\n"
        for entry in transcript.entries:
            minutes = int(entry.timestamp // 60)
            seconds = int(entry.timestamp % 60)
            formatted += f"[{minutes}:{seconds:02d}] {entry.speaker}: {entry.text}\n"

        return formatted

    async def _get_highlights(self, meeting_id: str) -> str:
        """Get meeting highlights."""
        highlights = await self.tldv_client.get_highlights(meeting_id)
        if not highlights.highlights:
            return "No highlights available for this meeting."

        formatted = "Meeting Highlights:\n\n"
        for i, highlight in enumerate(highlights.highlights, 1):
            formatted += f"{i}. {highlight}\n"

        return formatted

    async def _get_summary(self, meeting_id: str) -> str:
        """Get meeting summary combining metadata, highlights, and key points."""
        try:
            meeting = await self.tldv_client.get_meeting(meeting_id)
            highlights = await self.tldv_client.get_highlights(meeting_id)

            summary = f"Meeting Summary\n"
            summary += f"===============\n\n"
            summary += f"Title: {meeting.title}\n"
            summary += f"Platform: {meeting.platform}\n"
            summary += f"Date: {meeting.date}\n"
            summary += f"Duration: {meeting.duration_minutes} minutes\n"
            summary += f"Participants: {', '.join(meeting.participants) if meeting.participants else 'N/A'}\n\n"

            if highlights.highlights:
                summary += "Key Highlights:\n"
                for i, highlight in enumerate(highlights.highlights, 1):
                    summary += f"{i}. {highlight}\n"

            return summary
        except Exception as e:
            return f"Error generating summary: {str(e)}"
