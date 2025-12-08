"""
Application Configuration Module.

This module provides the main configuration class for the TabletopMagnat application.
It uses `pydantic_settings` to load configuration values from environment variables
and a `.env` file, allowing for structured and type-safe access to configuration data.

Key Features:
- Automatic loading of environment variables from `.env`.
- Support for nested configuration via `env_nested_delimiter`.
- Integration with service-specific configurations (e.g., OpenAI).

Classes:
    Config: Main configuration class that includes service-specific configurations.
"""
from pydantic import BaseModel, Field

from tabletopmagnat.config.langfuse import LangfuseSettings
from tabletopmagnat.config.models import Models
from tabletopmagnat.config.openai_config import OpenAIConfig


class Config(BaseModel):
    """
    Main application configuration class.

    Uses `pydantic_settings.BaseSettings` to automatically load settings from
    environment variables and the `.env` file.

    Attributes:
        model_config (SettingsConfigDict): Pydantic configuration specifying
            the `.env` file path, encoding, and nested parameter delimiter.
        openai (OpenAIConfig): Nested configuration for OpenAI services.
    """
    models: Models = Field(default_factory=Models)
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    langfuse: LangfuseSettings = Field(default_factory=LangfuseSettings)