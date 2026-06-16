<h1 align="center">🎬 Pixelle-Video — AI Video Generation Engine</h1>

<p align="center"><b>English</b> | <a href="README.vi.md">Tiếng Việt</a> | <a href="README_CN.md">中文</a></p>

<p align="center">全自动短视频引擎 - 输入主题，自动生成视频文案、AI配图、语音解说、背景音乐，一键合成视频。</p>

---

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [TTS Engines](#tts-engines)
- [Docker Deployment](#docker-deployment)
- [Integration with CreatorHub](#integration-with-creatorhub)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

- ✍️ **Auto Script**: Generate video script from topic
- 🎨 **AI Images**: Generate images using ComfyUI/RunningHub
- 🗣️ **Multi-TTS**: Support Edge TTS, Doubao, Azure, IndexTTS
- 🎵 **Background Music**: Add BGM to video
- 🎬 **Auto Compose**: One-click video synthesis
- 🌐 **Web UI**: Streamlit-based interface
- 🔌 **API**: RESTful API for integration
- 🌍 **Multi-language**: Vietnamese, English, Chinese

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone
git clone https://github.com/tinnt-truman/pixelle-video.git
cd pixelle-video

# Configure
cp config.example.yaml config.yaml
nano config.yaml

# Run
docker-compose up -d

# Access
open http://localhost:8511
```

### Option 2: Local Installation

```bash
# Clone
git clone https://github.com/tinnt-truman/pixelle-video.git
cd pixelle-video

# Python 3.10+
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp config.example.yaml config.yaml

# Run API
python api/app.py

# Run Web UI
streamlit run web/app.py
```

---

## 📦 Installation

### Prerequisites

- Python 3.10+
- Node.js 18+ (for some features)
- FFmpeg
- ComfyUI (local or RunningHub)

### Step 1: Clone & Setup

```bash
git clone https://github.com/tinnt-truman/pixelle-video.git
cd pixelle-video
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml`:

```yaml
# ComfyUI Configuration
comfyui:
  host: "127.0.0.1"
  port: 8188
  api_key: ""  # Optional

# RunningHub (Cloud ComfyUI)
runninghub:
  enabled: false
  api_key: ""
  host: "https://www.runninghub.cn"

# TTS Configuration
tts:
  engine: "edge"  # edge, doubao, azure, index
  edge:
    voice: "vi-VN-HoaiMyNeural"
  doubao:
    app_id: ""
    access_token: ""

# LLM Configuration
llm:
  provider: "openai"
  api_key: ""
  model: "gpt-4"
```

### Step 4: Run

```bash
# API server
python api/app.py --host 0.0.0.0 --port 8010

# Web UI
streamlit run web/app.py --server.port 8011
```

---

## ⚙️ Configuration

### Config File: `config.yaml`

```yaml
# Server
server:
  host: "0.0.0.0"
  port: 8010

# ComfyUI
comfyui:
  host: "127.0.0.1"
  port: 8188
  api_key: ""

# RunningHub (Cloud)
runninghub:
  enabled: false
  api_key: ""

# TTS
tts:
  engine: "edge"
  # Engine-specific configs...

# LLM
llm:
  provider: "openai"
  api_key: ""
  model: "gpt-4"

# Image Generation
image:
  provider: "comfyui"  # comfyui, runninghub
  
# Video
video:
  fps: 30
  resolution: "1920x1080"
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `COMFYUI_HOST` | ComfyUI host |
| `COMFYUI_PORT` | ComfyUI port |
| `OPENAI_API_KEY` | OpenAI API key |
| `DATABASE_URL` | PostgreSQL connection |
| `REDIS_URL` | Redis connection |

---

## 📖 Usage

### Generate Video from Topic

```python
from pixelle_video import VideoGenerator

generator = VideoGenerator()

# Generate video from topic
result = generator.generate(
    topic="Introduction to AI",
    language="en"
)

print(result.video_path)
```

### API Usage

```bash
# Create video project
curl -X POST http://localhost:8010/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Video",
    "topic": "Introduction to AI",
    "language": "en"
  }'

# Check status
curl http://localhost:8010/api/projects/{project_id}

# Generate TTS
curl -X POST http://localhost:8010/api/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "engine": "edge",
    "voice": "en-US-AriaNeural"
  }'
```

---

## 🔊 TTS Engines

### Supported Engines

| Engine | Description | Config |
|--------|-------------|--------|
| **Edge TTS** | Microsoft Edge TTS (free) | Default |
| **Doubao** | ByteDance Doubao TTS | Requires API key |
| **Azure** | Microsoft Azure TTS | Requires subscription |
| **IndexTTS** | Voice cloning TTS | Requires model |

### Configure TTS

```yaml
# config.yaml
tts:
  engine: "edge"
  
  edge:
    voice: "vi-VN-HoaiMyNeural"
    rate: "+0%"
    volume: "+0%"
    
  doubao:
    app_id: "your_app_id"
    access_token: "your_token"
    
  azure:
    subscription_key: "your_key"
    region: "eastus"
    
  index:
    model_path: "/path/to/model"
```

### List Available Voices

```bash
# Edge TTS
python -m edge_tts --list-voices

# API endpoint
curl http://localhost:8010/api/tts/voices?engine=edge
```

---

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d
```

### Build Image

```bash
docker build -t pixelle-video .
docker run -p 8010:8010 -p 8011:8011 pixelle-video
```

### Push to Docker Hub

```bash
# Set token
export DOCKER_TOKEN=your_token

# Build and push
./scripts/docker-push.sh v1.0.0
```

---

## 🔗 Integration with CreatorHub

Pixelle-Video is part of [CreatorHub](https://github.com/tinnt-truman/CreatorHub).

### Enable in CreatorHub

```bash
# Enable video service
curl -X POST http://localhost:8001/workspaces/default/projects/pixelle-video/enable
```

### Access via Traefik

```
https://your-domain.com/video-api   # API
https://your-domain.com/video-ui    # Web UI
```

---

## 🔧 Troubleshooting

### ComfyUI Connection Failed

```bash
# Check ComfyUI is running
curl http://localhost:8188/system_stats

# Check config
grep -A5 "comfyui" config.yaml
```

### TTS Not Working

```bash
# Test Edge TTS
python -c "import edge_tts; print('OK')"

# Check voice name
python -m edge_tts --list-voices | grep vi-VN
```

### Port Already in Use

```bash
# Find process
lsof -i :8010

# Change port in config.yaml
server:
  port: 8011
```

---

## 📝 License

MIT

---

## 🔗 Links

- [GitHub](https://github.com/tinnt-truman/pixelle-video)
- [CreatorHub](https://github.com/tinnt-truman/CreatorHub)
- [Issues](https://github.com/tinnt-truman/pixelle-video/issues)
