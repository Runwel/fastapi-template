from fastapi import APIRouter
from app.email.views import router

API_STR = "/email"

email_router = APIRouter(prefix=API_STR)
email_router.include_router(router)