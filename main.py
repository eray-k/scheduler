from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.config.config import *
from src.database.database import *
from src.database.models import *

from src.routes.users import router as users_router
from src.routes.activities import router as activities_router



app = FastAPI(title=APP_NAME, version=VERSION)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
    allow_credentials=True)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(users_router)
app.include_router(activities_router)

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
