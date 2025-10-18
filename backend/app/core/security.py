# from datetime import datetime, timedelta
# from jose import jwt
# from app.core.config import settings

# def create_access_token(data: dict, expires_delta: int = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         return payload
#     except Exception:
#         return None
# from datetime import datetime, timedelta
# from jose import jwt, JWTError
# from fastapi import Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# from app.core.config import settings
# from app.db.base import SessionLocal
# from app.db import crud

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# def create_access_token(data: dict, expires_delta: int = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(
#         minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES
#     )
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# # Dependency: DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Dependency: get current user
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
    
#     user = crud.get_user_by_email(db, email=email)
#     if user is None:
#         raise credentials_exception
#     return user
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.base import SessionLocal
from app.db import crud

# Use APIKeyHeader to read Authorization header
auth_header = APIKeyHeader(name="Authorization")

# Create JWT token
def create_access_token(data: dict):
    """Generate JWT token with user info."""
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Current user dependency
def get_current_user(token: str = Depends(auth_header), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token[len("Bearer "):]

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user
