from contextlib import contextmanager
from dataclasses import dataclass

import sqlalchemy
import sqlalchemy.orm


class Database:
    def __init__(self, database_dsn: str):
        self.engine = sqlalchemy.create_engine(database_dsn)
        self.session_factory = sqlalchemy.orm.scoped_session(
            sqlalchemy.orm.sessionmaker(self.engine)
        )

    @contextmanager
    def session(self):
        session = self.session_factory()
        session.begin()

        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
