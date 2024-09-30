from pydantic import BaseModel

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

class MessageResponse(MessageBase):
    sender_id: int
    receiver_id: int
    timestamp: str
