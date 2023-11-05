import sys
from datetime import datetime
from typing import List, Any

import psycopg2 as pg

from dao_base import DAOBase

import logging
logger = logging.getLogger(__name__)


def _select_schema(cursor, workspace_id: str) -> None:
    logger.info(f"Selecting schema for workspace: {workspace_id}")
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
                 hostname: str = 'teamspirit.postgres.database.azure.com',
                 port: int = 5432,
                 dbname: str = 'team_spirit',
                 user: str = 'kudosadmin',
                 password: str = 'Highsalary001') -> None:
        logger.info("Connecting to PostgreSQL database...")
        self.hostname = hostname
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self._connection = self._connect()
        logger.info("Connected to PostgreSQL database!")

    def create_workspace(self, workspace_id: str) -> bool:
        try:
            logger.info(f"Creating workspace for workspace with id: {workspace_id}")
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
            logger.error(f"Failed to create workspace with id: {workspace_id}")
            return False

    def add_user(self, workspace_id: str, slack_id: str, name: str) -> bool:
        try:
            logger.info(f"Adding user with slack_id and name '({slack_id}, {name})' "
                        f"for workspace with id: {workspace_id}")
            conn = self.get_connection()
            with conn.cursor() as cursor:
                _select_schema(cursor, workspace_id)

                cursor.execute("""
                    INSERT INTO users (slack_id, name) VALUES (%s, %s);
                """, (slack_id, name))

                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to add user '({slack_id}, {name})' "
                         f"in workspace with id: {workspace_id}")
            print(e, file=sys.stderr)
            return False

    def delete_user(self, workspace_id: str, slack_id: str) -> bool:
        try:
            logger.info(f"Deleting user with slack_id '{slack_id}' "
                        f"in workspace with id: {workspace_id}")
            conn = self.get_connection()
            with conn.cursor() as cursor:

                _select_schema(cursor, workspace_id)

                cursor.execute("""
                    DELETE FROM users WHERE slack_id = %s;
                """, (slack_id,))

                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to delete user with slack_id '{slack_id} "
                         f"in workspace with id: {workspace_id}")
            print(e, file=sys.stderr)
            return False

    def add_channel(self, workspace_id: str, channel_id: str,
                    name: str) -> bool:
        try:
            logger.info(f"Adding channel with channel_id and name '({channel_id}, {name})' "
                        f"to workspace with id: {workspace_id}")
            conn = self.get_connection()
            with conn.cursor() as cursor:

                _select_schema(cursor, workspace_id)

                cursor.execute("""
                    INSERT INTO channels (id, name) VALUES (%s, %s);
                """, (channel_id, name))

                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to add channel '({channel_id}, {name})' "
                         f"to workspace with id: {workspace_id}")
            print(e, file=sys.stderr)
            return False

    def delete_channel(self, workspace_id: str, channel_id: str) -> bool:
        try:
            logger.info(f"Deleting channel with channel_id '{channel_id}' "
                        f"from workspace with id: {workspace_id}")
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
            logger.error(f"Failed to delete channel with id '{channel_id}' "
                         f"from workspace with id: {workspace_id}")
            return False

    def add_message(self, workspace_id: str, channel_id: str, msg_id: str,
                    time: datetime, from_slack_id: str, to_slack_id: str,
                    text: str, kudos_value: List[str] = None) -> bool:
        try:
            logger.info(f"Adding message with msg_id '{msg_id}' "
                        f"from user with slack_id '{from_slack_id}' "
                        f"to user with slack_id '{to_slack_id}' "
                        f"in workspace with id: {workspace_id}'")
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
            logger.error(f"Failed to add message in workspace with id '{workspace_id}'")
            return False

    def add_corp_values(self, workspace_id: str, values: List[str]) -> bool:
        try:
            logger.info(f"Adding corp values '{values}' to workspace with id: {workspace_id}")
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
            logger.error(f"Failed to add values '{values}' to workspace with id '{workspace_id}'")
            print(e, file=sys.stderr)
            return False

    def delete_corp_values(self, workspace_id: str, values: List[str]) -> bool:
        try:
            logger.info(f"Deleting corp values '{values}' from workspace with id: {workspace_id}")
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
            logger.error(f"Failed to remove values '{values}' to workspace with id '{workspace_id}'")
            print(e, file=sys.stderr)
            return False

    def get_corp_values(self, workspace_id: str) -> List[str]:
        try:
            logger.info(f"Getting corp values from workspace with id: {workspace_id}")
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
            logger.error(f"Failed to get corp values from workspace with id '{workspace_id}'")
            print(e, file=sys.stderr)
            return []

    # TODO: Add get_user_kudos() function here, takes in "user_id", fetch all kudos for that user
    # Returns a dict with the following keys:
    # - 'total_kudos': int
    # - 'corp_values': dict[str, int]
    # Maps from a corp_value to the count that this user has received under that value

    def _connect(self):
        return pg.connect(host=self.hostname, port=self.port,
                          dbname=self.dbname, user=self.user,
                          password=self.password)

    def get_connection(self):
        logger.info("Getting connection to PostgreSQL database...")
        if self._connection.closed:
            logger.info("Connection closed, reconnecting...")
            self._connection = self._connect()
        return self._connection
