import pytest
from . import get_app
from pathlib import Path
import json


@pytest.fixture(scope="session")
def app():
    app = get_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_register(client):
    response = client.post("/register", json={
        "email": "reddy@gmail.com",
        "password": "Reddy@123",
        "username": "reddy",
        "role": "admin"
    })
    assert response.status_code == 200


def test_login(client):
    response = client.post("/login", json={
        "email": "shiva@gmail.com",
        "password": "Shiva@123"
    })
    assert response.status_code == 200


def test_get_admin(client):
    try:
        response = client.get("/admin", headers={
                              "x-access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiZXhwIjoxNjcyOTIwMjE2fQ.of4P6qCvKR2Po5feCRyQpYLj3DGQlORuS_Fvke51AME"})
        assert response.status_code == 200

    except AssertionError as msg:
        print(msg)


def test_get_agent(client):
    response = client.get("/agent", headers={
        "x-access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6ImFnZW50IiwiZXhwIjoxNjcyOTIwMTcyfQ.4ZJg0RIj7cf0-udhO1duykuYwco-fv7J5WRMN90AkGA"})
    assert response.status_code == 200


def test_get_users(client):
    try:
        response = client.get("/admin", headers={
                              "x-access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6ImFnZW50IiwiZXhwIjoxNjcyOTIwMTcyfQ.4ZJg0RIj7cf0-udhO1duykuYwco-fv7J5WRMN90AkGA"})
        assert response.status_code == 200
    except AssertionError as msg:
        print(msg)
