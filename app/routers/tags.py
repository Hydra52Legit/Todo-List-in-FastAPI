from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas
from .. auth import get_current_user
from .. database import get_db

router = APIRouter(prefix="/tags", tags=["tags"])

@router.post("/", response_mode=schemas.Tag, status_code=201)
def create_tag(
    tag: schemas.TagCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        db_tag = models.Tag(name=tag.name, color=tag.color, user_id=current_user)
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
    except IntegrityError:
        db.rollback(db_tag)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag with this name already exists"
        )
@router.get("/", response_model=list[schemas.Tag])
def list_tags(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Tag).filter(models.Tag.user_id == current_user.id).all()

@router.get("/{tag_id}", response_model=schemas.Tag)
def get_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    tag = db.query(models.Tag).filter(
        models.Tag.id == tag_id,
        models.Tag.user_id == current_user.id,
    ).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag
