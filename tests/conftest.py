import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app

#banco so para os testes, fica na memoria
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionTeste = sessionmaker(bind=engine)


def get_db_teste():
    db = SessionTeste()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = get_db_teste
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


#cria um usuario, faz login e devolve o header com o token
@pytest.fixture
def headers(client):
    client.post("/usuarios", json={"email": "teste@email.com", "senha": "123456"})
    resposta = client.post(
        "/login", data={"username": "teste@email.com", "password": "123456"}
    )
    token = resposta.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}