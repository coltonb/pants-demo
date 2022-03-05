from dependency_injector import containers, providers

from pants_demo import data
from pants_demo.lambdas.demo_lambda.event_handler import EventHandler


class Container(containers.DeclarativeContainer):
    data = providers.Container(data.Container)
    event_handler = providers.Factory(EventHandler, database=data.database)
