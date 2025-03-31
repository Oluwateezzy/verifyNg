from datetime import timedelta
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
    requests,
    status,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.token import TokenDTO
from app.services.email import send_email
from app.services.imgbb import upload_file_imgbb
from app.services.token import create_token, get_token
from app.services.twillo import send_otp
from app.utils.enums.token import TokenType
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


@router.post("/register", summary="Register a new user account")
def register(data: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user account by validating the provided email, checking if the email already exists, and creating a new user. Upon successful registration, a welcome email with a generated token is sent to the user.
    """

    if not validate_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email address"
        )
    user = get_user_by_email(db, data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    db_user, new_token = create_user(db, data)
    del db_user.hashed_password

    send_email(
        to_email=data.email,
        subject="Welcome to the platform",
        body=f"Welcome {db_user.email}, you have successfully registered on the platform. \n {new_token.token}",
    )

    return BaseResult(
        status=status.HTTP_201_CREATED,
        message="User created successfully",
        data={"token": new_token.token},
    )


@router.post("/login", summary="Authenticate a user and generate an access token")
def login(data: loginDTO, db: Session = Depends(get_db)):
    """
    Authenticates a user using their email and password, and generates an access token upon successful login.
    """
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


@router.post(
    "/documents/validate", summary="Validate uploaded documents and return their URLs"
)
async def validateDocs(file: UploadFile = File(...)):

    """
    Validates the uploaded document and returns its URL after uploading to an external service (e.g., ImgBB).
    """

    file_s3 = await upload_file_imgbb(file)
    return BaseResult(
        status=status.HTTP_200_OK,
        message="File uploaded successfully",
        data=file_s3.get("data").get("url"),
    )


@router.post(
    "/email/send-token", summary="Send an email verification token to the user"
)
def sendEmailToken(
    data: EmailDTO, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    """
    Sends an email verification token (OTP) to the user's email address for verification purposes.
    """
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    token = generate_random_code(4)
    create_token(db, TokenDTO(token=token, type=TokenType.EMAIL_CONFIRMATION), user.id)

    background_tasks.add_task(
        send_email,
        data.email,
        "OTP",
        f"Your OTP is {token}",
    )

    return BaseResult(status=status.HTTP_200_OK, message="OTP sent successfully")


@router.post(
    "/phone/send-token",
    summary="Send an SMS verification token to the user's phone number",
)
def sendPhoneNumber(
    data: PhoneNumberDTO,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Summary: Sends an SMS verification token (OTP) to the user's phone number for verification purposes.
    """
    user = get_user_by_phone_number(db, data.phone_number)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    token = generate_random_code(4)
    create_token(
        db, TokenDTO(token=token, type=TokenType.PHONE_NUMBER_CONFIRMATION), user.id
    )

    # background_tasks.add_task(send_otp, data.phone_number, token)

    return BaseResult(status=status.HTTP_200_OK, message="OTP sent successfully")


@router.post(
    "/email/verify", summary="Verify a user's email using a confirmation token"
)
def verifyEmail(data: VerifyEmailTokenDTO, db: Session = Depends(get_db)):
    """
    Verifies the user's email address using the provided confirmation token.
    """
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    if user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified"
        )

    token = get_token(db, data.token)
    if (
        not token
        or token.type != TokenType.EMAIL_CONFIRMATION
        or token.is_active is False
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    if token.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token does not belong to user",
        )

    user.is_email_verified = True
    token.is_active = False
    db.commit()

    return BaseResult(status=status.HTTP_200_OK, message="Email verified successfully")


@router.post("/phone/verify", summary="Verify a user's phone number using an OTP")
def verifyPhoneNumber(data: VerifyPhoneNumberTokenDTO, db: Session = Depends(get_db)):
    """
    Verifies the user's phone number using the provided OTP token.
    """
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

    token = get_token(db, data.token)

    if (
        not token
        or token.type != TokenType.PHONE_NUMBER_CONFIRMATION
        or token.is_active is False
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    if token.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token does not belong to user",
        )

    user.is_phone_verified = True
    token.is_active = False
    db.commit()

    return BaseResult(status=status.HTTP_200_OK, message="Email verified successfully")


@router.patch(
    "/password/reset", summary="Reset the user's password using a valid token"
)
def resetPassword(data: ResetPasswordDTO, db: Session = Depends(get_db)):
    """
    Resets the user's password using the provided reset token.
    """
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )
    if user.token != data.token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    token = get_token(db, data.token)

    if not token or token.type != TokenType.PASSWORD_RESET or token.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    if token.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token does not belong to user",
        )

    user.hashed_password = hash_password(data.password)
    token.is_active = False
    db.commit()

    return BaseResult(status=status.HTTP_200_OK, message="Password reset successfully")


@router.post(
    "/password/forgot",
    summary="Initiate a password reset by sending a recovery email",
)
def forgotPassword(
    data: EmailDTO, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    """
    Initiates a password reset by sending a recovery email with a token to the user's email address.
    """
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    token = generate_random_code(4)
    create_token(db, TokenDTO(token=token, type=TokenType.PASSWORD_RESET), user.id)

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
