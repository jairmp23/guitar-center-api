from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt
import requests
import os
from sqlalchemy.orm import Session

from api.db_config import get_db
from api.models.users import User


class AuthManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.jwks = cls._instance.get_jwks()
        return cls._instance

    def get_jwks(self):
        region = os.getenv("AWS_REGION")
        user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
        url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
        response = requests.get(url)
        jwks = response.json()
        return {
            key["kid"]: jwt.algorithms.RSAAlgorithm.from_jwk(key)
            for key in jwks["keys"]
        }

    def __call__(
        self, token: str = Depends(HTTPBearer()), db: Session = Depends(get_db)
    ):
        try:
            unverified_header = jwt.get_unverified_header(token.credentials)
            rsa_key = self.jwks[unverified_header["kid"]]
            decoded_token = jwt.decode(
                token.credentials,
                key=rsa_key,
                algorithms=["RS256"],
                options={"verify_aud": False},
            )
            self.current_user = (
                db.query(User)
                .filter(User.cognito_id == decoded_token["username"])
                .first()
            )
            return (
                db.query(User)
                .filter(User.cognito_id == decoded_token["username"])
                .first()
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except (jwt.InvalidTokenError, KeyError):
            raise HTTPException(status_code=401, detail="Invalid token")


auth = AuthManager()
