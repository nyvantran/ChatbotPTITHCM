import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config.settings import settings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.embeddings import Embeddings


class LLMFactory:
    @staticmethod
    def get_llm(provider: str = settings.DEFAULT_LLM_PROVIDER) -> BaseChatModel:
        if provider == "google":
            if os.environ.get("GOOGLE_API_KEY") is None:
                os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
            return ChatGoogleGenerativeAI(
                model=settings.DEFAULT_LLM,
                temperature=0.7
            )
        elif provider == "openai":
            if os.environ.get("OPENAI_API_KEY") is None:
                os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
            return ChatOpenAI(
                model=settings.DEFAULT_LLM,
                temperature=0.7,
                api_key=settings.OPENAI_API_KEY
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    @staticmethod
    def get_embeddings(provider: str = settings.DEFAULT_LLM_PROVIDER) -> Embeddings:
        if provider == "google":
            if os.environ.get("GOOGLE_API_KEY") is None:
                os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
            return GoogleGenerativeAIEmbeddings(
                model=settings.EMBEDDING_MODEL,
            )
        elif provider == "openai":
            if os.environ.get("OPENAI_API_KEY") is None:
                os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
            return OpenAIEmbeddings(
                model=settings.EMBEDDING_MODEL,
                api_key=settings.OPENAI_API_KEY
            )
        elif provider == "huggingface":
            return HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL
            )
        else:
            raise ValueError(f"Unsupported Embedding provider: {provider}")
