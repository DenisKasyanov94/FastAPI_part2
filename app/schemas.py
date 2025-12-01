from pydantic import BaseModel, EmailStr, validator, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid


# Enum для групп пользователей
class UserGroup(str, Enum):
    USER = "user"
    ADMIN = "admin"


# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    group: UserGroup = UserGroup.USER

    @validator('group', pre=True)
    def validate_group(cls, v):
        if isinstance(v, str) and v not in ['user', 'admin']:
            raise ValueError('Group must be "user" or "admin"')
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: uuid.UUID
    group: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # ← ИСПРАВЛЕНО (вместо class Config)


# Auth Schemas
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Advertisement Schemas
class AdvertisementBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float


class AdvertisementCreate(AdvertisementBase):
    pass


class AdvertisementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class AdvertisementResponse(AdvertisementBase):
    id: uuid.UUID
    author_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # ← ИСПРАВЛЕНО (вместо class Config)


# Для обратной совместимости
class IdResponse(BaseModel):
    id: uuid.UUID
