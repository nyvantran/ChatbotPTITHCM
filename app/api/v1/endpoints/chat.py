from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.deps import get_current_user
from app.schemas.chat import (
    ConversationCreate, ChatRequest, ChatResponse, MessageBase, HistoryResponse
)
from app.services.chat_service import ChatService
from typing import List

router = APIRouter()
chat_service = ChatService()


@router.post("/conversations", response_model=dict)
async def create_conversation(
        data: ConversationCreate,
        current_user: dict = Depends(get_current_user)
):
    conv_id = await chat_service.create_conversation(current_user["id"], data)
    if conv_id is None:
        return HTTPException(status_code=404, detail="không có user id này")
    return {"id": conv_id, "message": "Đã tạo cuộc trò chuyện mới"}


@router.get("/conversations", response_model=List[dict])
async def list_conversations(
        current_user: dict = Depends(get_current_user)
):
    return await chat_service.get_user_conversations(current_user["id"])


@router.post("/conversations/{conversation_id}", response_model=ChatResponse)
async def chat_with_agent(
        conversation_id: str,
        request: ChatRequest,
        current_user: dict = Depends(get_current_user)
):
    conv, _ = await chat_service.get_conversation(conversation_id, get_his=False)
    if not conv or conv["user_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Không tìm thấy cuộc trò chuyện")

    all_messages = await chat_service.get_agent_response(conversation_id, request.message)
    await chat_service.update_conversation_timestamp(conversation_id)

    response = all_messages[-1].content
    response = response if isinstance(response, str) else response[-1]["text"]
    return ChatResponse(
        response=response,
        conversation_id=conversation_id,
        history=[]
    )


@router.get("/conversations/{conversation_id}", response_model=HistoryResponse)
async def get_conversation(conversation_id: str):
    conv, his_data = await chat_service.get_conversation(conversation_id, get_his=True)
    if conv is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy cuộc trò chuyện")
    history = [MessageBase(content=str(his["content"]), role=his["role"]) for his in his_data]
    return HistoryResponse(history=history)


@router.delete("/conversations/{conversation_id}", response_model=dict)
def delete_conversation(conversation_id: str):
    status = chat_service.delete_conversation(conversation_id)
    if status == "ok":
        return {"id": conversation_id, "message": "Đã xóa cuộc trò chuyện"}
    else:
        raise HTTPException(status_code=500, detail=status)
