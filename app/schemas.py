from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime  # Исправленный импорт

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    group: Optional[str] = "user"  # По умолчанию "user"

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: str
    group: str
    is_active: bool
    created_at: datetime  # Исправлено

    class Config:
        orm_mode = True

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
    id: str
    author_id: str
    created_at: datetime  # Исправлено

    class Config:
        orm_mode = True

# Для обратной совместимости (можно удалить после обновления всех файлов)
class IdResponse(BaseModel):
    id: str

class GetAdvertisementResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    price: float
    author: str
    created_at: datetime  # Исправлено: убрал .datetime

class SearchAdvertisementResponse(BaseModel):
    advertisements: List[GetAdvertisementResponse]