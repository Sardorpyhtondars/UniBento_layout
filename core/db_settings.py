from typing import Optional, Union, Any
import psycopg2
from psycopg2.extras import DictCursor,DictRow
from core.config import DB_CONFIG

class DatabaseManager:
    """
    Database manager class to execute all queries
    """
    def __init__(self):
        self.connection = Optional[psycopg2.extensions.connection]
        self.cursor = Optional[psycopg2.extensions.cursor]

    def __enter__(self):
        self.connection = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor(cursor_factory=DictCursor)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.connection.rollback()
        else:
            self.connection.commit()

        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute(self, query: str, params: Union[tuple, dict, None] = None):
        self.cursor.execute(query, params)

    def fetchone(self, query: str, params: Union[tuple, dict, None] = None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetchall(self, query: str, params: Union[tuple, dict, None] = None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

def execute_query(
        query: str,
        params: Union[tuple, dict, None] = None,
        fetch: Union[str, None] = None,
)-> DictRow | None |list[tuple[Any, ...]]:
    try:
        with DatabaseManager() as db:
            if fetch =="one":
                return db.fetchone(query, params)
            elif fetch =="all":
                return db.fetchall(query, params)
            else:
                db.execute(query, params)
                return None
    except psycopg2.Error as e:
        print(e)
        return None