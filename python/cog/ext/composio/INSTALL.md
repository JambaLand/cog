# Installation Guide

## Step 1: Install Composio Package

The Composio plugin for Cog requires the `composio` package to be installed.

```bash
pip install composio
```

## Step 2: Get Your Composio API Key

1. Go to [platform.composio.dev](https://platform.composio.dev)
2. Sign up or log in
3. Navigate to your API keys section
4. Generate a new API key
5. Copy the key for use in the next step

## Step 3: Configure Your Environment

Set the API key as an environment variable in your shell:

```bash
export COMPOSIO_API_KEY="your-api-key-here"
```

Or in your `.env` file:

```
COMPOSIO_API_KEY=your-api-key-here
```

Or pass it directly when creating clients:

```python
from cog.ext.composio import ComposioClient

client = ComposioClient(api_key="your-api-key-here")
```

## Step 4: Verify Installation

Run this quick test to verify everything is working:

```python
from cog.ext.composio import ComposioClient

client = ComposioClient()
apps = client.get_available_apps()
print(f"Successfully connected! Found {len(apps)} apps")
```

## Troubleshooting

### ImportError: No module named 'composio'

Install the Composio package:
```bash
pip install composio
```

### ValueError: COMPOSIO_API_KEY not provided

Make sure you've set the environment variable or passed the API key to the client.

### RuntimeError: TLDV is not available

Your Composio account may not have access to TLDV. Check your account at platform.composio.dev.

## Next Steps

- Read the [README.md](./README.md) for usage examples
- Check out [example.py](./example.py) for working code samples
- Visit the [Composio Documentation](https://docs.composio.dev) for more information
