from fastapi import APIRouter, Depends, status

from app.core.database import get_db
from app.core.security import get_current_user, hash_password, verify_password
from app.models.users import User
from app.schemas.user import PasswordDTO, UserBaseUpdate
from app.services.user import get_user
from app.utils.result.base_result import BaseResult


router = APIRouter()


@router.get("/profile", summary="Retrieve the authenticated user's profile")
def profile(current_user: User = Depends(get_current_user)):
    return BaseResult(
        status=status.HTTP_200_OK, message="User profile", data=current_user
    )


@router.patch("/password", summary="Update the authenticated user's password")
def updatePassword(
    data: PasswordDTO,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    userData = get_user(db, current_user.id)

    if verify_password(data.old_password, userData.hashed_password):
        userData.hashed_password = hash_password(data.new_password)
        db.commit()
        db.refresh(userData)

        return BaseResult(
            status=status.HTTP_200_OK, message="Password updated successfully"
        )

    return BaseResult(status=status.HTTP_400_BAD_REQUEST, message="Incorrect password")


@router.patch("/profile", summary="Update the authenticated user's profile information")
def updateProfile(
    data: UserBaseUpdate,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    userData = get_user(db, current_user.id)

    userData.update(data.dict(exclude_none=True))
    db.commit()
    db.refresh(userData)

    return BaseResult(
        status=status.HTTP_200_OK, message="Profile updated successfully", data=userData
    )


@router.delete(
    "/account", summary="Permanently delete the authenticated user's account"
)
def deleteAccount(db=Depends(get_db), current_user: User = Depends(get_current_user)):
    userData = get_user(db, current_user.id)

    db.delete(userData)
    db.commit()

    return BaseResult(status=status.HTTP_200_OK, message="Account deleted successfully")
