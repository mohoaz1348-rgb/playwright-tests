from pathlib import Path

# from pydantic import AnyUrl
from pydantic import field_validator, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

RESULTS = "./results"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="."
    )
    app_url: str = "https://www.google.com/"

    @field_validator("app_url")
    @classmethod
    def check_url(cls, v: str) -> str:
        # Пытаемся превратить строку в HttpUrl.
        # Если адрес кривой, Pydantic выкинет ошибку.
        return str(HttpUrl(v))

    headless: bool = False
    expect_timeout: int = 30000
    videos_dir: Path = Path(RESULTS + "/videos")
    tracing_dir: Path = Path(RESULTS + "/tracing")
    allure_results: Path = Path(RESULTS + "/allure-results")
    downloads_dir: Path = Path(RESULTS + "/downloads")

    def model_post_init(self, __context):
        # Этот код сработает САМ при вызове Settings()
        self.videos_dir.mkdir(parents=True, exist_ok=True)
        self.tracing_dir.mkdir(parents=True, exist_ok=True)
        self.allure_results.mkdir(parents=True, exist_ok=True)
        # print("Отработал Settings::model_post_init")
