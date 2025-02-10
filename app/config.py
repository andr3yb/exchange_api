from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str  # Ключ для подписи JWT
    algorithm: str  # Алгоритм подписи
    access_token_expire_minutes: int  # Время жизни токена в минутах

    class Config:
        env_file = ".env"  # Можно указать путь к файлу с переменными окружения

settings = Settings()
