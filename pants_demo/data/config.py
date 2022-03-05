from pydantic import BaseSettings, PostgresDsn


class Config(BaseSettings):
    database_dsn: PostgresDsn

    class Config:
        env_prefix = "pants_demo_data_"
