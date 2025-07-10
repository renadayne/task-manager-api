import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

class Settings:
    # Cấu hình JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Cấu hình database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./task_manager.db")

# Tạo instance settings
settings = Settings() 