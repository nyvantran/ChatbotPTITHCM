# Chatbot RAG PTITHCM (FastAPI + LangChain)

Dự án Chatbot RAG (Retrieval-Augmented Generation) hỗ trợ giải đáp thắc mắc cho sinh viên Học viện Công nghệ Bưu chính Viễn thông (PTITHCM). Hệ thống sử dụng kiến trúc hiện đại, linh hoạt, hỗ trợ đa nền tảng LLM (Gemini, OpenAI, Anthropic) và cơ sở dữ liệu vector MongoDB Atlas.

## 🚀 Tính năng chính

- **Xác thực người dùng**: Đăng ký, đăng nhập và quản lý phiên làm việc bằng JWT (JSON Web Token).
- **Trò chuyện RAG**: Chatbot thông minh sử dụng kỹ thuật RAG để trả lời dựa trên tài liệu (PDF, JSON) của học viện.
- **Quản lý hội thoại**: Lưu trữ lịch sử trò chuyện, tạo mới hoặc xóa các cuộc hội thoại.
- **Giao diện Web**: Giao diện trực quan trên trình duyệt (HTML/CSS/JS thuần) tại `/user` và `/chat`.
- **Đa LLM**: Dễ dàng thay đổi Provider (Gemini, OpenAI, v.v.) qua cấu hình `.env`.
- **Nạp dữ liệu tự động**: Script `ingest.py` giúp xử lý và nạp tài liệu PDF/JSON vào VectorDB nhanh chóng.

## 🛠 Công nghệ sử dụng

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous).
- **Orchestration**: [LangChain](https://www.langchain.com/) & [LangGraph](https://www.langchain.com/langgraph).
- **Database**: 
  - [MongoDB Atlas](https://www.mongodb.com/atlas) (Vector Database).
  - SQLite (Local Chat History).
- **UI**: HTML, CSS, JavaScript (Vanilla).

## 📋 Yêu cầu hệ thống

- Python 3.9 trở lên.
- Tài khoản MongoDB Atlas (đã tạo Vector Index).
- Google API Key (cho Gemini) hoặc OpenAI API Key.

## ⚙️ Cài đặt & Khởi chạy

### 1. Tải dự án và cài đặt môi trường
```bash
git clone https://github.com/nyvantran/ChatbotPTITHCM
cd ChatbotPTITHCM

# Tạo môi trường ảo
python -m venv venv
source venv/bin/activate  # Linux/macOS
# hoặc
venv\Scripts\activate     # Windows

# Cài đặt thư viện
pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường
Tạo file `.env` từ file mẫu và điền thông tin:
```bash
cp .env.example .env
```
Các biến quan trọng: `GOOGLE_API_KEY`, `MONGODB_URL`, `SECRET_KEY`.

### 3. Nạp dữ liệu vào Vector Database
Đặt các file tài liệu (`.pdf`, `documents.json`) vào thư mục `data/`, sau đó chạy:
```bash
python ingest.py
```
*Lưu ý: Script sẽ tự động chia nhỏ văn bản (chunking) và tạo embedding để nạp vào MongoDB.*

### 4. Khởi chạy ứng dụng
```bash
python main.py
```
Mặc định ứng dụng sẽ chạy tại: `http://localhost:8000`

## 🖥 Hướng dẫn sử dụng

- **Giao diện người dùng**:
  - Truy cập `http://localhost:8000/user` để Đăng ký/Đăng nhập.
  - Sau khi đăng nhập, hệ thống sẽ tự động chuyển hướng sang `http://localhost:8000/chat` để bạn bắt đầu hỏi đáp.
- **Tài liệu API**:
  - `/docs`: Swagger UI để thử nghiệm các API trực tiếp.

## 📂 Cấu trúc thư mục

```text
ChatbotPTITHCM/
├── app/
│   ├── api/v1/         # Các endpoint API (auth, chat)
│   ├── core/           # Cấu hình hệ thống, logic RAG, factory
│   ├── static/         # Giao diện HTML/CSS/JS (/user và /chat)
│   └── ...
├── data/               # Thư mục chứa tài liệu PDF, JSON
├── ingest.py           # Script nạp dữ liệu vào VectorDB
├── main.py             # File khởi chạy server FastAPI
└── requirements.txt    # Danh sách thư viện cần thiết
```

---
