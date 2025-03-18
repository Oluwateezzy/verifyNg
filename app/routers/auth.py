from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import create_access_token, verify_password
from app.models.users import User
from app.utils.result.base_result import BaseResult
from sqlalchemy.orm import Session
from app.core.config import settings

from app.core.database import get_db
from app.schemas.user import UserBase, UserCreate, loginDTO
from app.services.user import create_user, get_user_by_email
from app.utils.validate_email import validate_email


router = APIRouter()


@router.post("/register", summary="Register a new user")
def register(data: UserCreate, db: Session = Depends(get_db)):
    if not validate_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email address"
        )
    user = get_user_by_email(db, data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )
    user = create_user(db, data)
    del user.hashed_password

    return BaseResult(
        status=status.HTTP_201_CREATED,
        message="User created successfully",
        data=user,
    )


@router.post("/login", summary="Login a user")
def login(data: loginDTO, db: Session = Depends(get_db)):
    if not validate_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email address"
        )
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return BaseResult(
        status=status.HTTP_200_OK,
        message="Login successful",
        data={"token": access_token},
    )


@router.post("/validateDocs", summary="Validate Documents and return docs URL")
def validateDocs():
    return {"message": "Validate Docs"}


@router.post("/sendOTP", summary="Send OTP to user")
def sendOTP():
    return {"message": "Send OTP"}


@router.post("/verifyOTP", summary="Verify OTP")
def verifyOTP():
    return {"message": "Verify OTP"}


@router.post("/resetPassword", summary="Reset Password")
def resetPassword():
    return {"message": "Reset Password"}


@router.post("/forgotPassword", summary="Forgot Password")
def forgotPassword():
    return {"message": "Forgot Password"}
