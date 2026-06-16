<h1 align="center">🎬 Pixelle-Video —— Công cụ tạo video ngắn AI hoàn toàn tự động</h1>

<p align="center"><a href="README_EN.md">English</a> | <a href="README.md">中文</a> | <b>Tiếng Việt</b></p>

<p align="center">
  <a href="https://github.com/AIDC-AI/Pixelle-Video/releases" target="_blank"><img src="https://img.shields.io/badge/📦 Gói Windows-50C878" alt="Gói Windows"></a>
  <a href="https://aidc-ai.github.io/Pixelle-Video/zh" target="_blank"><img src="https://img.shields.io/badge/📘 Tài liệu sử dụng-4A90E2" alt="Tài liệu"></a>
  <a href="https://github.com/AIDC-AI/Pixelle-Video/stargazers"><img src="https://img.shields.io/github/stars/AIDC-AI/Pixelle-Video.svg" alt="Stargazers"></a>
  <a href="https://github.com/AIDC-AI/Pixelle-Video/issues"><img src="https://img.shields.io/github/issues/AIDC-AI/Pixelle-Video.svg" alt="Issues"></a>
  <a href="https://github.com/AIDC-AI/Pixelle-Video/network/members"><img src="https://img.shields.io/github/forks/AIDC-AI/Pixelle-Video.svg" alt="Forks"></a>
  <a href="https://github.com/AIDC-AI/Pixelle-Video/blob/main/LICENSE"><img src="https://img.shields.io/github/license/AIDC-AI/Pixelle-Video.svg" alt="License"></a>
</p>

Chỉ cần nhập một **chủ đề**, Pixelle-Video sẽ tự động hoàn thành:
- ✍️ Viết lời bình video  
- 🎨 Tạo hình ảnh/video AI  
- 🗣️ Tổng hợp giọng đọc  
- 🎵 Thêm nhạc nền  
- 🎬 Tự động ghép video  

**Không cần kinh nghiệm**, biến việc tạo video thành một câu nói!

## Xem trước giao diện Web

![Giao diện Web UI](resources/webui.png)

## Cập nhật gần đây

- ✅ **2026-06-01**: Thêm cấu hình mô hình API trực tiếp, hỗ trợ cấu hình nhà cung cấp hình ảnh/video, Base URL và proxy trong WebUI
- ✅ **2026-01-26**: Thêm mô hình "Chuyển động", tải lên video và hình ảnh tham chiếu để chuyển động
- ✅ **2026-01-14**: Thêm pipeline "Avatar kỹ thuật số" và "Hình ảnh sang video", hỗ trợ giọng đọc đa ngôn ngữ
- ✅ **2026-01-06**: Thêm hỗ trợ máy 48GB VRAM RunningHub
- ✅ **2025-12-28**: Hỗ trợ giới hạn đồng thời RunningHub có thể cấu hình, tối ưu logic dữ liệu có cấu trúc LLM
- ✅ **2025-12-17**: Hỗ trợ cấu hình API Key ComfyUI, hỗ trợ gọi mô hình Nano Banana, API hỗ trợ tham số template tùy chỉnh

## Tính năng nổi bật

- ✅ **Tự động hoàn toàn** - Nhập chủ đề, tự động tạo video đầy đủ
- ✅ **Văn bản AI thông minh** - Tự động sáng tạo lời bình theo chủ đề
- ✅ **Hình ảnh AI** - Mỗi câu đều có minh họa AI đẹp mắt
- ✅ **Video AI** - Hỗ trợ sử dụng mô hình tạo video AI (như WAN 2.1)
- ✅ **API mô hình trực tiếp** - Gọi trực tiếp DashScope, OpenAI, Seedream, Seedance, Kling
- ✅ **Giọng đọc AI** - Hỗ trợ Edge-TTS, Index-TTS và nhiều giải pháp TTS khác
- ✅ **Nhạc nền** - Hỗ trợ thêm BGM
- ✅ **Phong cách hình ảnh** - Nhiều template có sẵn
- ✅ **Kích thước linh hoạt** - Hỗ trợ dọc, ngang và nhiều kích thước video
- ✅ **Nhiều mô hình AI** - Hỗ trợ GPT, Tongyi Qianwen, DeepSeek, Ollama
- ✅ **Khả năng nguyên tử kết hợp linh hoạt** - Hỗ trợ ComfyUI / RunningHub workflow, hoặc API trực tiếp

## Quy trình tạo video

![Sơ đồ quy trình](resources/flow.png)

Từ văn bản đầu vào đến video đầu ra: **Tạo lời bình → Lên kế hoạch hình ảnh → Xử lý từng frame → Ghép video**

Mỗi bước đều hỗ trợ tùy chỉnh linh hoạt, có thể chọn mô hình AI, engine âm thanh, phong cách hình ảnh khác nhau.

## Bắt đầu nhanh

### Gói Windows một cú nhấp (khuyến nghị cho người dùng Windows)

**Không cần cài đặt Python, uv hoặc ffmpeg, sử dụng ngay!**

👉 **[Tải gói Windows một cú nhấp](https://github.com/AIDC-AI/Pixelle-Video/releases/latest)**

1. Tải gói Windows mới nhất và giải nén
2. Nhấp đúp `start.bat` để khởi động giao diện Web
3. Trình duyệt tự mở http://localhost:8501
4. Cấu hình LLM API và dịch vụ tạo hình ảnh trong "⚙️ Cài đặt hệ thống"
5. Bắt đầu tạo video!

### Cài từ mã nguồn (dành cho macOS / Linux hoặc cần tùy chỉnh)

#### Yêu cầu môi trường

Trước khi bắt đầu, cần cài đặt trình quản lý gói Python `uv` và công cụ xử lý video `ffmpeg`:

##### Cài uv

Truy cập tài liệu chính thức uv để xem cách cài phù hợp với hệ thống của bạn:  
👉 **[Hướng dẫn cài uv](https://docs.astral.sh/uv/getting-started/installation/)**

##### Cài ffmpeg

**macOS**
```bash
brew install ffmpeg
```

**Ubuntu / Debian**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows**
- Tải: https://ffmpeg.org/download.html
- Giải nén, thêm thư mục `bin` vào biến môi trường PATH

#### Bước 1: Tải dự án

```bash
git clone https://github.com/AIDC-AI/Pixelle-Video.git
cd Pixelle-Video
```

#### Bước 2: Khởi động giao diện Web

```bash
# Sử dụng uv (khuyến nghị, tự động cài phụ thuộc)
uv run streamlit run web/app.py
```

Trình duyệt tự mở http://localhost:8501

#### Bước 3: Cấu hình trong Web

Lần đầu sử dụng, mở panel "⚙️ Cài đặt hệ thống":
- **Cấu hình LLM**: Chọn mô hình AI (như Tongyi Qianwen, GPT) và nhập API Key
- **Cấu hình ComfyUI / RunningHub**: Nếu cần sử dụng workflow tạo hình ảnh, video hoặc giọng đọc
- **Cấu hình mô hình API**: Nếu cần gọi trực tiếp mô hình hình ảnh/video

Nhấp "Lưu cấu hình" sau khi hoàn tất.

## Hướng dẫn sử dụng

### ⚙️ Cài đặt hệ thống (bắt buộc lần đầu)

#### 1. Cấu hình LLM (Mô hình ngôn ngữ lớn)
AI dùng để tạo lời bình video.

**Chọn nhanh theo preset**  
- Chọn mô hình từ danh sách thả xuống (Tongyi Qianwen, GPT-4o, DeepSeek...)
- Tự động điền base_url và model

**Cấu hình thủ công**  
- API Key: Nhập khóa
- Base URL: Địa chỉ API
- Model: Tên mô hình

#### 2. Cấu hình ComfyUI / RunningHub
Dùng để tạo hình ảnh, video hoặc giọng đọc qua ComfyUI workflow.

**Triển khai cục bộ (khuyến nghị)**  
- ComfyUI URL: Địa chỉ dịch vụ ComfyUI cục bộ (mặc định http://127.0.0.1:8188)

**Triển khai đám mây**  
- RunningHub API Key: Khóa dịch vụ tạo hình ảnh đám mây

#### 3. Cấu hình mô hình API trực tiếp
Gọi trực tiếp nhà cung cấp mô hình hình ảnh, video hoặc phân tích tài nguyên mà không cần ComfyUI/RunningHub.

**Nhà cung cấp được hỗ trợ**
- OpenAI / GPT Image
- DashScope / Wan / HappyHorse
- Volcengine ARK / Seedream / Seedance
- Kling AI

### 📝 Nhập nội dung (cột trái)

#### Chế độ tạo
- **AI tạo nội dung**: Nhập chủ đề, AI tự sáng tạo lời bình
- **Văn bản cố định**: Nhập lời bình sẵn, bỏ qua bước AI sáng tạo

#### Nhạc nền (BGM)
- **Không BGM**: Chỉ giọng đọc
- **Nhạc có sẵn**: Chọn nhạc nền đặt sẵn
- **Tải lên tùy chỉnh**: Đặt file nhạc (MP3/WAV) vào thư mục `bgm/`

### 🎤 Cài đặt giọng nói (cột giữa)

#### Workflow TTS
- Chọn workflow TTS từ danh sách thả xuống (hỗ trợ Edge-TTS, Index-TTS...)

#### Âm thanh tham chiếu (tùy chọn)
- Tải lên file âm thanh tham chiếu để sao chép giọng nói

### 🎨 Cài đặt hình ảnh (cột giữa)

#### Tạo hình ảnh
**ComfyUI Workflow**  
- Chọn workflow tạo hình ảnh từ danh sách thả xuống
- Hỗ trợ triển khai cục bộ (selfhost) và đám mây (RunningHub)

**Kích thước hình ảnh**  
- Đặt chiều rộng và chiều cao (đơn vị: pixel)
- Mặc định 1024x1024

**Tiền tố Prompt**  
- Kiểm soát phong cách hình ảnh tổng thể (bằng tiếng Anh)

#### Template video
- `static_*.html`: Template tĩnh (không cần media AI)
- `image_*.html`: Template hình ảnh (sử dụng ảnh AI làm nền)
- `video_*.html`: Template video (sử dụng video AI làm nền)

### 🎬 Tạo video (cột phải)

#### Nút tạo
- Nhấp "🎬 Tạo video" sau khi cấu hình xong
- Hiển thị tiến trình thời gian thực
- Tự động hiển thị video xem trước sau khi hoàn tất

## Câu hỏi thường gặp

**Q: Lần đầu sử dụng mất bao lâu?**  
A: Thời gian tạo phụ thuộc số lượng frame, tốc độ mạng và tốc độ suy luận AI, thường vài phút.

**Q: Không hài lòng với kết quả?**  
A: Có thể thử:
1. Đổi mô hình LLM
2. Điều chỉnh kích thước hình ảnh và tiền tố prompt
3. Đổi workflow TTS hoặc tải lên âm thanh tham chiếu
4. Thử template và kích thước video khác

**Q: Chi phí khoảng bao nhiêu?**  
A: **Dự án hỗ trợ chạy miễn phí hoàn toàn!**

- **Phương án miễn phí**: LLM dùng Ollama (chạy cục bộ) + ComfyUI cục bộ = 0 đồng
- **Phương án khuyến nghị**: LLM dùng Tongyi Qianwen (chi phí thấp) + ComfyUI cục bộ
- **Phương án đám mây**: LLM dùng OpenAI + hình ảnh dùng RunningHub

## Tài liệu tham khảo

- [Tài liệu sử dụng](https://aidc-ai.github.io/Pixelle-Video/zh) — Hướng dẫn chi tiết cách sử dụng
- [README tiếng Việt](README.vi.md) ← bạn đang đọc
- [README tiếng Anh](README_EN.md)
- [README tiếng Trung](README.md)

## Dự án tham khảo

- [Pixelle-MCP](https://github.com/AIDC-AI/Pixelle-MCP) - Máy chủ ComfyUI MCP
- [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) - Công cụ tạo video
- [NarratoAI](https://github.com/linyqh/NarratoAI) - Tự động hóa bình luận phim
- [MoneyPrinterPlus](https://github.com/ddean2009/MoneyPrinterPlus) - Nền tảng sáng tạo video
- [ComfyKit](https://github.com/puke3615/ComfyKit) - Thư viện gói ComfyUI workflow

## Phản hồi và hỗ trợ

- 🐛 **Gặp vấn đề**: Gửi [Issue](https://github.com/AIDC-AI/Pixelle-Video/issues)
- 💡 **Đề xuất tính năng**: Gửi [Feature Request](https://github.com/AIDC-AI/Pixelle-Video/issues)
- ⭐ **Cho Star**: Nếu dự án hữu ích, hãy cho Star ủng hộ!

## Giấy phép

Dự án sử dụng giấy phép Apache 2.0, xem chi tiết trong [LICENSE](LICENSE).
