from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ignora os valores extras na .env
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    DATABASE_URL: str
    SECRETY_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
