# Composio Plugin for Cog

This plugin integrates Cog with [Composio](https://composio.dev), providing access to 1000+ third-party applications and services, including **TLDV** for meeting transcription and recording.

## Features

- 🔌 **1000+ App Integrations**: Access to Composio's extensive app catalog
- 🎯 **TLDV Integration**: Built-in support for TLDV meeting recordings and transcription
- 🔐 **Secure Authentication**: Composio handles authentication across all supported apps
- 🚀 **Easy to Use**: Simple Python API for executing actions in integrated apps

## Installation

### 1. Install Composio Package

```bash
pip install composio
```

### 2. Get Your Composio API Key

1. Visit [platform.composio.dev](https://platform.composio.dev)
2. Sign up or log in to your account
3. Generate an API key from the dashboard
4. Copy your API key

### 3. Set Up Environment

```bash
export COMPOSIO_API_KEY="your-api-key-here"
```

Or pass it directly when initializing the client.

## Quick Start

### Using TLDV

```python
from cog import BasePredictor, Input, Output
from cog.ext.composio import TLDVIntegration

class MeetingTranscriber(BasePredictor):
    def setup(self):
        self.tldv = TLDVIntegration()

    def predict(self, recording_id: str = Input()) -> Output[str]:
        # Get transcript
        transcript = self.tldv.get_transcript(recording_id)
        
        # Get summary
        summary = self.tldv.get_summary(recording_id)
        
        return f"Transcript: {transcript}\n\nSummary: {summary}"
```

### Using Other Composio Apps

```python
from cog.ext.composio import ComposioClient

class APIIntegration(BasePredictor):
    def setup(self):
        self.composio = ComposioClient()
        # List available apps
        apps = self.composio.get_available_apps()
        print(f"Available apps: {apps}")

    def predict(self, action: str = Input()) -> Output[str]:
        # Execute action in any app
        result = self.composio.execute_action(
            app_name="slack",
            action="send_message",
            params={"channel": "#general", "message": "Hello from Cog!"}
        )
        return result
```

## API Reference

### ComposioClient

Main client for interacting with Composio.

#### Methods

- `get_available_apps() -> list[str]`: List all available apps
- `get_app_actions(app_name: str) -> list[str]`: List actions for a specific app
- `authenticate_app(app_name: str, credentials: Dict) -> Dict`: Authenticate with an app
- `execute_action(app_name: str, action: str, params: Dict) -> Dict`: Execute an action

### TLDVIntegration

Specialized integration for TLDV.

#### Methods

- `get_recordings(**params) -> Dict`: Get list of recordings
- `get_transcript(recording_id: str) -> Dict`: Get meeting transcript
- `get_summary(recording_id: str) -> Dict`: Get AI summary of meeting
- `get_meeting_details(recording_id: str) -> Dict`: Get detailed meeting info
- `create_action_items(recording_id: str) -> Dict`: Extract action items
- `share_recording(recording_id: str, email: str) -> Dict`: Share recording

## Examples

See `example.py` for complete working examples of:
- `TLDVTranscriber`: Get transcripts from TLDV recordings
- `MeetingAnalyzer`: Analyze meetings and extract action items

## Troubleshooting

### "COMPOSIO_API_KEY not provided"
Make sure to set the environment variable or pass the API key to the client:
```python
client = ComposioClient(api_key="your-key")
```

### "composio package is required"
Install the Composio package:
```bash
pip install composio
```

### "TLDV is not available"
Ensure your Composio API key has access to TLDV. Check your account on platform.composio.dev.

## More Information

- [Composio Documentation](https://docs.composio.dev)
- [TLDV Documentation](https://docs.tldv.io)
- [Cog Documentation](https://github.com/replicate/cog)

## License

Same as Cog - see LICENSE file in the root of the repository.
