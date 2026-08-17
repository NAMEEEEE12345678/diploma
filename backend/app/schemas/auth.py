from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=120, examples=["Анна Иванова"])
    email: EmailStr = Field(examples=["anna@example.com"])
    password: str = Field(min_length=8, max_length=128, examples=["strong-password-123"])

    @field_validator("full_name")
    @classmethod
    def full_name_must_not_be_blank(cls, value: str) -> str:
        normalized_value = value.strip()
        if not normalized_value:
            raise ValueError("Имя не может состоять только из пробелов.")
        return normalized_value


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
