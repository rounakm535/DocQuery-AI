from pydantic_settings import BaseSettings
import os
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Document QA System"
    API_V1_STR: str = "/api/v1"
    
    # Gemini config
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173", # Vite default
        "http://localhost:3000",
        "*" # In production, restrict this to your frontend URL
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
