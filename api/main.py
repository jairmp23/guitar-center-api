import os
from fastapi import FastAPI
from dotenv import load_dotenv

from .routers import health, users

## ENV
load_dotenv()

## FASTAPI INIT
app = FastAPI()

## REGISTER ROUTES
app.include_router(health.router, prefix="/health")
app.include_router(users.router, prefix="/users")
