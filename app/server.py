from fastapi import FastAPI, Query
from typing import Optional

from app.crud import (
    add_advertisement,
    delete_advertisement,
    get_advertisement_by_id,
    search_advertisements,
)
from app.database import SessionDependency
from app.lifespan import lifespan
from app.models import Advertisement
from app.schema import (
    CreateAdvertisementRequest,
    GetAdvertisementResponse,
    IdResponse,
    SearchAdvertisementResponse,
    UpdateAdvertisementRequest,
)

app = FastAPI(
    title="Advertisement API",
    description="Service for buying/selling advertisements",
    lifespan=lifespan,
)


@app.post("/advertisement", response_model=IdResponse)
async def create_advertisement(session: SessionDependency, item: CreateAdvertisementRequest):
    advertisement = Advertisement(
        title=item.title,
        description=item.description,
        price=item.price,
        author=item.author
    )
    await add_advertisement(session, advertisement)
    return {"id": advertisement.id}


@app.get("/advertisement/{advertisement_id}", response_model=GetAdvertisementResponse)
async def get_advertisement(session: SessionDependency, advertisement_id: str):
    advertisement = await get_advertisement_by_id(session, advertisement_id)
    return advertisement.dict


@app.get("/advertisement/", response_model=SearchAdvertisementResponse)
async def search_advertisement(
        session: SessionDependency,
        title: Optional[str] = Query(None),
        description: Optional[str] = Query(None),
        author: Optional[str] = Query(None),
        min_price: Optional[float] = Query(None),
        max_price: Optional[float] = Query(None)
):
    advertisements = await search_advertisements(
        session, title, description, author, min_price, max_price
    )
    return {"advertisements": [ad.dict for ad in advertisements]}


@app.patch("/advertisement/{advertisement_id}", response_model=IdResponse)
async def update_advertisement(
        session: SessionDependency,
        advertisement_id: str,
        item: UpdateAdvertisementRequest
):
    advertisement = await get_advertisement_by_id(session, advertisement_id)

    update_payload = item.dict(exclude_unset=True)
    for key, value in update_payload.items():
        setattr(advertisement, key, value)

    await add_advertisement(session, advertisement)
    return {"id": advertisement_id}


@app.delete("/advertisement/{advertisement_id}", response_model=IdResponse)
async def delete_advertisement(session: SessionDependency, advertisement_id: str):
    advertisement = await get_advertisement_by_id(session, advertisement_id)
    await delete_advertisement(session, advertisement)
    return {"id": advertisement_id}