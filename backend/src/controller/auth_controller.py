import bcrypt
import jwt
from jwt import PyJWTError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from src.service.database import db
from dotenv import load_dotenv
import os

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
security = HTTPBearer()

def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise PyJWTError()
        return {"username": username}
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau kadaluarsa",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Digunakan di Depends() untuk proteksi route
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    print("Credentials:", credentials)
    token = credentials.credentials
    return decode_token(token)

async def register(username: str, password: str):
    # Check if user already exists
    user_ref = db.collection('users').document(username)
    if user_ref.get().exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Save user to Firestore
    user_ref.set({
        'username': username,
        'password': hashed_password,
        'created_at': datetime.now().isoformat()
    })

    return {"message": "User registered successfully"}

async def login(username: str, password: str):
    user_ref = db.collection('users').document(username)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    user_data = user_doc.to_dict()
    
    # Verify password
    if not bcrypt.checkpw(password.encode('utf-8'), user_data['password']):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Create JWT token
    token_data = {
        "username": user_data['username'],
    }
    token = jwt.encode(token_data, JWT_SECRET, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}




