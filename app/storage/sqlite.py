import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from app.core.config.settings import settings


class CheckpointStorage:
    @staticmethod
    def get_checkpointer():
        db_path = settings.SQLITE_URL.replace("sqlite:///", "")
        conn = sqlite3.connect(
            db_path,
            check_same_thread=False
        )
        return SqliteSaver(conn)


checkpoint_storage = CheckpointStorage()

