from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app import models
import pytest


SQLALCHEMY_DATABASE_URL_TEST = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_testing'
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


client = TestClient(app)

@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# this way you can see how you got the arrow 
    # models.Base.metadata.create_all(bind=engine)
    # yield TestClient(app)
    # models.Base.metadata.drop_all(bind=engine)
    
    

def test_root(client):
    res = client.get("/")
    print (res.json().get('message'))
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={
        "email" : "broken95@gmail.com",
        "password" : "password123"
    })

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "broken95@gmail.com"
    assert res.status_code == 201

    

    # print (res.json())
    # assert res.json().get("email") == "broken305@gmail.com"
    # assert res.status_code == 201

# @app.get("/")
# def root():
#     return {"message" : "Hello World"}