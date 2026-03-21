"""Types for TLDV (tl;dv meeting intelligence) integration."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TranscriptEntry(BaseModel):
    """A single entry in a meeting transcript."""

    speaker: str = Field(..., description="Name of the speaker")
    text: str = Field(..., description="Spoken text")
    timestamp: float = Field(..., description="Timestamp in seconds from start of meeting")


class Transcript(BaseModel):
    """Meeting transcript containing entries with speaker and timing information."""

    meeting_id: str = Field(..., description="The ID of the meeting")
    entries: List[TranscriptEntry] = Field(default_factory=list, description="List of transcript entries")


class Highlights(BaseModel):
    """AI-generated highlights from a meeting."""

    meeting_id: str = Field(..., description="The ID of the meeting")
    highlights: List[str] = Field(default_factory=list, description="List of highlight summaries")


class Meeting(BaseModel):
    """Meeting metadata and information from TLDV."""

    id: str = Field(..., description="Unique meeting ID")
    title: str = Field(..., description="Meeting title")
    participants: List[str] = Field(default_factory=list, description="List of participant emails or names")
    duration_minutes: int = Field(..., description="Meeting duration in minutes")
    platform: str = Field(..., description="Platform used (Google Meet, Zoom, or Microsoft Teams)")
    date: datetime = Field(..., description="Meeting date and time")
    recording_url: Optional[str] = Field(None, description="URL to meeting recording if available")
