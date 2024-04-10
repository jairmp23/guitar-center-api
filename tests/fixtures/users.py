import pytest
import uuid
from api.models.users import User


@pytest.fixture
def user1(db):
    user = User(
        email="user1@example.com",
        name="John",
        last_name="Doe",
        phone="+123456789",
        cognito_id=uuid.uuid4(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.close()
