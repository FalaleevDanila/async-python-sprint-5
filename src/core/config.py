import os
from logging import config as logging_config
from pydantic import BaseSettings, PostgresDsn

from src.core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

BLACK_LIST: list[str] = []

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_FILES_FOLDER="./data"


class AppSettings(BaseSettings):
    app_title: str = "LibraryApp"
    HOST: str = '0.0.0.0'
    PORT: int = 9000
    database_dsn: PostgresDsn = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'

    class Config:
        env_file = '../.env'


app_settings = AppSettings()
