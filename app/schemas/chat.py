from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class MessageBase(BaseModel):
    content: str
    role: str  # 'user' or 'assistant'


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: str
    created_at: datetime


class ConversationBase(BaseModel):
    title: Optional[str] = "New Conversation"


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    history: List[MessageBase] = []


class HistoryResponse(BaseModel):
    history: List[MessageBase]
