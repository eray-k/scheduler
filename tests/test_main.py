import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel, StaticPool

from main import app
from src.database.database import get_session
from src.database.models import User

user1 = User(username="John William", activities=[])
user2 = User(username="Matthew Patrick", activities=[])

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
    session.refresh(user1)
    session.refresh(user2)
    yield client
    
    app.dependency_overrides.clear()

def test_create_user(client: TestClient):
    response = client.post("/users/create", json={"username": "John William"})
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data["username"] == "John William"
    assert data["id"] is not None


def test_create_user_incomplete(client: TestClient):
    response = client.post("/users/create", json={})
    data = response.json()
    print(data)
    assert response.status_code == 422


def test_read_users(client: TestClient):
    response = client.get("/users")
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data[0]["username"] == user1.username
    assert data[0]["id"] is not None
    assert data[1]["username"] == user2.username
    assert data[1]["id"] is not None


def test_read_user(client: TestClient):
    response = client.get("/users/1")
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data[0]["username"] == user1.username
    assert data[0]["id"] is not None


def test_update_user(client: TestClient):
    response = client.patch("/users/1", json={"username": "Changed Name"})
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data["username"] == "Changed Name"
