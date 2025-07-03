from httpx import Client


def test_register(client: Client):
    resp = client.post("/auth/register", json={"username": "alice", "password": "secret"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "alice"
    assert "id" in data


def test_register_duplicate(client: Client):
    client.post("/auth/register", json={"username": "bob", "password": "secret"})
    resp = client.post("/auth/register", json={"username": "bob", "password": "other"})
    assert resp.status_code == 400


def test_login_success(client: Client):
    client.post("/auth/register", json={"username": "eve", "password": "pw"})
    resp = client.post("/auth/login", data={"username": "eve", "password": "pw"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: Client):
    client.post("/auth/register", json={"username": "john", "password": "pass"})
    resp = client.post("/auth/login", data={"username": "john", "password": "wrong"})
    assert resp.status_code == 400


def test_login_nonexistent_user(client: Client):
    resp = client.post("/auth/login", data={"username": "idontexist", "password": "xxx"})
    assert resp.status_code == 400
