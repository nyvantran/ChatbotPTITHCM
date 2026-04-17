from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

from app.core.config.settings import settings
from app.core.rag.factory import LLMFactory
from app.core.rag.retriever import retriever
from app.storage.sqlite import checkpoint_storage


class RagAgent:
    __agent = None

    @classmethod
    def get_agent(cls, provider: str = settings.DEFAULT_LLM_PROVIDER):
        if cls.__agent is None:
            model = LLMFactory.get_llm(provider)
            tools = [retriever]
            system_prompt = settings.SYSTEM_PROMPT
            checkpoint = checkpoint_storage.get_checkpointer()
            middleware = [SummarizationMiddleware(
                model=model,
                trigger=("tokens", 4000),
                keep=("messages", 20)
            )]
            cls.__agent = create_agent(
                model=model,
                tools=tools,
                middleware=middleware,
                system_prompt=system_prompt,
                checkpointer=checkpoint,
            )
        return cls.__agent
