from pydantic import BaseSettings


class SettingsTest(BaseSettings):
    # DB TEST
    DB_HOST: str = ''
    DB_PORT: str = ''
    DB_USER: str = ''
    DB_PASS: str = ''
    DB_NAME: str = ''

    # JWT

    class Config:
        env_file = '.env.test'
