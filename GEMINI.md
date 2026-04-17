# PROJECT CONTEXT: RAG BACKEND (LANGCHAIN + FASTAPI)

## Tổng quan dự án

Hệ thống Backend cung cấp API cho chatbot RAG. Mục tiêu là xây dựng một kiến trúc linh hoạt, cho phép thay đổi LLM
Provider (OpenAI, Anthropic, Gemini) và Vector Database (Mongodb, Pinecone) chỉ bằng cách thay đổi cấu hình.

## Tech Stack

- **Framework:** FastAPI (Asynchronous).
- **Orchestration:** LangChain.
- **Data Validation:** Pydantic v2.
- **Database:** Mongodb atlas
- **Vector DB** Mongodb atlas
- **Inference:** LangChain LCEL (LangChain Expression Language).
- **Checkpoint:** SQLite

## VAI TRÒ CỦA BẠN (AI AGENT)

Bạn là một Senior Ai Engineer dày dặn kinh nghiệm và trả lời bằng tiếng việt. Nhiệm vụ của bạn là viết code sạch, dễ bảo
trì, an toàn và có hiệu suất cao.

### 1. Tính trừu tượng (Multi-provider Support)

- KHÔNG được viết cứng (hard-code) các lớp của OpenAI hay Anthropic vào Controller.
- Ưu tiên sử dụng các bản phân phối có sẵn của langchain
- Mọi Provider phải kế hoạch qua một Interface chung hoặc sử dụng `BaseChatModel` của LangChain.
- Sử dụng Pattern `Factory` để khởi tạo các thành phần dựa trên file `.env`.
- triển khai hệ thống theo hướng đối tượng

### 2. Cấu trúc thư mục (Folder Structure)

Khi tạo file mới, hãy tuân thủ sơ đồ:

- `app/api/`: Chứa các router FastAPI.
- `app/services/`: Chứa logic nghiệp vụ chính.
- `app/core/rag/`: Chứa LangChain Chains, Retrievers, và Prompt Templates.
- `app/schemas/`: Định nghĩa Pydantic models.
- `app/core/config/`: Quản lý biến môi trường và cài đặt provider.

### 3. Quy tắc Coding (Coding Convention)

- **Async:** Sử dụng `async def` cho tất cả các endpoint và hàm gọi I/O (Database, LLM API).
- **Logging:** Sử dụng module `logging` của Python để ghi lại các bước: (1) Nhận query, (2) Kết quả Retrieval, (3)
  Response từ LLM.
- **Type Hinting:** Mọi hàm phải có kiểu dữ liệu đầu vào và đầu ra.
- **LCEL:** Ưu tiên sử dụng cú pháp `|` của LangChain để xây dựng pipeline nhằm tối ưu tính modular.
- **API:** tuân thủ quy tắc restful api

## Những API đã hoàn thành

### 1. đăng ký tài khoản mới | post: /api/v1/auth/register  
Request body
```json 
{
  "email": "user@example.com",
  "password": "stringst",
  "confirm_password": "stringst"
}
```
	
Successful Response, code: 201
```json
{
  "email": "user@example.com",
  "id": "string",
  "is_active": true
}
```
### 2. đăng nhập tài khoản | post: /api/v1/auth/login
 Request body
```json 
{
  "email": "user@example.com",
  "password": "string"
}
```
	
Successful Response, code: 200
```json
{
  "access_token": "string",
  "token_type": "string"
}
```
### 3. post: /api/v1/auth/logout
### 4. lấy danh sách các cuộc trò chuyện | get: /api/v1/chat/conversations	
Successful Response, code: 200
```json
[
  {
    "additionalProp1": {}
  }
]
```
### 5. tạo cuộc trò chuyện mới | post: /api/v1/chat/conversations
 Request body
```json 
{
  "title": "New Conversation"
}
```
	
Successful Response, code: 200
```json
{
  "additionalProp1": {}
}
```
### 6. trò chuyện trong cuộc trò chuyện | post: /api/v1/chat/conversations/{conversation_id}
 Request body
```json 
{
  "message": "string"
}
```
	
Successful Response, code: 200
```json
{
  "response": "string",
  "conversation_id": "string",
  "history": []
}
```
### 7. lấy lịch sử cuộc trò chuyện | get: /api/v1/chat/conversations/{conversation_id}

Successful Response, code: 200
```json
{
  "history": [
    {
      "content": "string",
      "role": "string"
    }
  ]
}
```
