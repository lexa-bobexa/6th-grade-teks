from pydantic import BaseModel


class Settings(BaseModel):
    environment: str = "dev"


def get_settings() -> Settings:
    return Settings()
