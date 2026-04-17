from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.v1 import api_router
from app.core.config.logging_config import setup_logging
import os

app = FastAPI(
    title="Chatbot PTITHCM API",
    description="Backend for RAG Chatbot using LangChain and FastAPI",
    version="1.0.0"
)

# Initialize logging
setup_logging()

# Route API
app.include_router(api_router, prefix="/api/v1")

# Route for Static Files (CSS/JS if needed)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return FileResponse("app/static/user.html")

@app.get("/user")
async def user_page():
    return FileResponse("app/static/user.html")

@app.get("/chat")
async def chat_page():
    return FileResponse("app/static/chat.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
