from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app import crud, schemas, models
from app.dependencies import get_current_user, require_admin, optional_auth

router = APIRouter(prefix="/user", tags=["users"])

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    return crud.create_user(db, user)

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(
        user_id: str,
        current_user: Optional[models.User] = Depends(optional_auth),
        db: Session = Depends(get_db)
):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.patch("/{user_id}", response_model=schemas.UserResponse)
def update_user(
        user_id: str,
        user_update: schemas.UserUpdate,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Пользователь может обновлять только себя, админ - любого
    if current_user.group != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    user = crud.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.delete("/{user_id}")
def delete_user(
        user_id: str,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Пользователь может удалять только себя, админ - любого
    if current_user.group != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    user = crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully"}