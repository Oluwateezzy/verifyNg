from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from app.core.config import settings
from app.core.database import get_db
from app.schemas.user import UserBase, UserResponse
import jwt
from app.models.users import User
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from jwt.exceptions import PyJWTError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
jwt_scheme = HTTPBearer()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(jwt_scheme),
    db: Session = Depends(get_db),
) -> UserBase:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    bearer_token = token.credentials

    try:
        payload = jwt.decode(
            bearer_token, settings.secret_key, algorithms=[settings.algorithm]
        )
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return UserResponse.model_validate(user)
