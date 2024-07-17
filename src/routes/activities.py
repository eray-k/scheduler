from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select

from src.database.database import get_session
from src.database.models import *

router = APIRouter(prefix="/activities")


@router.get("/", response_model=list[ActivityPublic])
def read_activities(*, session: Session = Depends(get_session), limit: int = Query(default=100, le=500), ):
    activities = session.exec(select(Activity).limit(limit)).all()
    return activities


@router.post("/create/{owner_id}", response_model=ActivityPublic)
def create_activity(*, session: Session = Depends(get_session), activity: ActivityCreate, owner_id: int):
    if activity.beginning_datetime > activity.ending_datetime:
        raise HTTPException(status_code=400, detail="Starting timestamp can't be later than ending timestamp")

    db_user = session.get(User, owner_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    statement = select(Activity).limit(1).where(Activity.owner_id == owner_id,
                                                Activity.beginning_datetime < activity.ending_datetime,
                                                Activity.ending_datetime > activity.beginning_datetime)
    result = session.exec(statement).first()
    if result:
        print(result.model_dump())
        raise HTTPException(status_code=400, detail=f'User is not available, activity content: <{result.content}>')

    db_activity = Activity.model_validate({**activity.model_dump(exclude_unset=True), "owner_id": owner_id})
    session.add(db_activity)
    session.commit()
    session.refresh(db_activity)
    return db_activity


@router.get("/{activity_id}", response_model=ActivityPublicWithOwner)
def read_activity(activity_id: int, session: Session = Depends(get_session)):
    db_activity = session.get(Activity, activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity


@router.patch("/{activity_id}", response_model=ActivityPublic)
def update_activity(*, session: Session = Depends(get_session), activity_id: int, activity: ActivityUpdate):
    db_activity = session.get(Activity, activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity_data = activity.model_dump(exclude_unset=True)
    for key, value in activity_data.items():
        setattr(db_activity, key, value)
    session.add(db_activity)
    session.commit()
    session.refresh(db_activity)
    return db_activity


@router.delete("/{activity_id}")
def delete_activity(*, session: Session = Depends(get_session), activity_id: int):
    db_activity = session.get(Activity, activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    session.delete(db_activity)
    session.commit()
    return {"message": "Activity deleted"}
