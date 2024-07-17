from http.client import HTTPException
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from src.database.database import get_session
from src.database.models import *

router = APIRouter(prefix="/users")


@router.get("/", response_model=list[UserPublic])
def read_users(*, session: Session = Depends(get_session), limit: int = Query(default=10, le=100, ge=3), ):
    users = session.exec(select(User).limit(limit)).all()
    return users


@router.post("/create", response_model=UserPublic)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/{user_id}", response_model=UserPublicWithActivities)
def read_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(*, session: Session = Depends(get_session), user_id: int, user: UserUpdate):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(*, session: Session = Depends(get_session), user_id: int):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(db_user)
    session.commit()
    return {"message": "User deleted"}


@router.get("/{user_id}/activities", response_model=list[ActivityPublic])
def get_activities_of_user(*, session: Session = Depends(get_session), user_id: int):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user.activities
