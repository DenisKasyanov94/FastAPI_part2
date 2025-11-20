import datetime
from typing import Optional, List

from pydantic import BaseModel


class IdResponse(BaseModel):
    id: str


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    author: str


class GetAdvertisementResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    price: float
    author: str
    created_at: datetime.datetime


class SearchAdvertisementResponse(BaseModel):
    advertisements: List[GetAdvertisementResponse]


class UpdateAdvertisementRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    author: Optional[str] = None