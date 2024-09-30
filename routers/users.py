from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User
from schemas import UserResponse, UserCreate, Token
from utils import hash_password, verify_password
from auth import create_access_token
from database import SessionLocal
from azure_chat import create_acs_user

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

@router.post('/register', response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(SessionLocal)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Username already registered')
    
    hashed_password = hash_password(user.password)
    acs_user, acs_token = create_acs_user()
    
    new_user = User(
        username=user.username,
        hashed_password=hashed_password,
        acs_identity=acs_user.properties['id'],
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login', response_model=Token)
def login(user: UserCreate, db: Session = Depends(SessionLocal)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    
    access_token = create_access_token(data={'sub': db_user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}
