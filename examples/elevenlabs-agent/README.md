# ElevenLabs Conversational AI Agent - Cog Integration

This example shows how to integrate the ElevenLabs Conversational AI Agent with Cog.

## Customer Support Agent

**Agent ID:** `agent_0201kjywpmreevjtt20xac516ww5`

## Setup

### 1. Get an API Key

Sign up at [elevenlabs.io](https://elevenlabs.io) and get your API key from the dashboard.

### 2. Set Environment Variable

```bash
export ELEVENLABS_API_KEY="your-api-key-here"
```

Or create a `.env` file:

```
ELEVENLABS_API_KEY=your-api-key-here
```

### 3. Run the Predictor

Build and run with Cog:

```bash
cog predict -i agent_id="agent_0201kjywpmreevjtt20xac516ww5"
```

Or with custom instructions:

```bash
cog predict \
  -i agent_id="agent_0201kjywpmreevjtt20xac516ww5" \
  -i custom_instructions="You are a customer support agent for an e-commerce platform"
```

## Integration Methods

### Option 1: Docker Container

Deploy as a Docker container:

```bash
cog build -t elevenlabs-agent
docker run -e ELEVENLABS_API_KEY=$ELEVENLABS_API_KEY elevenlabs-agent predict
```

### Option 2: Web API with FastAPI

Create a simple REST API (add to `predict.py`):

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/conversation")
async def start_conversation(agent_id: str):
    # Use the predictor to start conversation
    pass
```

### Option 3: Direct Python

Use the `elevenlabs_agent.py` module directly:

```python
from cog.elevenlabs_agent import ElevenLabsAgent

agent = ElevenLabsAgent(
    agent_id="agent_0201kjywpmreevjtt20xac516ww5"
)
status = agent.start_conversation()
result = agent.end_conversation()
print(f"Conversation ID: {result['conversation_id']}")
```

## Features

- 🎤 Real-time voice conversations
- 🔗 WebRTC and WebSocket support
- 📊 Conversation tracking and history
- 🚀 Production-ready deployment
- 🔄 Context-aware responses

## API Reference

### Parameters

- **agent_id** (string, required): ID of the ElevenLabs agent
- **custom_instructions** (string, optional): Custom system instructions for the agent

### Output

Yields status messages and conversation updates during the interaction.

## Wix Integration

To add this agent to your Wix website, use the embeddable widget:

```html
<script src="https://elevenlabs.io/convai-widget/index.js" async></script>
<elevenlabs-convai
    agent-id="agent_0201kjywpmreevjtt20xac516ww5">
</elevenlabs-convai>
```

## More Information

- [ElevenLabs Documentation](https://elevenlabs.io/docs/eleven-agents)
- [ElevenLabs API Reference](https://elevenlabs.io/docs/api-reference/introduction)
- [Cog Documentation](https://github.com/replicate/cog)
