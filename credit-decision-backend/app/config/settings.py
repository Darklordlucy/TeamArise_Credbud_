from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_ANON_KEY: str
    
    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_VERSION: str = "v1"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173"
    
    # ML Model
    ML_MODEL_PATH: str = "./app/ml/models/credit_model.pkl"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760
    ALLOWED_EXTENSIONS: str = "csv,xlsx,xls"
    
    # Thresholds (percentage of income)
    TRANSPORT_THRESHOLD: int = 15
    EDUCATION_THRESHOLD: int = 10
    MEDICAL_THRESHOLD: int = 8
    FOOD_SHOPPING_THRESHOLD: int = 25
    GROCERIES_THRESHOLD: int = 15
    EMI_THRESHOLD: int = 35
    ENTERTAINMENT_THRESHOLD: int = 10
    OTHERS_THRESHOLD: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
