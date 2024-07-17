from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from main import app
from src.database.database import get_session
from src.database.models import User, Activity, ActivityCreate

user1 = User(username="John William", activities=[])
user2 = User(username="Matthew Patrick", activities=[])
activity1 = Activity(content="Drinking milk", beginning_datetime=datetime(2020,1,1), ending_datetime=datetime(2020,1,2), owner_id=1)
activity2 = Activity(content="Playing tennis", beginning_datetime=datetime(2020,1,4), ending_datetime=datetime(2020,1,6), owner_id=1)
activity3 = Activity(content="Cooking", beginning_datetime=datetime(2020,1,1), ending_datetime=datetime(2020,1,2), owner_id=2)

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    session.add(user1)
    session.add(user2)

    session.commit()
    print(f"User1 ID: {user1.id}")
    print(f"User2 ID: {user2.id}")

    session.add(activity1)
    session.add(activity2)
    session.add(activity3)
    session.commit()

    yield client
    app.dependency_overrides.clear()

def test_create_activity(client: TestClient):
    response = client.post("/activities/create/1", json=activity1.dict(exclude={"owner_id"}))
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data["content"] == "Drinking milk"
    assert data["id"] is not None


def test_create_activity_incomplete(client: TestClient):
    response = client.post("/activities/create/1", json=activity1.dict(exclude={"owner_id", "content"}))
    data = response.json()
    print(data)
    assert response.status_code == 422


def test_read_activities(client: TestClient):
    response = client.get("/activities")
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data[0]["content"] == activity1.content
    assert data[0]["id"] is not None
    assert data[1]["content"] == activity2.content
    assert data[1]["id"] is not None


def test_read_activity(client: TestClient):
    response = client.get("/activities/1")
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data[0]["content"] == activity1.content
    assert data[0]["id"] is not None


def test_update_activity(client: TestClient):
    response = client.patch("/activities/2", json={"content": "Playing Golf"})
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data["content"] == "Playing Golf"
