from uuid import UUID
from app.core.security import hash_password
from app.models.users import User
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def create_user(db: Session, user: UserCreate):
    password_hash = hash_password(user.password)
    db_user = User(**user.model_dump(), hashed_password=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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
