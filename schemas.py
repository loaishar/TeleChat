from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  # For Pydantic v2 (if Pydantic v1, use `orm_mode = True`)

class Token(BaseModel):
    access_token: str
    token_type: str

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    sender_id: int
    chat_thread_id: str
    timestamp: datetime

    class Config:
        from_attributes = True

class ChatThreadCreate(BaseModel):
    topic: str

class ChatThreadResponse(BaseModel):
    id: str
    topic: str
    created_on: datetime

    class Config:
        from_attributes = True

class ChatParticipant(BaseModel):
    user_id: int
    display_name: str

class ChatThreadDetails(ChatThreadResponse):
    participants: List[ChatParticipant]
    last_message: Optional[MessageResponse] = None

class UserInChat(BaseModel):
    user_id: int
    display_name: str
    azure_communication_id: str

class AddParticipantsRequest(BaseModel):
    participants: List[UserInChat]