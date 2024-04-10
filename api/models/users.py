from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from api.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    name = Column(String)
    last_name = Column(String)
    cognito_id = Column(UUID(as_uuid=True), unique=True, index=True)
    is_active = Column(Boolean, default=True)
