# Setup TLDV in Claude Desktop (macOS)

This guide will set up the TLDV MCP Server in your Claude Desktop application.

## ⚡ Quick Setup (3 Steps)

### Step 1: Copy the Setup Script

Copy this command and paste it in your macOS Terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/replicate/cog/claude/install-composio-plugin-osj4O/script/setup-claude-tldv | bash
```

Or if you have the Cog repository cloned:

```bash
bash script/setup-claude-tldv
```

### Step 2: Restart Claude Desktop

1. **Completely close Claude Desktop** (not just minimize)
   - Use: Cmd+Q or Claude → Quit Claude
2. **Wait 3 seconds**
3. **Reopen Claude Desktop** from Applications

### Step 3: Test It Works

Ask Claude in the chat:

```
List my TLDV meetings
```

Or:

```
Get highlights from meeting: [meeting-id]
```

## ✅ What the Script Does

The `setup-claude-tldv` script automatically:

1. ✅ Checks Docker is installed
2. ✅ Clones the TLDV MCP Server repository
3. ✅ Builds the Docker image (`tldv-mcp-server`)
4. ✅ Creates/updates your Claude Desktop config
5. ✅ Adds your TLDV API key securely

## 📂 What Gets Modified

- **File**: `~/.config/Claude/claude_desktop_config.json`
- **What**: Adds TLDV MCP Server configuration
- **Backup**: Creates `claude_desktop_config.json.backup` if file exists

## 🧪 Available Tools in Claude

Once setup, you can use these TLDV tools:

### List Meetings
```
"List all my TLDV meetings from the past week"
```

### Get Meeting Details
```
"Get the metadata for meeting: abc123def"
```

### Get Transcript
```
"Get the full transcript for meeting: abc123def"
```

### Get Highlights
```
"Get the AI highlights from meeting: abc123def"
```

## 🔐 Security

- Your API key is stored in Claude's config file
- The config file is typically only readable by your user
- If you revoke the key later, update: `~/.config/Claude/claude_desktop_config.json`

## ❌ Troubleshooting

### Docker not found
**Error**: "Docker not found"
- **Fix**: Install Docker from https://www.docker.com/products/docker-desktop

### Build failed
**Error**: "Failed to build Docker image"
- **Fix**: Try running again, internet connection may have been interrupted

### Tools not appearing
**Problem**: TLDV tools still don't show up in Claude
- **Solution**:
  1. Close Claude Desktop completely (Cmd+Q)
  2. Wait 5 seconds
  3. Open Claude Desktop again
  4. Refresh the page (if using web version)

### Need to reconfigure
Run the script again:
```bash
bash script/setup-claude-tldv
```

## 🔧 Manual Configuration

If the script doesn't work, you can manually edit:

1. Open: `~/.config/Claude/claude_desktop_config.json`
2. Add this under `mcpServers`:

```json
{
  "mcpServers": {
    "tldv": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--init",
        "--rm",
        "-e",
        "TLDV_API_KEY=60baeeba-e74b-405c-ae1f-219fa5b2a691",
        "tldv-mcp-server"
      ]
    }
  }
}
```

3. Save and restart Claude Desktop

## 📚 More Information

- TLDV API Docs: https://tldv.io/docs
- MCP Server Repo: https://gitlab.com/tldv/tldv-mcp-server
- Cog TLDV Integration: `docs/tldv.md`

## ✨ That's It!

You're all set! Start asking Claude about your TLDV meetings! 🎉
