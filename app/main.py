from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db, get_current_user
from sqlalchemy import text

from fastapi import FastAPI
from routers import auth, currency  # импортируем модуль с маршрутами авторизации

app = FastAPI()

# Подключаем маршруты авторизации под префиксом /auth (можно задать префикс, если нужно)
app.include_router(auth.router, prefix="/auth")
app.include_router(currency.router, prefix="/currency")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


@app.get("/test")
async def test_endpoint(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"result": result.scalar()}

@app.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Привет, {current_user}!"}