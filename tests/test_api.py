import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from database import Base, get_db
from main import app

TEST_DB_URL = "sqlite:///./test_vulntracker.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def register_and_login(username="alice", email="alice@example.com", password="password123"):
    client.post("/auth/register", json={"username": username, "email": email, "password": password})
    resp = client.post("/auth/login", json={"username": username, "password": password})
    return resp.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_register_user():
    resp = client.post("/auth/register", json={
        "username": "bob",
        "email": "bob@example.com",
        "password": "secret",
    })
    assert resp.status_code == 201
    assert resp.json()["username"] == "bob"


def test_login_success():
    client.post("/auth/register", json={"username": "alice", "email": "alice@example.com", "password": "pw"})
    resp = client.post("/auth/login", json={"username": "alice", "password": "pw"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_create_scan():
    token = register_and_login()
    resp = client.post(
        "/scans",
        json={
            "title": "Reflected XSS in search",
            "description": "User input is echoed without sanitisation",
            "severity": "high",
            "affected_component": "GET /search",
        },
        headers=auth_headers(token),
    )
    assert resp.status_code == 201
    assert resp.json()["title"] == "Reflected XSS in search"


def test_search_shares_and_password_protected_link():
    token = register_and_login()
    scan_id = client.post(
        "/scans",
        json={
            "title": "Privilege escalation",
            "severity": "critical",
            "affected_component": "RBAC",
        },
        headers=auth_headers(token),
    ).json()["id"]

    share = client.post(
        f"/scans/{scan_id}/share",
        json={"password": "secret"},
        headers=auth_headers(token),
    )
    assert share.status_code == 200
    share_url = share.json()["share_url"]
    public_token = share_url.rsplit("/", 1)[-1]

    resp = client.get(f"/share/{public_token}")
    assert resp.status_code == 401

    protected_resp = client.get(f"/share/{public_token}?password=secret")
    assert protected_resp.status_code == 200
    assert protected_resp.json()["title"] == "Privilege escalation"
