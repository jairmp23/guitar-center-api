from unittest.mock import MagicMock


def test_user_login(client, user1, monkeypatch):

    def mock_initiate_auth(*args, **kwargs):
        return {"AuthenticationResult": {"AccessToken": "asdjlkdjaioijaij"}}

    monkeypatch.setattr(
        "boto3.client",
        lambda *args, **kwargs: MagicMock(
            initiate_auth=mock_initiate_auth,
        ),
    )

    user_data = {
        "email": user1.email,
        "password": "secret",
    }

    response = client.post("/users/login", json=user_data)
    data = response.json()

    assert response.status_code == 200
    assert data.get("access_token") != None


def test_user_login_no_token(client, user1, monkeypatch):

    def mock_initiate_auth(*args, **kwargs):
        return {}

    monkeypatch.setattr(
        "boto3.client",
        lambda *args, **kwargs: MagicMock(
            initiate_auth=mock_initiate_auth,
        ),
    )

    user_data = {
        "email": user1.email,
        "password": "secret",
    }

    response = client.post("/users/login", json=user_data)
    data = response.json()

    assert response.status_code == 401
    assert data["detail"] == "Authentication failed"


def test_user_login_no_user(client, user1, monkeypatch):

    def mock_initiate_auth(*args, **kwargs):
        return {}

    monkeypatch.setattr(
        "boto3.client",
        lambda *args, **kwargs: MagicMock(
            initiate_auth=mock_initiate_auth,
        ),
    )

    user_data = {
        "email": "test@example.com",
        "password": "secret",
    }

    response = client.post("/users/login", json=user_data)
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "User not found"
