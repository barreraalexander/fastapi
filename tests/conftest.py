from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
from app.main import app
from app.config import settings
from app.oauth2 import create_access_token
from app import models


from secrets import token_hex

SQLALCHEMY_DATABASE_URL_TEST = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_testing'
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

client = TestClient(app)

# function is the default
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # Base.metadata.drop_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

 
@pytest.fixture
def test_user(client):
    user_data = {
        "email" : f"tuna_@gmail.com",
        "password" : "password123"
    }
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({
        "user_id" : test_user.get('id'),
    })


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {
            "title" : "first title",
            "content" : "first content",
            "owner_id" : test_user.get('id')
        },
        {
            "title" : "second title",
            "content" : "second content",
            "owner_id" : test_user.get('id')
        },
        {
            "title" : "third title",
            "content" : "third content",
            "owner_id" : test_user.get('id')
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)

    # session.add_all([models.User(title="asdf")])


    session.commit()
    posts = session.query(models.Post).all()
    return posts
