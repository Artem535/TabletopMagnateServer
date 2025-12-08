"""
Application settings handled using Pydantic Settings management.

Pydantic is used both to read app settings from various sources, and to validate their
values.

https://docs.pydantic.dev/latest/usage/settings/
"""
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from tabletopmagnat.config.config import Config
from tabletopmagnat.config.langfuse import LangfuseSettings
from tabletopmagnat.config.models import Models
from tabletopmagnat.config.openai_config import OpenAIConfig

class APIInfo(BaseModel):
    title: str = "TabletopMagnatServer API"
    version: str = "0.0.1"


class App(BaseModel):
    show_error_details: bool = False


class Site(BaseModel):
    copyright: str = "Example"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")
    # to override info:
    # export app_info='{"title": "x", "version": "0.0.2"}'
    info: APIInfo = APIInfo()

    # to override app:
    # export app_app='{"show_error_details": True}'
    app: App = App()
    service: Config

def load_settings() -> Settings:
    return Settings()
