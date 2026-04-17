from fastapi import FastAPI
from app.api.v1 import api_router
from app.core.config.logging_config import setup_logging

app = FastAPI(
    title="Chatbot PTITHCM API",
    description="Backend for RAG Chatbot using LangChain and FastAPI",
    version="1.0.0"
)

# Initialize logging
setup_logging()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Chatbot PTITHCM API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
