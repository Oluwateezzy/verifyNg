from datetime import timedelta
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.models.users import User
from app.services.digital_ocean import upload_file
from app.services.email import send_email
from app.services.imgbb import upload_file_imgbb
from app.services.twillo import send_otp
from app.utils.generate_random_token import generate_random_code
from app.utils.result.base_result import BaseResult
from sqlalchemy.orm import Session
from app.core.config import settings

from app.core.database import get_db
from app.schemas.user import (
    EmailDTO,
    PhoneNumberDTO,
    ResetPasswordDTO,
    UserCreate,
    VerifyEmailTokenDTO,
    VerifyPhoneNumberTokenDTO,
    loginDTO,
)
from app.services.user import create_user, get_user_by_email, get_user_by_phone_number
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

    send_email(
        to_email=data.email,
        subject="Welcome to the platform",
        body=f"Welcome {user.email}, you have successfully registered on the platform. \n {user.token}",
    )

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
async def validateDocs(file: UploadFile = File(...)):
    file_s3 = await upload_file_imgbb(file)
    return BaseResult(
        status=status.HTTP_200_OK,
        message="File uploaded successfully",
        data=file_s3.get("data").get("url"),
    )


@router.post("/sendEmailToken", summary="Send Email Token")
def sendEmailToken(
    data: EmailDTO, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    token = generate_random_code(4)
    user.token = token
    db.commit()

    background_tasks.add_task(
        send_email,
        data.email,
        "OTP",
        f"Your OTP is {token}",
    )

    return BaseResult(status=status.HTTP_200_OK, message="OTP sent successfully")


@router.post("/sendPhoneNumber", summary="Send Phone Token")
def sendPhoneNumber(
    data: PhoneNumberDTO,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = get_user_by_phone_number(db, data.phone_number)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    token = generate_random_code(4)
    user.token = token
    db.commit()

    # background_tasks.add_task(send_otp, data.phone_number, token)

    return BaseResult(status=status.HTTP_200_OK, message="OTP sent successfully")


@router.post("/verifyEmail", summary="Verify Email")
def verifyEmail(data: VerifyEmailTokenDTO, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )
    if user.token != data.token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    if user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified"
        )

    user.is_email_verified = True
    user.token = None
    db.commit()

    return BaseResult(status=status.HTTP_200_OK, message="Email verified successfully")


@router.post("/verifyPhoneNumber", summary="Verify Phone Number")
def verifyPhoneNumber(data: VerifyPhoneNumberTokenDTO, db: Session = Depends(get_db)):
    user = get_user_by_phone_number(db, data.phone_number)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    if user.is_phone_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already verified",
        )

    if user.token != data.token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    user.is_phone_verified = True
    user.token = None
    db.commit()

    return BaseResult(status=status.HTTP_200_OK, message="Email verified successfully")


@router.patch("/resetPassword", summary="Reset Password")
def resetPassword(data: ResetPasswordDTO, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )
    if user.token != data.token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    user.hashed_password = hash_password(data.password)
    user.token = None
    db.commit()

    return BaseResult(status=status.HTTP_200_OK, message="Password reset successfully")


@router.post("/forgotPassword", summary="Forgot Password")
def forgotPassword(
    data: EmailDTO, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    token = generate_random_code(4)
    user.token = token
    db.commit()

    # Send email in the background
    background_tasks.add_task(
        send_email,
        data.email,
        "Reset Password",
        f"Your reset password token is {token}",
    )

    return BaseResult(
        status=status.HTTP_200_OK, message="Reset password token sent successfully"
    )
