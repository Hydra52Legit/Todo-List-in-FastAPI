from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from .. import models, schemas, auth
from ..auth import get_db

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database unavailable")
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    try:
        hashed = auth.get_password_hash(user.password)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    db_user = models.User(username=user.username, hashed_password=hashed)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database unavailable")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    return db_user

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.User)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user