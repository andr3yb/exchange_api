from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"  # Можно указать путь к файлу с переменными окружения

settings = Settings()
