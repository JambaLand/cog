"""TLDV API client for accessing meeting intelligence."""

import json
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .types import Highlights, Meeting, Transcript, TranscriptEntry


class TLDVClient:
    """Client for interacting with the TLDV (tl;dv) API."""

    def __init__(self, api_key: str, base_url: str = "https://api.tldv.io") -> None:
        """
        Initialize TLDV client.

        Args:
            api_key: TLDV API key for authentication
            base_url: Base URL for TLDV API (defaults to production)

        Raises:
            ValueError: If api_key is empty or None
        """
        if not api_key:
            raise ValueError("TLDV_API_KEY environment variable must be set")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make HTTP request to TLDV API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters for the request

        Returns:
            Parsed JSON response

        Raises:
            RuntimeError: If API request fails
        """
        url = f"{self.base_url}{endpoint}"

        # Add query parameters if provided
        if params:
            query_string = urlencode(params)
            url = f"{url}?{query_string}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "cog-tldv-client/1.0",
        }

        try:
            request = Request(url, headers=headers, method=method)
            with urlopen(request) as response:
                data = response.read()
                return json.loads(data.decode("utf-8"))
        except HTTPError as e:
            error_msg = e.read().decode("utf-8")
            raise RuntimeError(f"TLDV API error ({e.code}): {error_msg}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to communicate with TLDV API: {str(e)}") from e

    async def list_meetings(
        self,
        query: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        participation: Optional[str] = None,
        meeting_type: Optional[str] = None,
    ) -> List[Meeting]:
        """
        List meetings with optional filters.

        Args:
            query: Search query for meeting titles
            date_from: Start date filter (ISO format)
            date_to: End date filter (ISO format)
            participation: Filter by participation status
            meeting_type: Filter by meeting type

        Returns:
            List of Meeting objects
        """
        params: Dict[str, Any] = {}
        if query:
            params["query"] = query
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        if participation:
            params["participation"] = participation
        if meeting_type:
            params["type"] = meeting_type

        response = self._make_request("GET", "/meetings", params)

        meetings = []
        if isinstance(response, dict) and "meetings" in response:
            for meeting_data in response.get("meetings", []):
                meetings.append(self._parse_meeting(meeting_data))
        elif isinstance(response, list):
            for meeting_data in response:
                meetings.append(self._parse_meeting(meeting_data))

        return meetings

    async def get_meeting(self, meeting_id: str) -> Meeting:
        """
        Get detailed metadata for a specific meeting.

        Args:
            meeting_id: ID of the meeting

        Returns:
            Meeting object with metadata

        Raises:
            RuntimeError: If meeting not found or API error occurs
        """
        response = self._make_request("GET", f"/meetings/{meeting_id}")
        return self._parse_meeting(response)

    async def get_transcript(self, meeting_id: str) -> Transcript:
        """
        Get transcript for a specific meeting.

        Args:
            meeting_id: ID of the meeting

        Returns:
            Transcript object with entries

        Raises:
            RuntimeError: If transcript not found or API error occurs
        """
        response = self._make_request("GET", f"/meetings/{meeting_id}/transcript")

        entries = []
        if isinstance(response, dict) and "transcript" in response:
            transcript_data = response["transcript"]
        else:
            transcript_data = response

        if isinstance(transcript_data, list):
            for entry_data in transcript_data:
                entries.append(self._parse_transcript_entry(entry_data))

        return Transcript(meeting_id=meeting_id, entries=entries)

    async def get_highlights(self, meeting_id: str) -> Highlights:
        """
        Get AI-generated highlights for a specific meeting.

        Args:
            meeting_id: ID of the meeting

        Returns:
            Highlights object with list of highlights

        Raises:
            RuntimeError: If highlights not found or API error occurs
        """
        response = self._make_request("GET", f"/meetings/{meeting_id}/highlights")

        highlights_list = []
        if isinstance(response, dict):
            if "highlights" in response:
                highlights_data = response["highlights"]
                if isinstance(highlights_data, list):
                    highlights_list = highlights_data
            elif "summary" in response:
                # Alternative structure
                highlights_list = [response["summary"]]
        elif isinstance(response, list):
            highlights_list = response

        return Highlights(meeting_id=meeting_id, highlights=highlights_list)

    @staticmethod
    def _parse_meeting(data: Dict[str, Any]) -> Meeting:
        """Parse meeting data from API response."""
        return Meeting(
            id=data.get("id", ""),
            title=data.get("title", ""),
            participants=data.get("participants", []),
            duration_minutes=int(data.get("duration", 0) / 60) if data.get("duration") else 0,
            platform=data.get("platform", ""),
            date=data.get("date", data.get("createdAt", "")),
            recording_url=data.get("recordingUrl"),
        )

    @staticmethod
    def _parse_transcript_entry(data: Dict[str, Any]) -> TranscriptEntry:
        """Parse transcript entry from API response."""
        return TranscriptEntry(
            speaker=data.get("speaker", "Unknown"),
            text=data.get("text", ""),
            timestamp=float(data.get("timestamp", 0)),
        )
