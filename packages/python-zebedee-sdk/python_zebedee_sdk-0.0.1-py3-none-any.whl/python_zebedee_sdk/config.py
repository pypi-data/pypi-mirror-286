from typing import Optional
from pydantic_settings import BaseSettings


class Config(BaseSettings):

    BASE_URL: str = 'https://api.zebedee.io'
    API_KEY: Optional[str] = None