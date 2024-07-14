from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.config.config import *
from src.database.database import *
from src.database.models.user import User


app = FastAPI(title=APP_NAME, version=VERSION)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
    allow_credentials=True)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Redirect / -> Swagger-UI documentation
@app.get("/")
def main_function():
    """
    # Redirect
    to documentation (`/docs/`).
    """
    return RedirectResponse(url="/docs/")


@app.get("/dummy")
def dummy(session: Session = Depends(get_session)):
    setup_database(session)
    return {"status": "success"}

@app.post("/users/create", response_model=UserPublic)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    db_hero = User.model_validate(user)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.get("/users/{user_id}", response_model=UserPublicWithActivities)
def read_user_by_id(user_id: int, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    return db_user
