from dataclasses import dataclass

import sqlalchemy

from pants_demo.data import Database


@dataclass
class EventHandler:
    database: Database

    def handle_event(self, event):
        with self.database.session() as session:
            session.execute(sqlalchemy.insert("test").values(name=event["name"]))
