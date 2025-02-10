from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasicCredentials, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from schemas.user import UserCreate
from internal.security import security, hash_password, verify_password
from internal.jwt import create_access_token
from dependencies import get_db  # Функция для получения сессии БД
from models.user import User  # Импорт модели пользователя


router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Регистрация пользователя"""
    existing_user = await db.execute(
        select(User).where(User.username == user.username)
    )
    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    new_user = User(username=user.username, hashed_password=hash_password(user.password))
    db.add(new_user)
    await db.commit()
    return {"msg": "Пользователь зарегистрирован"}

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    """Авторизация пользователя"""
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверные учетные данные")
    
    access_token = create_access_token({"sub": user.username}, expires_delta=timedelta(minutes=30))
    
    return {"access_token": access_token, "token_type": "bearer"}
