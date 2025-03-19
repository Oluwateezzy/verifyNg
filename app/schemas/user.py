from pydantic import BaseModel, EmailStr, Field, constr
from uuid import UUID
from datetime import datetime
from typing import Optional, Union
import re

pattern = r"^\+?(\d[\d-. ]+)?(\([\d-. ]+\))?[\d-. ]+\d$"


class UserBase(BaseModel):
    email: EmailStr = Field(title="Email Address")
    first_name: str = Field(title="First Name")
    last_name: str = Field(title="Last Name")
    middle_name: Union[str, None] = Field(title="Middle Name")
    phone_number: Union[str, None] = Field(title="Phone Number")
    nin: str = Field(title="National Identification Number")
    is_identical: bool = Field(title="Is Identical")
    photo_image: Optional[str] = Field(title="Photo Image")
    government_id: Optional[str] = Field(title="Government ID")
    thumb_photo: Optional[str] = Field(title="Thumb Photo")


class UserCreate(UserBase):
    password: str = Field(title="Hashed Password")


class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class loginDTO(BaseModel):
    email: EmailStr = Field(title="Email Address")
    password: constr(min_length=6, max_length=100) = Field(title="Password")


class EmailDTO(BaseModel):
    email: EmailStr = Field(title="Email Address")
