from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Advertisement


async def get_advertisement_by_id(session: AsyncSession, advertisement_id: str) -> Advertisement:
    advertisement = await session.get(Advertisement, advertisement_id)
    if advertisement is None:
        raise HTTPException(404, "Advertisement not found")
    return advertisement


async def add_advertisement(session: AsyncSession, advertisement: Advertisement):
    session.add(advertisement)
    try:
        await session.commit()
    except IntegrityError as err:
        await session.rollback()
        raise HTTPException(409, "Advertisement creation failed")


async def delete_advertisement(session: AsyncSession, advertisement: Advertisement):
    await session.delete(advertisement)
    await session.commit()


async def search_advertisements(
        session: AsyncSession,
        title: str = None,
        description: str = None,
        author: str = None,
        min_price: float = None,
        max_price: float = None
):
    query = select(Advertisement)

    if title:
        query = query.where(Advertisement.title.ilike(f"%{title}%"))
    if description:
        query = query.where(Advertisement.description.ilike(f"%{description}%"))
    if author:
        query = query.where(Advertisement.author.ilike(f"%{author}%"))
    if min_price is not None:
        query = query.where(Advertisement.price >= min_price)
    if max_price is not None:
        query = query.where(Advertisement.price <= max_price)

    query = query.order_by(Advertisement.created_at.desc())
    result = await session.scalars(query)
    return result.all()