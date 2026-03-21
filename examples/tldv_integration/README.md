# TLDV Integration Example

This example demonstrates how to use the Cog TLDV extension to integrate with the tl;dv API for meeting intelligence.

## Quick Start

### 1. Setup API Key

First, get your TLDV API key from [tl;dv settings](https://tldv.io/app/settings/personal-settings/api-keys).

Run the setup script from the project root:

```bash
cd ../..
script/setup-tldv
```

This will:
- Prompt you for your TLDV API key
- Create a `.env` file with your configuration
- Test the connection to verify it works

### 2. Build the Model

```bash
cog build
```

### 3. Make Predictions

Get a transcript from a meeting:

```bash
export TLDV_API_KEY="your-api-key-here"
cog predict -i meeting_id="your-meeting-id"
```

Or analyze highlights:

```bash
cog predict \
  -i meeting_id="your-meeting-id" \
  -i analysis_type="highlights"
```

## Features

The example predictor supports three analysis types:

### 1. Transcript Analysis
Get the full transcript of a meeting with timestamps:

```bash
cog predict \
  -i meeting_id="meeting123" \
  -i analysis_type="transcript"
```

Output:
```
Meeting Transcript:

[0:15] John Smith: Let's discuss the project timeline
[1:30] Jane Doe: I agree, we need to accelerate the schedule
[2:45] John Smith: What resources do we need?
...
```

### 2. Highlights
Get AI-generated highlights from the meeting:

```bash
cog predict \
  -i meeting_id="meeting123" \
  -i analysis_type="highlights"
```

Output:
```
Meeting Highlights:

1. Project timeline needs to be accelerated
2. Additional resources required for Q2
3. Decision made to review scope next week
...
```

### 3. Summary (Default)
Get a comprehensive summary with metadata and highlights:

```bash
cog predict \
  -i meeting_id="meeting123" \
  -i analysis_type="summary"
```

Output:
```
Meeting Summary
===============

Title: Q1 Planning Session
Platform: Google Meet
Date: 2024-03-20 14:00:00
Duration: 60 minutes
Participants: john@company.com, jane@company.com

Key Highlights:
1. Project timeline needs to be accelerated
2. Additional resources required for Q2
3. Decision made to review scope next week
...
```

## Environment Variables

The model requires:

- `TLDV_API_KEY` - Your tl;dv API key (required)

Set it before running predictions:

```bash
export TLDV_API_KEY="your-api-key-here"
```

Or let the setup script handle it automatically.

## Understanding the Code

### predict.py

The predictor uses the `TLDVClient` from the Cog TLDV extension:

```python
from cog.ext.tldv import TLDVClient

# Initialize the client
client = TLDVClient(api_key=os.environ["TLDV_API_KEY"])

# Get meeting transcript
transcript = await client.get_transcript(meeting_id)

# Get meeting metadata
meeting = await client.get_meeting(meeting_id)

# Get highlights
highlights = await client.get_highlights(meeting_id)
```

All methods are asynchronous - use `await` when calling them.

## Available Data Types

The extension provides Pydantic models for type safety:

- `Meeting` - Metadata about a meeting (title, date, participants, platform, etc.)
- `Transcript` - Full transcript with timestamped entries
- `TranscriptEntry` - Individual transcript line (speaker, text, timestamp)
- `Highlights` - AI-generated meeting highlights

## Troubleshooting

### API Key Error
If you get "TLDV_API_KEY environment variable not set", make sure:
1. You ran `script/setup-tldv` from the project root
2. The `.env` file was created with your API key
3. You're running predictions from the same directory or with the env var exported

### Connection Error
If you get connection errors:
1. Verify your API key is correct
2. Check your internet connection
3. Visit [tl;dv status](https://status.tldv.io) to check service health

### Invalid Meeting ID
If a meeting is not found:
1. Double-check the meeting ID is correct
2. Verify the meeting is accessible from your TLDV account
3. Check the meeting hasn't expired or been deleted

## More Information

For complete documentation, see:
- [`docs/tldv.md`](../../docs/tldv.md) - Complete TLDV integration guide
- [`python/cog/ext/tldv/`](../../python/cog/ext/tldv/) - Extension source code

## Next Steps

1. **Customize the prediction logic** - Modify `predict.py` to process meeting data your way
2. **Add more analysis** - Use meeting transcripts with your AI models
3. **Integrate with other tools** - Combine TLDV data with other Cog features

Happy analyzing meetings! 📊
