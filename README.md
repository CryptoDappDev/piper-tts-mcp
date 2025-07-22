# 🎤 Piper TTS MCP Server

A **Model Context Protocol (MCP)** server that integrates [Piper TTS](https://github.com/rhasspy/piper) for high-quality text-to-speech functionality. This server provides a `speak` tool that converts text to speech and plays it directly through your speakers with customizable volume control.

## ✨ Features

- 🔊 **High-quality text-to-speech** using Piper TTS
- 🎚️ **Volume control** (0.01 to 1.00)
- ⚡ **Memory-based audio playback** (no temporary files)
- 🔧 **Customizable voice parameters** (speaker, speed, voice variation)
- 🚀 **Fast and lightweight** MCP integration
- 🔇 **Silent operation** (no console output)

## 📋 Requirements

**⚠️ Important Prerequisites:**
- **Python 3.12+** installed on your system
- **Piper TTS service** running on `localhost:5000`

You can set this up using the included Docker configuration or by running Piper TTS separately.

## 🚀 Quick Start

### 1. 🐳 Start Piper TTS Service

Clone this repo and start the TTS service:

```bash
git clone https://github.com/CryptoDappDev/piper-tts-mcp.git
cd piper-tts-mcp
```

**Option A: Using Docker Compose (Recommended)**
```bash
docker compose up -d
```

**Option B: Using Docker Build**
```bash
docker build -t piper-tts-mcp .
docker run -p 5000:5000 piper-tts-mcp
```

### 2. 🔧 Configure MCP Client

Add the server to your MCP configuration (e.g., `.mcp.json` for Claude Desktop):

```json
{
  "mcpServers": {
    "speak": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/your/piper-tts-mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

### 3. 🎉 Enjoy!

The `speak` tool is now available in your MCP client!

## 🛠️ Usage

The MCP server provides a `speak` tool with the following parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | *required* | Text to convert to speech |
| `speaker_id` | int | 0 | Voice speaker ID |
| `length_scale` | float | 1.1 | Speech speed (lower = faster) |
| `noise_scale` | float | 0.667 | Voice variation control |
| `noise_w_scale` | float | 0.333 | Pronunciation variation |
| `volume` | float | 0.15 | Volume level (0.01 to 1.00) |

### Example Usage

```python
# Basic usage
speak("Hello, world!")

# With custom volume
speak("This is louder!", volume=0.5)

# With custom voice settings
speak("Fast and varied speech", 
      length_scale=0.8, 
      volume=0.3, 
      noise_scale=0.8)
```

## 🔧 Development

### Dependencies

- Python 3.12+
- `mcp[cli]` - MCP framework
- `requests` - HTTP client for TTS API
- `pygame` - Audio playback

### Local Development

```bash
# Install dependencies
uv sync

# Run the server
uv run server.py
```

## 📦 Docker Configuration

The included Docker setup provides:
- **Piper TTS service** on port 5000
- **Pre-configured voice models**
- **Automatic startup**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Piper TTS](https://github.com/rhasspy/piper) - Fast, local neural text to speech
- [Model Context Protocol](https://modelcontextprotocol.io/) - Standardized protocol for AI model interactions

---

**Made with ❤️ for the MCP community**