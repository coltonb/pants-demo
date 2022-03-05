from dependency_injector import containers, providers

from pants_demo.data.config import Config
from pants_demo.data.database import Database


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[Config()])
    database = providers.Singleton(Database, database_dsn=config.database_dsn)
