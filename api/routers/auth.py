from fastapi import APIRouter, Depends, HTTPException
from api.db_config import get_db
from api.exceptions import EntitieNotFound
from api.schemas.requests.users import CreateUserRequest
from api.schemas.resources.users import UserResource
from sqlalchemy.orm import Session

from api.services.users import AuthService

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)


@router.post("/", response_model=UserResource, status_code=201)
def create_user(
    user: CreateUserRequest, user_service: UserService = Depends(get_user_service)
):
    db_user = user_service.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(user)


@router.get("/{user_id}", response_model=UserResource, status_code=200)
def get_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    db_user = user_service.get_user(user_id)
    if not db_user:
        raise EntitieNotFound(detail="User Not Found")
    return db_user
