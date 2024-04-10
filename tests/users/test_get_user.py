import uuid


def test_get_user(client, user1, monkeypatch):
    response = client.get(f"/users/{user1.id}")

    assert response.status_code == 200


def test_get_user_not_found(client, monkeypatch):
    response = client.get(f"/users/{uuid.uuid4()}")

    assert response.status_code == 404
