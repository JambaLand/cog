"""TLDV (tl;dv meeting intelligence) integration for Cog.

This module provides integration with the TLDV API to access meeting intelligence
from Google Meet, Zoom, and Microsoft Teams.

Example usage:
    from cog import BasePredictor, Input
    from cog.ext.tldv import TLDVClient, Transcript
    import os

    class Predictor(BasePredictor):
        def setup(self) -> None:
            self.tldv_client = TLDVClient(api_key=os.environ["TLDV_API_KEY"])

        def predict(self, meeting_id: str = Input()) -> str:
            # Get transcript from TLDV
            transcript = await self.tldv_client.get_transcript(meeting_id)
            # Process transcript...
            return "Processed result"
"""

from .client import TLDVClient
from .types import Highlights, Meeting, Transcript, TranscriptEntry

__all__ = [
    "TLDVClient",
    "Meeting",
    "Transcript",
    "TranscriptEntry",
    "Highlights",
]
