from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# config.py fica em sapientrack/backend/app/core/.
# parents[0] = core, [1] = app, [2] = backend, [3] = sapientrack (raiz, onde está o .env)
_ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ROOT_ENV,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "SapienEx Track"
    database_url: str
    test_database_url: str | None = None


settings = Settings()
