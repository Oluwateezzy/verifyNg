from pydantic import BaseModel, Field
from app.utils.enums.token import TokenType


class TokenDTO(BaseModel):
    token: str = Field(title="Token", examples=["1234", "5678", "9101"])
    type: TokenType = Field(
        title="Token Type", examples=["EMAIL_CONFIRMATION", "PASSWORD_RESET"]
    )
