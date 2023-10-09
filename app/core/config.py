from pydantic import BaseSettings


class Settings(BaseSettings):
    # App
    DEBUG: bool = False
    HOST: str = '0.0.0.0'
    PORT: int = 8000
    RELOAD: bool = False

    # DB
    CONN_DB: str = ''

    CONN_DB_TEST: str = ''

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRATION_TIME_MINUTES: int = 60

    class Config:
        env_file = '.env'
