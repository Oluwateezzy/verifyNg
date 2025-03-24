from uuid import UUID
from app.core.security import hash_password
from app.models.users import User
from app.models.token import Token
from app.schemas.user import UserCreate
from app.utils.enums.token import TokenType
from app.utils.generate_random_token import generate_random_code
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    token = generate_random_code(4)
    db_user = User(
        **user.model_dump(exclude={"password"}),
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    new_token = Token(
        token=token, type=TokenType.EMAIL_CONFIRMATION, user_id=db_user.id
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)

    return db_user, new_token


def get_user(db: Session, user_id: UUID):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()

    return user


def get_user_by_phone_number(db: Session, phoneNumber: str):
    user = db.query(User).filter(User.phone_number == phoneNumber).first()

    return user


def update_user(db: Session, user_id: UUID, user: UserCreate):
    db_user = get_user(db, user_id)
    db_user.update(user.model_dump())
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: UUID):
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
    return db_user
