from httpx import Client


def test_root(client: Client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("status")
