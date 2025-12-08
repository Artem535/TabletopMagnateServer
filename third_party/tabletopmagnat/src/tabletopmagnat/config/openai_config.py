"""
OpenAI Configuration Module.

This module defines the configuration class for OpenAI services used in the TabletopMagnat application.
It provides a structured way to manage and access OpenAI-specific settings such as API key, base URL,
and model name using Pydantic's `BaseSettings`.

Classes:
    OpenAIConfig: Represents the configuration for OpenAI services.
"""

from pydantic_settings import BaseSettings  # type: ignore 


class OpenAIConfig(BaseSettings):
    """
    Configuration class for OpenAI services.

    Attributes:
        api_key (str): The API key used to authenticate with OpenAI services.
        base_url (str): The base URL of the OpenAI API endpoint.
    """

    api_key: str = ""
    base_url: str = ""
