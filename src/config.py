
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    """
    Настройки подключения к PostgreSQL
    """
    username: str
    password: str
    host: str
    port: int
    name: str
    echo: bool

    @property
    def url(self) -> str:
        """
        Формирует URL для подключения к БД
        """
        return (
            f"postgresql+asyncpg://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class ApiSettings(BaseModel):
    """
    Настройка API
    """
    prefix: str = "/v1"


class ParseSettings(BaseModel):
    """
    Настройка Парсера
    """
    prefix: str = "/parser"
    url: str = "https://hh.ru/search/vacancy"
    header: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }


class Settings(BaseSettings):
    """
    Главные настройки приложения
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__"
    )

    db: DatabaseSettings
    api: ApiSettings = ApiSettings()
    parser: ParseSettings = ParseSettings()


settings = Settings()