from passlib.context import CryptContext
from fastapi.security import HTTPBasic

# Контекст для хеширования паролей (используем bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Схема базовой авторизации
security = HTTPBasic()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
