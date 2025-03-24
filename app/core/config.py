from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"  # Load environment variables from .env
        extra = "allow"  # Allow extra fields

settings = Settings()  # Create a single instance of the settings
