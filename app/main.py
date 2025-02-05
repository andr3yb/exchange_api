from fastapi import FastAPI
from routers import auth  # импортируем модуль с маршрутами авторизации

app = FastAPI()

# Подключаем маршруты авторизации под префиксом /auth (можно задать префикс, если нужно)
app.include_router(auth.router, prefix="/auth")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
