from pydantic_settings import BaseSettings, SettingsConfigDict

from ..constants import BASE_DIR


class Config(BaseSettings):
    BOT_TOKEN: str
    PAYMASTER_TOKEN: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    model_config = SettingsConfigDict(env_file=BASE_DIR/'.env', env_file_encoding='utf-8', extra='ignore')


config = Config()
DB_URL = f'postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'
