from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(min_length=1, max_length=30)
    last_name: str = Field(min_length=1, max_length=30)
    email: EmailStr
    phone: str = Field(min_length=5, max_length=25)
    birthday: date


class ContactUpdate(ContactModel):
    done: bool


class ContactStatusUpdate(BaseModel):
    done: bool


class ContactResponse(ContactModel):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=1, max_length=30)
    email: EmailStr
    password: str = Field(min_length=3, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str    

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr    
