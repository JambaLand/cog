# TLDV Integration

This document describes how to use the Cog TLDV extension to integrate with the [tl;dv](https://tldv.io) API for meeting intelligence.

## Overview

[tl;dv](https://tldv.io) is a meeting intelligence platform that captures, transcribes, and analyzes meetings across Google Meet, Zoom, and Microsoft Teams. The Cog TLDV extension provides a Python client to programmatically access meeting data, transcripts, and AI-generated highlights.

## Prerequisites

- **tl;dv Account**: You need a Business or Enterprise tl;dv account
- **tl;dv API Key**: Get your API key from [tl;dv settings](https://tldv.io/app/settings/personal-settings/api-keys)
- **Cog**: Version with TLDV extension support

## Installation

No additional installation is needed. The TLDV extension is built-in to the Cog SDK.

## Configuration

### Setting the API Key

You need to provide your TLDV API key to your Cog model. This is typically done via environment variables in your `cog.yaml`:

```yaml
# cog.yaml
build:
  python_version: "3.11"

predict: predict.py

environment:
  - TLDV_API_KEY
```

When running predictions, set the environment variable:

```bash
export TLDV_API_KEY="your-api-key-here"
cog predict -i meeting_id="meeting123"
```

## Basic Usage

### Importing the Extension

```python
from cog.ext.tldv import TLDVClient, Meeting, Transcript, Highlights
```

### Creating a Client

```python
from cog import BasePredictor
from cog.ext.tldv import TLDVClient
import os

class Predictor(BasePredictor):
    def setup(self) -> None:
        api_key = os.environ.get("TLDV_API_KEY")
        self.tldv_client = TLDVClient(api_key=api_key)
```

## API Methods

### List Meetings

Retrieve meetings with optional filters:

```python
meetings = await self.tldv_client.list_meetings(
    query="project planning",  # Optional search query
    date_from="2024-01-01",    # Optional start date (ISO format)
    date_to="2024-12-31",      # Optional end date (ISO format)
    participation="all",        # Optional participation filter
    meeting_type="standup"     # Optional meeting type filter
)

for meeting in meetings:
    print(f"{meeting.title} on {meeting.date}")
    print(f"Duration: {meeting.duration_minutes} minutes")
    print(f"Platform: {meeting.platform}")
```

### Get Meeting Metadata

Retrieve detailed information about a specific meeting:

```python
meeting = await self.tldv_client.get_meeting(meeting_id="meeting123")
print(f"Title: {meeting.title}")
print(f"Participants: {', '.join(meeting.participants)}")
print(f"Platform: {meeting.platform}")
print(f"Date: {meeting.date}")
print(f"Duration: {meeting.duration_minutes} minutes")
```

### Get Transcript

Retrieve the full transcript of a meeting:

```python
transcript = await self.tldv_client.get_transcript(meeting_id="meeting123")

for entry in transcript.entries:
    minutes = int(entry.timestamp // 60)
    seconds = int(entry.timestamp % 60)
    print(f"[{minutes}:{seconds:02d}] {entry.speaker}: {entry.text}")
```

### Get Highlights

Retrieve AI-generated highlights from a meeting:

```python
highlights = await self.tldv_client.get_highlights(meeting_id="meeting123")

for highlight in highlights.highlights:
    print(f"• {highlight}")
```

## Complete Example

Here's a complete example of a Cog predictor that analyzes a TLDV meeting:

```python
from cog import BasePredictor, Input
from cog.ext.tldv import TLDVClient
import os

class Predictor(BasePredictor):
    def setup(self) -> None:
        api_key = os.environ.get("TLDV_API_KEY")
        if not api_key:
            raise ValueError("TLDV_API_KEY environment variable not set")
        self.tldv_client = TLDVClient(api_key=api_key)

    async def predict(
        self,
        meeting_id: str = Input(description="The TLDV meeting ID"),
        analysis_type: str = Input(
            description="Type: 'transcript', 'highlights', or 'summary'",
            default="summary",
        ),
    ) -> str:
        if analysis_type == "transcript":
            transcript = await self.tldv_client.get_transcript(meeting_id)
            result = "Meeting Transcript:\n\n"
            for entry in transcript.entries:
                result += f"{entry.speaker}: {entry.text}\n"
            return result

        elif analysis_type == "highlights":
            highlights = await self.tldv_client.get_highlights(meeting_id)
            result = "Meeting Highlights:\n\n"
            for highlight in highlights.highlights:
                result += f"• {highlight}\n"
            return result

        else:  # summary
            meeting = await self.tldv_client.get_meeting(meeting_id)
            highlights = await self.tldv_client.get_highlights(meeting_id)

            result = f"Meeting: {meeting.title}\n"
            result += f"Platform: {meeting.platform}\n"
            result += f"Duration: {meeting.duration_minutes} minutes\n\n"
            result += "Highlights:\n"
            for highlight in highlights.highlights:
                result += f"• {highlight}\n"
            return result
```

## Data Types

### Meeting

Represents a meeting with metadata:

- `id: str` - Unique meeting ID
- `title: str` - Meeting title
- `participants: List[str]` - List of participant emails or names
- `duration_minutes: int` - Duration in minutes
- `platform: str` - Platform used (Google Meet, Zoom, or Microsoft Teams)
- `date: datetime` - Meeting date and time
- `recording_url: Optional[str]` - URL to recording if available

### Transcript

Contains the full transcript of a meeting:

- `meeting_id: str` - The meeting ID
- `entries: List[TranscriptEntry]` - List of transcript entries

### TranscriptEntry

A single line in the transcript:

- `speaker: str` - Name of the speaker
- `text: str` - Spoken text
- `timestamp: float` - Timestamp in seconds from start of meeting

### Highlights

AI-generated highlights from a meeting:

- `meeting_id: str` - The meeting ID
- `highlights: List[str]` - List of highlight summaries

## Error Handling

The TLDV client raises `RuntimeError` for API errors. Always wrap API calls in try-except blocks:

```python
from cog import BasePredictor
from cog.ext.tldv import TLDVClient
import os

class Predictor(BasePredictor):
    def setup(self) -> None:
        self.tldv_client = TLDVClient(api_key=os.environ["TLDV_API_KEY"])

    async def predict(self, meeting_id: str = Input()) -> str:
        try:
            transcript = await self.tldv_client.get_transcript(meeting_id)
            return f"Got transcript with {len(transcript.entries)} entries"
        except RuntimeError as e:
            return f"Error: {str(e)}"
        except ValueError as e:
            return f"Configuration error: {str(e)}"
```

## Running the Example

A complete example is available in `examples/tldv_integration/`:

```bash
cd examples/tldv_integration
export TLDV_API_KEY="your-api-key"
cog predict -i meeting_id="your-meeting-id" -i analysis_type="summary"
```

## Limitations and Future Features

- **Import Meeting**: The ability to import meetings via URL is coming soon to the TLDV API
- **Rate Limiting**: Check TLDV API documentation for rate limits on your account tier
- **Data Retention**: Transcripts and highlights availability depends on your TLDV subscription

## Support

For issues with the TLDV extension, check:
- [TLDV Documentation](https://tldv.io/docs)
- [TLDV API Status](https://status.tldv.io)
- [Cog GitHub Issues](https://github.com/replicate/cog/issues)

## License

The TLDV extension is part of Cog and follows the same license terms.
