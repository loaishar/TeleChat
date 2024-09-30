from fastapi import FastAPI, Depends
from database import engine, Base  # Update to remove telechat_backend
from routers import users, chat    # Update to remove telechat_backend
from dotenv import load_dotenv
import os
from jose import jwt
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Load necessary environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")
ACS_ENDPOINT = os.getenv("ACS_ENDPOINT")

# Create the FastAPI app
app = FastAPI()

# Create database tables with error handling
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error creating database tables: {e}")

# Include routers
app.include_router(users.router)
app.include_router(chat.router)

# Root endpoint
@app.get('/')
def read_root():
    return {'message': 'Welcome to TeleChat API'}

# Generate access token (example using SECRET_KEY and JWT)
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Example endpoint using ACS and environment variables
@app.get('/acs-config')
def get_acs_config():
    return {
        "ACS_CONNECTION_STRING": ACS_CONNECTION_STRING,
        "ACS_ENDPOINT": ACS_ENDPOINT
    }

# Example token creation endpoint
@app.post("/token")
def login_for_access_token():
    user_data = {"sub": "example_user"}  # Example user data, replace with actual
    access_token = create_access_token(user_data)
    return {"access_token": access_token, "token_type": "bearer"}
