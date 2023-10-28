import sys
from datetime import datetime
from typing import List, Any

import psycopg2 as pg

from dao_base import DAOBase


def _select_schema(cursor, workspace_id: str) -> None:
    cursor.execute("""
        SET search_path TO %s
    """, (workspace_id,))


class DAOPostgreSQL(DAOBase):
    """An implementation of the DAO interface using PostgreSQL.

    For backend guys: Do NOT initialize any instance of this class manually.
                      Instead, use the get_DAO() function in __init__.py.

    Attributes:
        hostname: The hostname of the database.
        port: The port of the database.
        dbname: The name of the database.
        user: The username of the database.
        password: The password of the database.
    """

    hostname: str
    port: int
    dbname: str
    user: str
    password: str
    _connection: Any

    def __init__(self,
                 hostname: str = 'csc301-database.postgres.database.azure.com',
                 port: int = 5432,
                 dbname: str = 'team_spirit',
                 user: str = 'dev',
                 password: str = 'dev') -> None:
        self.hostname = hostname
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self._connection = self._connect()

    def create_workspace(self, workspace_id: str) -> bool:
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(f'CREATE SCHEMA IF NOT EXISTS {workspace_id};')
                _select_schema(cursor, workspace_id)

                # init tables
                init_sql = open('init.sql', 'r').read().replace(
                    'test_schema', workspace_id)
                cursor.execute(init_sql)
                conn.commit()
                return True
        except Exception as e:
            print(e, file=sys.stderr)
            return False

    def add_user(self, workspace_id: str, slack_id: str, name: str) -> bool:
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                _select_schema(cursor, workspace_id)

                cursor.execute("""
                    INSERT INTO users (slack_id, name) VALUES (%s, %s);
                """, (slack_id, name))

                conn.commit()
                return True
        except Exception as e:
            print(e, file=sys.stderr)
            return False

    def delete_user(self, workspace_id: str, slack_id: str) -> bool:
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:

                _select_schema(cursor, workspace_id)

                cursor.execute("""
                    DELETE FROM users WHERE slack_id = %s;
                """, (slack_id,))

                conn.commit()
                return True
        except Exception as e:
            print(e, file=sys.stderr)
            return False

    def add_channel(self, workspace_id: str, channel_id: str,
                    name: str) -> bool:
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:

                _select_schema(cursor, workspace_id)

                cursor.execute("""
                    INSERT INTO channels (id, name) VALUES (%s, %s);
                """, (channel_id, name))

                conn.commit()
                return True
        except Exception as e:
            print(e, file=sys.stderr)
            return False

    def delete_channel(self, workspace_id: str, channel_id: str) -> bool:
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:

                _select_schema(cursor, workspace_id)

                cursor.execute("""
                    DELETE FROM channels WHERE id = %s;
                """, (channel_id,))

                conn.commit()
                return True
        except Exception as e:
            print(e, file=sys.stderr)
            return False

    def add_message(self, workspace_id: str, channel_id: str, msg_id: str,
                    time: datetime, from_slack_id: str, to_slack_id: str,
                    text: str, kudos_value: List[str] = None) -> bool:
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:

                _select_schema(cursor, workspace_id)

                cursor.execute("""
                    INSERT INTO messages (id, channel_id, time, from_slack_id,
                                          to_slack_id, text)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (msg_id, channel_id, time, from_slack_id,
                      to_slack_id, text))

                if kudos_value is not None:
                    for value in kudos_value:
                        # get the kudos value id
                        cursor.execute("""
                            SELECT id FROM corp_values WHERE corp_value = %s;
                        """, (value,))
                        kudos_value_id = cursor.fetchone()[0]
                        cursor.execute("""
                            INSERT INTO kudos (message_id, corp_value_id)
                            VALUES (%s, %s);
                        """, (msg_id, kudos_value_id))

                conn.commit()
                return True
        except Exception as e:
            print(e, file=sys.stderr)
            return False

    def add_corp_values(self, workspace_id: str, values: List[str]) -> bool:
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:

                _select_schema(cursor, workspace_id)

                # get the current values, we only insert values that are not
                # already in the table
                curr_values = self.get_corp_values(workspace_id)

                for value in values:
                    # check if the value is already in the table
                    if value not in curr_values:
                        cursor.execute("""
                            INSERT INTO corp_values (corp_value) VALUES (%s);
                        """, (value,))
                conn.commit()
                return True
        except Exception as e:
            print(e, file=sys.stderr)
            return False

    def delete_corp_values(self, workspace_id: str,
                           values: List[str], ) -> bool:
        try:
            # get connection
            conn = self.get_connection()
            with conn.cursor() as cursor:

                _select_schema(cursor, workspace_id)

                for value in values:
                    cursor.execute("""
                        DELETE FROM corp_values WHERE corp_value = %s;
                    """, (value,))
                conn.commit()
                return True
        except Exception as e:
            print(e, file=sys.stderr)
            return False

    def get_corp_values(self, workspace_id: str) -> List[str]:
        try:
            # get connection
            conn = self.get_connection()
            with conn.cursor() as cursor:

                _select_schema(cursor, workspace_id)

                # get all values
                cursor.execute("""
                    SELECT corp_value FROM corp_values;
                """)
                values = cursor.fetchall()
                return values
        except Exception as e:
            print(e, file=sys.stderr)
            return []

    def _connect(self):
        return pg.connect(host=self.hostname, port=self.port,
                          dbname=self.dbname, user=self.user,
                          password=self.password)

    def get_connection(self):
        if self._connection.closed:
            self._connection = self._connect()
        return self._connection
