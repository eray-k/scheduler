import datetime

from sqlmodel import create_engine, SQLModel, Session, select

from .models import *

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def setup_database(session: Session):
    user1 = User(username="John Miller", activities=[])
    user2 = User(username="Matthew Manson", activities=[])
    t = datetime.datetime.now(datetime.UTC)
    activity1 = Activity(content="Drinking milk", beginning_datetime=t, ending_datetime=t + datetime.timedelta(hours=2),
                         owner=user1)
    session.add(user1)
    session.add(user2)
    session.add(activity1)
    session.commit()

def get_session():
    with Session(engine) as session:
        yield session

