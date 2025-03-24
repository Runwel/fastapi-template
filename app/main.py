import os
from fastapi import FastAPI, APIRouter
from fastapi_sqlalchemy import DBSessionMiddleware
from dotenv import load_dotenv

# Import role and user routes for authentication and RBAC
from app.CRUD.routes.role import router as role_router
from app.CRUD.routes.user import router as user_router
from app.email import router as email_router
from app.core.logger import init_logging

load_dotenv(".env")

root_router = APIRouter()

app = FastAPI(title="FastAPI Boiler Plate")

# Add database middleware
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

# Register routes
# app.include_router(email_router)
app.include_router(root_router)
app.include_router(role_router)
app.include_router(user_router)

init_logging()

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
