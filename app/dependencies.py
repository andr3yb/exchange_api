from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from internal.jwt import decode_access_token

from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Получение текущего пользователя из токена"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    return payload["sub"]