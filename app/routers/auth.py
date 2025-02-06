from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasicCredentials

from schemas.user import UserCreate
from internal.security import security, hash_password, verify_password

# Фейковая база данных пользователей (словарь)
fake_users_db = {}

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    print(f"Попытка регистрации: {user.username}")
    if user.username in fake_users_db:
        print("Ошибка: пользователь уже существует")
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    hashed_password = hash_password(user.password)
    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": hashed_password
    }
    print("Пользователь успешно зарегистрирован")
    return {"msg": "Пользователь успешно зарегистрирован"}

@router.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    user = fake_users_db.get(credentials.username)
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")
    return {"msg": "Успешный вход"}
