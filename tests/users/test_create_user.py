import uuid
from unittest.mock import MagicMock


def test_create_user(client, monkeypatch):

    def mock_admin_create_user(*args, **kwargs):
        return {"User": {"Username": uuid.uuid4()}}

    def mock_admin_set_user_password(*args, **kwargs):
        pass

    monkeypatch.setattr(
        "boto3.client",
        lambda *args, **kwargs: MagicMock(
            admin_create_user=mock_admin_create_user,
            admin_set_user_password=mock_admin_set_user_password,
        ),
    )

    user_data = {
        "email": "john@example.com",
        "password": "secret",
        "name": "John",
        "last_name": "Doe",
        "phone": "+52555555555",
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 201


def test_create_user_exists(client, user1, monkeypatch):

    def mock_admin_create_user(*args, **kwargs):
        return {"User": {"Username": uuid.uuid4()}}

    def mock_admin_set_user_password(*args, **kwargs):
        pass

    monkeypatch.setattr(
        "boto3.client",
        lambda *args, **kwargs: MagicMock(
            admin_create_user=mock_admin_create_user,
            admin_set_user_password=mock_admin_set_user_password,
        ),
    )

    user_data = {
        "email": user1.email,
        "password": "secret",
        "name": "John",
        "last_name": "Doe",
        "phone": "+52555555555",
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 400
