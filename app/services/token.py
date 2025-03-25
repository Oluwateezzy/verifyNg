from app.models.token import Token
from uuid import UUID
from app.schemas.token import TokenDTO
from sqlalchemy.orm import Session


def create_token(db: Session, data: TokenDTO, user_id: UUID):
    new_token = Token(**data.dict(), user_id=user_id)
    db.add(new_token)
    db.commit()
    db.refresh(new_token)

    return new_token


def get_token(db: Session, token: str):
    token = db.query(Token).filter(Token.token == token).first()

    return token
