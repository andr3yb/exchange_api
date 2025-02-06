from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from schemas.user import UserCreate
from internal.security import security, hash_password, verify_password
from dependencies import get_db  # Функция для получения сессии БД
from models.user import User  # Импорт модели пользователя


router = APIRouter()

@router.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security), db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.username == credentials.username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")

    return {"msg": "Успешный вход"}

@router.post("/register")
async def add_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.username == user.username)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    new_user = User(username=user.username, hashed_password=hash_password(user.password))
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return {"msg": "Пользователь добавлен в базу данных", "id": new_user.id}
