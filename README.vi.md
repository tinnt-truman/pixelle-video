<h1 align="center">🎬 Pixelle-Video — Engine Tạo Video AI</h1>

<p align="center"><a href="README.md">English</a> | <b>Tiếng Việt</b> | <a href="README_CN.md">中文</a></p>

<p align="center">Tự động tạo video ngắn - Nhập chủ đề, tự động viết kịch bản, tạo ảnh AI, lồng tiếng, thêm nhạc nền.</p>

---

## 📋 Mục lục

- [Tính năng](#tính-năng)
- [Bắt đầu nhanh](#bắt-đầu-nhanh)
- [Cài đặt](#cài-đặt)
- [Cấu hình](#cấu-hình)
- [Sử dụng](#sử-dụng)
- [Tham chiếu API](#tham-chiếu-api)
- [TTS Engines](#tts-engines)
- [Triển khai Docker](#triển-khai-docker)
- [Tích hợp CreatorHub](#tích-hợp-creatorhub)
- [Khắc phục sự cố](#khắc-phục-sự-cố)

---

## ✨ Tính năng

- ✍️ **Tự động viết kịch bản**: Tạo kịch bản video từ chủ đề
- 🎨 **Ảnh AI**: Tạo ảnh bằng ComfyUI/RunningHub
- 🗣️ **Multi-TTS**: Hỗ trợ Edge TTS, Doubao, Azure, IndexTTS
- 🎵 **Nhạc nền**: Thêm BGM vào video
- 🎬 **Tự động ghép**:合成 video một click
- 🌐 **Web UI**: Giao diện Streamlit
- 🔌 **API**: RESTful API để tích hợp
- 🌍 **Đa ngôn ngữ**: Tiếng Việt, Anh, Trung

---

## 🚀 Bắt đầu nhanh

### Cách 1: Docker (Khuyến nghị)

```bash
# Clone
git clone https://github.com/tinnt-truman/pixelle-video.git
cd pixelle-video

# Cấu hình
cp config.example.yaml config.yaml
nano config.yaml

# Chạy
docker-compose up -d

# Truy cập
open http://localhost:8511
```

### Cách 2: Cài đặt Local

```bash
# Clone
git clone https://github.com/tinnt-truman/pixelle-video.git
cd pixelle-video

# Python 3.10+
python -m venv .venv
source .venv/bin/activate

# Cài dependencies
pip install -r requirements.txt

# Cấu hình
cp config.example.yaml config.yaml

# Chạy API
python api/app.py

# Chạy Web UI
streamlit run web/app.py
```

---

## 📦 Cài đặt

### Yêu cầu

- Python 3.10+
- Node.js 18+ (một số tính năng)
- FFmpeg
- ComfyUI (local hoặc RunningHub)

### Bước 1: Clone & Setup

```bash
git clone https://github.com/tinnt-truman/pixelle-video.git
cd pixelle-video
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
```

### Bước 2: Cài Dependencies

```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình

```bash
cp config.example.yaml config.yaml
```

Chỉnh sửa `config.yaml`:

```yaml
# Cấu hình ComfyUI
comfyui:
  host: "127.0.0.1"
  port: 8188
  api_key: ""  # Tùy chọn

# RunningHub (Cloud ComfyUI)
runninghub:
  enabled: false
  api_key: ""
  host: "https://www.runninghub.cn"

# Cấu hình TTS
tts:
  engine: "edge"  # edge, doubao, azure, index
  edge:
    voice: "vi-VN-HoaiMyNeural"
  doubao:
    app_id: ""
    access_token: ""

# Cấu hình LLM
llm:
  provider: "openai"
  api_key: ""
  model: "gpt-4"
```

### Bước 4: Chạy

```bash
# API server
python api/app.py --host 0.0.0.0 --port 8010

# Web UI
streamlit run web/app.py --server.port 8011
```

---

## ⚙️ Cấu hình

### File Cấu hình: `config.yaml`

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
  # Cấu hình cho từng engine...

# LLM
llm:
  provider: "openai"
  api_key: ""
  model: "gpt-4"

# Tạo ảnh
image:
  provider: "comfyui"  # comfyui, runninghub
  
# Video
video:
  fps: 30
  resolution: "1920x1080"
```

### Biến Environment

| Biến | Mô tả |
|------|-------|
| `COMFYUI_HOST` | Host ComfyUI |
| `COMFYUI_PORT` | Cổng ComfyUI |
| `OPENAI_API_KEY` | API key OpenAI |
| `DATABASE_URL` | Chuỗi kết nối PostgreSQL |
| `REDIS_URL` | Chuỗi kết nối Redis |

---

## 📖 Sử dụng

### Tạo Video từ Chủ đề

```python
from pixelle_video import VideoGenerator

generator = VideoGenerator()

# Tạo video từ chủ đề
result = generator.generate(
    topic="Giới thiệu về AI",
    language="vi"
)

print(result.video_path)
```

### Sử dụng API

```bash
# Tạo video project
curl -X POST http://localhost:8010/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Video của tôi",
    "topic": "Giới thiệu về AI",
    "language": "vi"
  }'

# Kiểm tra trạng thái
curl http://localhost:8010/api/projects/{project_id}

# Tạo TTS
curl -X POST http://localhost:8010/api/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Xin chào thế giới",
    "engine": "edge",
    "voice": "vi-VN-HoaiMyNeural"
  }'
```

---

## 🔊 TTS Engines

### Engines được hỗ trợ

| Engine | Mô tả | Cấu hình |
|--------|-------|----------|
| **Edge TTS** | Microsoft Edge TTS (miễn phí) | Mặc định |
| **Doubao** | ByteDance Doubao TTS | Cần API key |
| **Azure** | Microsoft Azure TTS | Cần subscription |
| **IndexTTS** | TTS cloning giọng nói | Cần model |

### Cấu hình TTS

```yaml
# config.yaml
tts:
  engine: "edge"
  
  edge:
    voice: "vi-VN-HoaiMyNeural"
    rate: "+0%"
    volume: "+0%"
    
  doubao:
    app_id: "app_id_cua_ban"
    access_token: "token_cua_ban"
    
  azure:
    subscription_key: "key_cua_ban"
    region: "eastus"
    
  index:
    model_path: "/path/to/model"
```

### Liệt kê giọng nói

```bash
# Edge TTS
python -m edge_tts --list-voices

# API endpoint
curl http://localhost:8010/api/tts/voices?engine=edge
```

---

## 🐳 Triển khai Docker

### Sử dụng Docker Compose

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

### Push lên Docker Hub

```bash
# Set token
export DOCKER_TOKEN=token_cua_ban

# Build và push
./scripts/docker-push.sh v1.0.0
```

---

## 🔗 Tích hợp CreatorHub

Pixelle-Video là một phần của [CreatorHub](https://github.com/tinnt-truman/CreatorHub).

### Bật trong CreatorHub

```bash
# Bật video service
curl -X POST http://localhost:8001/workspaces/default/projects/pixelle-video/enable
```

### Truy cập qua Traefik

```
https://ten-mien-cua-ban/video-api   # API
https://ten-mien-cua-ban/video-ui    # Web UI
```

---

## 🔧 Khắc phục sự cố

### Lỗi kết nối ComfyUI

```bash
# Kiểm tra ComfyUI đang chạy
curl http://localhost:8188/system_stats

# Kiểm tra cấu hình
grep -A5 "comfyui" config.yaml
```

### TTS không hoạt động

```bash
# Test Edge TTS
python -c "import edge_tts; print('OK')"

# Kiểm tra tên voice
python -m edge_tts --list-voices | grep vi-VN
```

### Port đã được sử dụng

```bash
# Tìm process
lsof -i :8010

# Thay đổi port trong config.yaml
server:
  port: 8011
```

---

## 📝 Giấy phép

MIT

---

## 🔗 Liên kết

- [GitHub](https://github.com/tinnt-truman/pixelle-video)
- [CreatorHub](https://github.com/tinnt-truman/CreatorHub)
- [Issues](https://github.com/tinnt-truman/pixelle-video/issues)
