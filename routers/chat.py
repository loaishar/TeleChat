from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import auth
import database

router = APIRouter(
    prefix='/chat',
    tags=['Chat'],
)

# Mock data for chat threads (for demonstration)
chat_threads = [
    {"user": "user1", "messages": ["Hello", "How are you?"]},
    {"user": "user2", "messages": ["Hi", "What's up?"]}
]

@router.get('/threads')
def get_threads(current_user=Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    user = current_user.username
    # Simulate fetching user-specific chat threads (replace with actual DB interaction)
    user_threads = [thread for thread in chat_threads if thread["user"] == user]
    if not user_threads:
        raise HTTPException(status_code=404, detail="No chat threads found.")
    return user_threads

@router.post('/send')
def send_message(content: str, current_user=Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    user = current_user.username
    # Simulate saving message to the thread (replace with actual DB interaction)
    for thread in chat_threads:
        if thread["user"] == user:
            thread["messages"].append(content)
            return {"status": "Message sent"}
    return {"status": "No active thread found for user"}
