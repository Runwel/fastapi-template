import os
from fastapi import FastAPI, APIRouter
from fastapi_sqlalchemy import DBSessionMiddleware
from dotenv import load_dotenv
from app.auth.routes.role import router as role_router
from app.auth.routes.user import router as user_router
from app.auth.routes.file import router as file_router 
from app.receipt_scanner.route import router as receipt_router
from app.auth.routes.admin import router as admin_router
from app.core.logger import init_logging
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(".env")

root_router = APIRouter()

app = FastAPI(title="FastAPI Boiler Plate")

# Add database middleware
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.1.3:8080"],  # OR replace with ["http://your-machine-ip:5173"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(root_router)

# User routes
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(role_router, prefix="/roles", tags=["Roles"])
app.include_router(user_router, prefix="/auth", tags=["Auth"])
app.include_router(file_router, prefix="/files", tags=["Files"])

# Payment route
app.include_router(receipt_router, prefix="/receipt", tags=["Receipt"])

init_logging()

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
