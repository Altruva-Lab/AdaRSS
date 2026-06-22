import os

# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./api/database/adarss.db")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://ennas:Akiim@localhost/adarss")
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 100))  # requests per minute
# MODEL_PATH = os.getenv("MODEL_PATH", "./api/model/adarss-baseline.pkl")
MODEL_PATH = os.getenv("MODEL_PATH", "./api/model/adarss-distilbert")
VECTORIZER_PATH = os.getenv("VECTORIZER_PATH", "./api/model/adarss-vectorizer.pkl")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
