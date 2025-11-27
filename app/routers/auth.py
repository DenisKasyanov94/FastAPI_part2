from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app import crud, auth, schemas

router = APIRouter(prefix="/login", tags=["authentication"])

@router.post("/", response_model=schemas.TokenResponse)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, login_data.username)
    if not user or not auth.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = auth.create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(hours=48)
    )

    return {"access_token": access_token, "token_type": "bearer"}