import pymongo

from app.storage.mongodb import mongo_storage
from app.storage import checkpoint_storage
from app.core.rag.agent import RagAgent
from app.schemas.chat import ConversationCreate
from app.services.user_service import UserService
from datetime import datetime
from bson import ObjectId
from typing import List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage


class ChatService:
    last_id_conversation: int = -1
    checkpoint = checkpoint_storage.get_checkpointer()
    db = mongo_storage.get_db()
    collection = db["conversations"]

    def __init__(self):
        # Sử dụng pymongo sync client
        if self.last_id_conversation == -1:
            self.last_id_conversation = int(self.collection.find_one(sort=[("conversation_id", pymongo.DESCENDING)])[
                                                "conversation_id"])

    @staticmethod
    def format_message(message: BaseMessage):
        if isinstance(message, HumanMessage):
            return {
                "role": "user",
                "content": message.content,
            }
        elif isinstance(message, AIMessage):
            if message.content == "":
                # return {
                #     "role": "assistant",
                #     # "content": message.additional_kwargs,
                #     "content": "",
                # }
                return None
            elif message.content != "":
                return {
                    "role": "assistant",
                    "content": message.content,
                }
        # elif isinstance(message, ToolMessage):
        #     return {
        #         "role": "tools",
        #         "content":"",
        #     }
        return None

    async def create_conversation(self, user_id: str, data: ConversationCreate) -> str:
        """tạo cuộc trò chuyện mới của 1 user"""
        user_service = UserService()
        if user_service.get_user_by_id(user_id) is None:
            return None
        self.last_id_conversation += 1

        new_conv = {
            "user_id": user_id,
            "title": data.title,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "conversation_id": str(self.last_id_conversation)
        }
        # Thao tác đồng bộ qua pymongo
        result = self.collection.insert_one(new_conv)
        return str(result.inserted_id)

    async def get_user_conversations(self, user_id: str) -> List[dict]:
        """lấy danh sách các cuộc trò chuyện"""
        cursor = self.collection.find({"user_id": user_id}).sort("updated_at", -1)
        conversations = list(cursor.limit(100))
        for conv in conversations:
            conv["_id"] = str(conv["_id"])
        return conversations

    async def get_conversation(self, conversation_id: str, get_his=True) -> dict:
        conv = self.collection.find_one({"_id": ObjectId(conversation_id)})
        if conv is None:
            return None, []
        configure = {"configurable": {"thread_id": str(conv["conversation_id"])}}
        if conv:
            conv["id"] = str(conv["_id"])
        history = []
        if get_his:
            history_data = self.checkpoint.get(config=configure)
            if history_data is None:
                return conv, []
            history = [self.format_message(his) for his in history_data["channel_values"]["messages"]]
            history = filter(lambda x: x is not None, history)
        return conv, history

    async def update_conversation_timestamp(self, conversation_id: str):
        self.collection.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"updated_at": datetime.utcnow()}}
        )

    async def get_agent_response(self, conversation_id: str, user_message: str) -> List[BaseMessage]:
        """
        Hàm xử lý tin nhắn người dùng:
        - Kiểm tra độ dài hội thoại để tóm tắt (Summarization Middleware).
        - Gọi Agent xử lý và lưu lịch sử.
        """
        id = self.collection.find_one({"_id": ObjectId(conversation_id)})["conversation_id"]
        configure = {"configurable": {"thread_id": str(id)}}
        human_msg = {"messages":
            [
                {"role": "user", "content": user_message}
            ]
        }
        agent = RagAgent.get_agent()
        return agent.invoke(human_msg, configure)["messages"]

    def delete_conversation(self, conversation_id: str) -> str:
        conv = self.collection.find_one({"_id": ObjectId(conversation_id)})
        conv_id = str(conv["conversation_id"])

        try:
            self.checkpoint.delete_thread(conv_id)
            self.collection.delete_one({"_id": ObjectId(conversation_id)})
        except Exception as e:
            return str(e)

        return "ok"
