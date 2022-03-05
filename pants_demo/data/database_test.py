import socket
from dataclasses import dataclass
from time import sleep

import docker
import psycopg2
import pytest

from pants_demo.data.database import Database


def get_free_port():
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@dataclass
class PostgresInfo:
    name: str
    port: int
    user: str
    password: str
    database: str
    version: str = "14.2"

    @property
    def dsn(self):
        return f"postgresql://{self.user}:{self.password}@localhost:{self.port}/{self.database}"


@dataclass
class PostgreSQL:
    info: PostgresInfo


@pytest.fixture(scope="session")
def postgresql():
    client = docker.from_env()

    info = PostgresInfo(
        name="pants-demo-test-database",
        port=get_free_port(),
        user="test",
        password="test",
        database="test",
    )

    container = None

    try:
        container = client.containers.get(info.name)
    except docker.errors.NotFound:
        pass

    container.start()
    info.port = client.api.port(info.name, "5432")[0]["HostPort"]

    if container is None:
        container = client.containers.run(
            f"postgres:{info.version}",
            name=info.name,
            environment=dict(
                POSTGRES_USER=info.user, POSTGRES_PASSWORD=info.password, POSTGRES_DB=info.database
            ),
            ports={"5432/tcp": info.port},
            detach=True,
        )

    while True:
        try:
            psycopg2.connect(info.dsn).close()
            break
        except psycopg2.OperationalError:
            sleep(1)

    try:
        yield PostgreSQL(info=info)
    finally:
        container.stop()


@pytest.fixture
def test_database(postgresql):
    yield Database(database_dsn=postgresql.info.dsn)


def test_session(test_database):
    with test_database.session() as session:
        result = session.execute("SELECT 1").all()
        assert result[0][0] == 1
