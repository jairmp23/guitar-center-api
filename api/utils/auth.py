from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer
import jwt
import requests
import os
from cachetools import cached, TTLCache


@cached(cache=TTLCache(maxsize=1, ttl=3600))
def get_jwks():
    region = os.getenv("AWS_REGION")
    user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
    url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
    response = requests.get(url)
    jwks = response.json()
    return {
        key["kid"]: jwt.algorithms.RSAAlgorithm.from_jwk(key) for key in jwks["keys"]
    }


def authenticate_user(token: str = Depends(HTTPBearer())):
    try:
        unverified_header = jwt.get_unverified_header(token.credentials)
        rsa_key = get_jwks()[unverified_header["kid"]]
        decoded_token = jwt.decode(
            token.credentials,
            key=rsa_key,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )

        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except (jwt.InvalidTokenError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid token")
