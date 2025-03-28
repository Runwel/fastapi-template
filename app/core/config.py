from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str  # ✅ Add missing fields
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str
    X_TOKEN: str
    PAYMONGO_SECRET_KEY: str

    class Config:
        env_file = ".env"  # Ensure the .env file is loaded
        env_file_encoding = "utf-8"  # Optional, ensures proper encoding

settings = Settings()

# Debugging: Print values to confirm they are loaded
print(f"Loaded SECRET_KEY: {settings.SECRET_KEY[:5]}***")  # Masking for security
print(f"Loaded ALGORITHM: {settings.ALGORITHM}")
print(f"Token Expiry (min): {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
