from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "Chatbot PTITHCM"
    API_V1_STR: str = "/api/v1"

    SYSTEM_PROMPT: str = """bạn là chuyên gia tổng hợp thông tin của Học viện công nghệ bưu chính viễn thông cở sở thành phố Hồ Chí Minh. bạn phải tuân thủ một số yêu cầu sau \n
    - hãy trả lời dựa trên những gì bạn tìm được bằng công cụ search. \n
    - khi trả lời phải để trích dẫn nguồn cho những thông tin bạn đưa ra. \n
    - nếu không tìm thấy thông tin liên quan có thể trả lời không biết hoặc ko có trong csdl \n"""

    # LLM Providers
    OPENAI_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None

    # Security
    SECRET_KEY: str = "your-secret-key-change-it-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    MONGODB_URL: str | None = None
    DATABASE_NAME: str = "chatbot_ptit"
    VECTOR_INDEX_NAME: str = "vector_index"
    SQLITE_URL: str = r"D:\Project\AI\ChatbotPTITHCM\chat_history.db"

    # LLM Settings
    DEFAULT_LLM_PROVIDER: str = "google"  # google, openai, anthropic
    DEFAULT_LLM: str = "gemini-2.5-flash-lite"

    EMBEDDING_MODEL: str = "models/embedding-001"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
