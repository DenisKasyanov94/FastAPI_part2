from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
import uuid
from app.database import get_db
from app import crud, schemas, models
from app.dependencies import get_current_user, require_admin, optional_auth

router = APIRouter(prefix="/advertisement", tags=["advertisements"])


@router.post("/", response_model=schemas.AdvertisementResponse)
def create_advertisement(
        advertisement: schemas.AdvertisementCreate,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Только авторизованные пользователи могут создавать объявления
    return crud.create_advertisement(db, advertisement, current_user.id)


@router.get("/{advertisement_id}", response_model=schemas.AdvertisementResponse)
def get_advertisement(
        advertisement_id: uuid.UUID,
        current_user: Optional[models.User] = Depends(optional_auth),
        db: Session = Depends(get_db)
):
    advertisement = crud.get_advertisement_by_id(db, advertisement_id)
    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advertisement not found"
        )
    return advertisement


@router.patch("/{advertisement_id}", response_model=schemas.AdvertisementResponse)
def update_advertisement(
        advertisement_id: uuid.UUID,
        advertisement_update: schemas.AdvertisementUpdate,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    advertisement = crud.get_advertisement_by_id(db, advertisement_id)
    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advertisement not found"
        )

    # Пользователь может обновлять только свои объявления, админ - любые
    if current_user.group != "admin" and advertisement.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return crud.update_advertisement(db, advertisement_id, advertisement_update)


@router.delete("/{advertisement_id}")
def delete_advertisement(
        advertisement_id: uuid.UUID,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    advertisement = crud.get_advertisement_by_id(db, advertisement_id)
    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advertisement not found"
        )

    # Пользователь может удалять только свои объявления, админ - любые
    if current_user.group != "admin" and advertisement.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    crud.delete_advertisement(db, advertisement_id)
    return {"message": "Advertisement deleted successfully"}


@router.get("/", response_model=List[schemas.AdvertisementResponse])
def search_advertisements(
        title: Optional[str] = Query(None),
        description: Optional[str] = Query(None),
        min_price: Optional[float] = Query(None),
        max_price: Optional[float] = Query(None),
        current_user: Optional[models.User] = Depends(optional_auth),
        db: Session = Depends(get_db)
):
    return crud.get_advertisements(db, title, description, min_price, max_price)