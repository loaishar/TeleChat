from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import ChatCreate, MessageCreate
from azure.communication.chat import ChatClient
from azure.communication.identity import CommunicationIdentityClient
from auth import oauth2_scheme
import os

chat_router = APIRouter()

ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Implement user authentication logic here
    # This is a placeholder; you should implement proper JWT validation
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

@chat_router.post("/create")
def create_chat(chat: ChatCreate, current_user: User = Depends(get_current_user)):
    identity_client = CommunicationIdentityClient.from_connection_string(ACS_CONNECTION_STRING)
    chat_client = ChatClient.from_connection_string(ACS_CONNECTION_STRING)

    # Create a chat thread
    create_chat_thread_result = chat_client.create_chat_thread(topic=chat.topic)
    chat_thread_client = chat_client.get_chat_thread_client(create_chat_thread_result.chat_thread.id)
    
    # Add the current user to the chat
    user_id = identity_client.create_user().communication_user_id
    chat_thread_client.add_participants([{"communication_id": user_id}])
    
    return {"thread_id": create_chat_thread_result.chat_thread.id, "topic": chat.topic}

@chat_router.post("/{thread_id}/message")
def send_message(thread_id: str, message: MessageCreate, current_user: User = Depends(get_current_user)):
    chat_client = ChatClient.from_connection_string(ACS_CONNECTION_STRING)
    chat_thread_client = chat_client.get_chat_thread_client(thread_id)
    
    send_message_result = chat_thread_client.send_message(content=message.content)
    return {"id": send_message_result.id}

@chat_router.get("/{thread_id}/messages")
def get_messages(thread_id: str, current_user: User = Depends(get_current_user)):
    chat_client = ChatClient.from_connection_string(ACS_CONNECTION_STRING)
    chat_thread_client = chat_client.get_chat_thread_client(thread_id)
    
    messages = chat_thread_client.list_messages()
    return [{"id": message.id, "content": message.content, "sender_display_name": message.sender_display_name, "created_on": message.created_on.isoformat()} for message in messages]