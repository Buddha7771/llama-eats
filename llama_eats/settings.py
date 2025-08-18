import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV = os.environ.get("ENV", "dev")


class Settings(BaseSettings):
    """Configuration settings for the application."""

    model_config = SettingsConfigDict(
        env_file=[".env", f".env.{ENV}"],
        env_file_encoding="utf-8",
    )
    notion_token: str = Field(
        ...,
        description="Notion API token",
    )
    notion_key_db_id: str = Field(
        ...,
        description="Notion database ID that contains key paper metadata",
    )


settings = Settings()
