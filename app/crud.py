from sqlalchemy.orm import Session
from typing import Optional, List
import uuid
from app import models, schemas, auth


# User CRUD
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: uuid.UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    # Проверяем уникальность username и email
    if get_user_by_username(db, user.username):
        raise ValueError("Username already exists")
    if get_user_by_email(db, user.email):
        raise ValueError("Email already exists")

    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        group=user.group.value if isinstance(user.group, schemas.UserGroup) else user.group
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: uuid.UUID, user_update: schemas.UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    update_data = user_update.dict(exclude_unset=True)

    # Проверяем уникальность при обновлении
    if "username" in update_data and update_data["username"] != db_user.username:
        if get_user_by_username(db, update_data["username"]):
            raise ValueError("Username already exists")

    if "email" in update_data and update_data["email"] != db_user.email:
        if get_user_by_email(db, update_data["email"]):
            raise ValueError("Email already exists")

    if "password" in update_data:
        update_data["hashed_password"] = auth.get_password_hash(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: uuid.UUID):
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# Advertisement CRUD
def create_advertisement(db: Session, advertisement: schemas.AdvertisementCreate, author_id: uuid.UUID):
    db_advertisement = models.Advertisement(
        **advertisement.dict(),
        author_id=author_id
    )
    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)
    return db_advertisement


def get_advertisement_by_id(db: Session, advertisement_id: uuid.UUID):
    return db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()


def get_advertisements(
        db: Session,
        title: Optional[str] = None,
        description: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
):
    query = db.query(models.Advertisement)
    if title:
        query = query.filter(models.Advertisement.title.ilike(f"%{title}%"))
    if description:
        query = query.filter(models.Advertisement.description.ilike(f"%{description}%"))
    if min_price is not None:
        query = query.filter(models.Advertisement.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Advertisement.price <= max_price)

    return query.order_by(models.Advertisement.created_at.desc()).all()


def update_advertisement(db: Session, advertisement_id: uuid.UUID, advertisement_update: schemas.AdvertisementUpdate):
    db_advertisement = get_advertisement_by_id(db, advertisement_id)
    if not db_advertisement:
        return None

    update_data = advertisement_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_advertisement, field, value)

    db.commit()
    db.refresh(db_advertisement)
    return db_advertisement


def delete_advertisement(db: Session, advertisement_id: uuid.UUID):
    db_advertisement = get_advertisement_by_id(db, advertisement_id)
    if db_advertisement:
        db.delete(db_advertisement)
        db.commit()
    return db_advertisement


def get_user_advertisements(db: Session, user_id: uuid.UUID):
    return db.query(models.Advertisement).filter(models.Advertisement.author_id == user_id).all()