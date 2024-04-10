from pydantic import BaseModel
import uuid


class UserResource(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    last_name: str
    cognito_id: uuid.UUID
    is_active: bool

    class Config:
        from_attributes = True

class UserTokenResource(BaseModel):
    access_token: str