from pydantic import BaseSettings
import os


class Setting(BaseSettings):
    DB_URL: str
    ACCESS_TOKEN_EXPIRED: int
    ALGHORITHM: str
    SECRET_KEY: str
    class Config:
        env_file = os.path.join(os.getcwd(),'.env')