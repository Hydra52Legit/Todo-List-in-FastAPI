import os
from dotenv import load_dotenv

load_dotenv()

# Просто берем URL из переменной окружения
# В .env должно быть ПОЛНОСТЬЮ: postgresql://user:password@db:5432/todo
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30