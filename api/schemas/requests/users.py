from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    name: str
    last_name: str
    email: str
    phone: str
    password: str
    is_active: bool = True

class UserLoginRequest(BaseModel):
    email: str
    password: str