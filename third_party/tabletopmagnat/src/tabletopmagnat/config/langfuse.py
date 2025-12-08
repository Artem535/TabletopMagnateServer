from pydantic_settings import BaseSettings


class LangfuseSettings(BaseSettings):
    public_key: str = ""
    secret_key: str = ""
    host: str = ""