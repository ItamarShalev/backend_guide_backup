from httpx import Client


def get_auth_token(client: Client, username: str = "user", password: str = "pw") -> str:
    client.post("/auth/register", json={"username": username, "password": password})
    resp = client.post("/auth/login", data={"username": username, "password": password})
    return resp.json()["access_token"]


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_create_and_get_todo(client: Client):
    token = get_auth_token(client)
    # Create todo
    resp = client.post("/todos/", headers=auth_header(token), json={"title": "t1", "description": "desc"})
    assert resp.status_code == 201
    todo = resp.json()
    assert todo["title"] == "t1"
    todo_id = todo["id"]

    # Get by id
    resp = client.get(f"/todos/{todo_id}", headers=auth_header(token))
    assert resp.status_code == 200
    assert resp.json()["id"] == todo_id


def test_list_todos(client: Client):
    token = get_auth_token(client, "another", "ppp")
    client.post("/todos/", headers=auth_header(token), json={"title": "A", "description": ""})
    client.post("/todos/", headers=auth_header(token), json={"title": "B", "description": ""})
    resp = client.get("/todos/", headers=auth_header(token))
    todos = resp.json()
    assert len(todos) >= 2

def test_update_and_delete_todo(client: Client):
    token = get_auth_token(client, "updater", "qqq")
    # Create
    resp = client.post("/todos/", headers=auth_header(token), json={"title": "to be updated", "description": ""})
    todo_id = resp.json()["id"]

    # Update
    resp = client.put(
        f"/todos/{todo_id}",
        headers=auth_header(token),
        json={"title": "updated!", "description": "desc", "completed": True},
    )
    assert resp.status_code == 200
    assert resp.json()["completed"]

    # Delete
    resp = client.delete(f"/todos/{todo_id}", headers=auth_header(token))
    assert resp.status_code == 200

    # Confirm gone
    resp = client.get(f"/todos/{todo_id}", headers=auth_header(token))
    assert resp.status_code == 404


def test_todo_attachment(client: Client):
    token = get_auth_token(client)
    # Create todo
    resp = client.post("/todos/", headers=auth_header(token), json={"title": "attach", "description": ""})
    todo_id = resp.json()["id"]
    # Attach file
    files = {"file": ("test.txt", b"12345", "text/plain")}
    resp = client.post(f"/todos/{todo_id}/attachment", headers=auth_header(token), files=files)
    assert resp.status_code == 200
    assert resp.json()["filename"] == "test.txt"


def test_filter_completed(client: Client):
    token = get_auth_token(client, "filterer", "yyy")
    # Create todos
    client.post("/todos/", headers=auth_header(token), json={"title": "a", "description": ""})
    client.post("/todos/", headers=auth_header(token), json={"title": "b", "description": ""})
    # Mark one completed
    resp = client.get("/todos/", headers=auth_header(token))
    tid = resp.json()[0]["id"]
    client.put(f"/todos/{tid}", headers=auth_header(token), json={"title": "a", "description": "", "completed": True})
    # Filter completed
    resp = client.get("/todos/?completed=true", headers=auth_header(token))
    for todo in resp.json():
        assert todo["completed"] is True


def test_todo_unauthorized(client: Client):
    resp = client.get("/todos/")
    assert resp.status_code == 401
    resp = client.post("/todos/", json={"title": "t", "description": ""})
    assert resp.status_code == 401
