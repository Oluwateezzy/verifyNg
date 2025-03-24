from pydantic import BaseModel, ConfigDict, EmailStr, Field, constr
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


class UserBaseUpdate(BaseModel):
    first_name: Optional[str] = Field(title="First Name")
    last_name: Optional[str] = Field(title="Last Name")
    middle_name: Optional[Union[str, None]] = Field(title="Middle Name")


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


class PhoneNumberDTO(BaseModel):
    phone_number: str = Field(title="Phone Number")


class ResetPasswordDTO(BaseModel):
    email: EmailStr = Field(title="Email Address")
    token: str = Field(title="Token")
    password: constr(min_length=6, max_length=100) = Field(title="Password")


class VerifyEmailTokenDTO(BaseModel):
    token: str = Field(title="Token")
    email: EmailStr = Field(title="Email Address")


class VerifyPhoneNumberTokenDTO(BaseModel):
    token: str = Field(title="Token")
    phone_number: EmailStr = Field(title="Email Address")


class PasswordDTO(BaseModel):
    old_password: constr(min_length=6, max_length=100) = Field(title="Old Password")
    new_password: constr(min_length=6, max_length=100) = Field(title="New Password")
