import os
import boto3
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from api.exceptions import EntitieNotFound
from api.models.users import User
from botocore.exceptions import ClientError

from api.schemas.requests.users import CreateUserRequest


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, email: str, password: str):
        db_user = self.get_user_by_email(email)
        if not db_user:
            raise EntitieNotFound(detail="User not found")

        cognito_client = boto3.client(
            "cognito-idp",
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

        response = cognito_client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": str(db_user.cognito_id),
                "PASSWORD": password,
            },
            ClientId=os.getenv("COGNITO_CLIENT_ID"),
        )
        return response

    def create_user(self, user: CreateUserRequest):

        cognito_client = boto3.client(
            "cognito-idp",
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

        response = cognito_client.admin_create_user(
            UserPoolId=os.getenv("COGNITO_USER_POOL_ID"),
            Username=str(uuid.uuid4()),
            UserAttributes=[
                {"Name": "email", "Value": user.email},
                {"Name": "phone_number", "Value": user.phone},
            ],
            MessageAction="SUPPRESS",
        )

        cognito_id = response["User"]["Username"]

        cognito_client.admin_set_user_password(
            UserPoolId=os.getenv("COGNITO_USER_POOL_ID"),
            Username=cognito_id,
            Password=user.password,
            Permanent=True,
        )

        db_user = User(
            email=user.email,
            name=user.name,
            phone=user.phone,
            last_name=user.last_name,
            cognito_id=cognito_id,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_user(self, user_id: str):
        return self.db.query(User).filter(User.id == user_id).first()
