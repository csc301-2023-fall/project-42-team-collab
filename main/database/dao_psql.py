import sys
from datetime import datetime
from typing import List, Any, Tuple

import psycopg2 as pg

from database.dao_base import DAOBase

import pathlib
import os

import config

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
                 hostname: str = config.DB_HOSTNAME,
                 port: int = config.DB_PORT,
                 dbname: str = config.DB_DBNAME,
                 user: str = config.DB_USER,
                 password: str = config.DB_PASSWORD) -> None:
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
                # cursor.execute(f'CREATE SCHEMA IF NOT EXISTS {workspace_id};')
                # _select_schema(cursor, workspace_id)

                # init tables
                init_sql = open(os.path.join(pathlib.Path(__file__).parent.resolve(), 'init.sql'), 'r').read().replace(
                    'test_schema', workspace_id)
                cursor.execute(init_sql)

                conn.commit()

                default_values = [
                    "Good Teamwork",
                    "Customer First",
                    "Innovation",
                    "Leadership",
                    "Continuous Learning",
                    "Problem Solving",
                    "Integrity",
                    "Collaboration",
                    "Passion",
                    "Flexibility",
                    "Accountability"
                ]

                self.add_corp_values(workspace_id, default_values)

                return True
        except Exception as e:
            print(e, file=sys.stderr)
            logger.error(f"Failed to create workspace with id: {workspace_id}")
            self.get_connection().rollback()
            return False

    def add_user(self, workspace_id: str, slack_id: str, name: str) -> bool:
        try:
            logger.info(f"Adding user with slack_id and name '({slack_id}, {name})' "
                        f"for workspace with id: {workspace_id}")
            conn = self.get_connection()
            with conn.cursor() as cursor:
                # TODO: Temporary work around
                t = f"SELECT slack_id FROM {workspace_id}.users WHERE slack_id = '{slack_id}'"
                cursor.execute(t)

                # If the user already exists
                if cursor.fetchone() is not None:
                    return False

                # _select_schema(cursor, workspace_id)

                t = f"INSERT INTO {workspace_id}.users (slack_id, name) VALUES ('{slack_id}', '{name}')"
                cursor.execute(t)

                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to add user '({slack_id}, {name})' "
                         f"in workspace with id: {workspace_id}")
            print(e, file=sys.stderr)
            self.get_connection().rollback()
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
                # TODO: Temporary work around
                t = f"SELECT id FROM {workspace_id}.channels WHERE id = '{channel_id}'"
                cursor.execute(t)

                # If the user already exists
                if cursor.fetchone() is not None:
                    return False

                t = f"INSERT INTO {workspace_id}.channels (id, name) VALUES ('{channel_id}', '{name}')"
                cursor.execute(t)

                # _select_schema(cursor, workspace_id)

                # cursor.execute("""
                #     INSERT INTO channels (id, name) VALUES (%s, %s);
                # """, (channel_id, name))

                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to add channel '({channel_id}, {name})' "
                         f"to workspace with id: {workspace_id}")
            print(e, file=sys.stderr)
            self.get_connection().rollback()
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

    def add_message(self, workspace_id: str, channel_id: str, channel_name: str, msg_id: str,
                    time: datetime, from_slack_id: str, to_slack_id: str,
                    from_username: str, to_username: str,
                    text: str, kudos_value: List[str] = None) -> bool:
        try:
            logger.info(f"Adding message with msg_id '{msg_id}' "
                        f"from user with slack_id '{from_slack_id}' "
                        f"to user with slack_id '{to_slack_id}' "
                        f"in workspace with id: '{workspace_id}'")
            conn = self.get_connection()
            self.add_user(workspace_id, from_slack_id, from_username)
            self.add_user(workspace_id, to_slack_id, to_username)
            self.add_channel(workspace_id, channel_id, channel_name)

            with conn.cursor() as cursor:
                # TODO: Temporary work around

                # _select_schema(cursor, workspace_id)
                t = (f"INSERT INTO {workspace_id}.messages (id, channel_id, time, from_slack_id, to_slack_id, text)"
                     f"VALUES ('{msg_id}', '{channel_id}', '{time}', '{from_slack_id}', '{to_slack_id}', '{text}')")
                cursor.execute(t)

                # cursor.execute("""
                #     INSERT INTO messages (id, channel_id, time, from_slack_id,
                #                           to_slack_id, text)
                #     VALUES (%s, %s, %s, %s, %s, %s);
                # """, (msg_id, channel_id, time, from_slack_id,
                #       to_slack_id, text))

                # Only add the message id tied with kudos once
                t = f"SELECT message_id FROM {workspace_id}.kudos WHERE message_id = '{msg_id}'"
                cursor.execute(t)
                if cursor.fetchall() == []:
                    if kudos_value is not None:
                        for value in kudos_value:
                            t = f"SELECT id FROM {workspace_id}.corp_values WHERE corp_value = '{value}'"
                            cursor.execute(t)

                            # get the kudos value id
                            # cursor.execute("""
                            #     SELECT id FROM corp_values WHERE corp_value = %s;
                            # """, (value,))

                            kudos_value_id = cursor.fetchone()[0]

                            t = f"INSERT INTO {workspace_id}.kudos (message_id, corp_value_id) VALUES ('{msg_id}', '{kudos_value_id}')"
                            cursor.execute(t)

                            # cursor.execute("""
                            #     INSERT INTO kudos (message_id, corp_value_id)
                            #     VALUES (%s, %s);
                            # """, (msg_id, kudos_value_id))

                conn.commit()
                return True
        except Exception as e:
            print(e, file=sys.stderr)
            logger.error(f"Failed to add message in workspace with id '{workspace_id}'")
            self.get_connection().rollback()
            return False

    def add_corp_values(self, workspace_id: str, values: List[str]) -> bool:
        try:
            logger.info(f"Adding corp values '{values}' to workspace with id: {workspace_id}")
            conn = self.get_connection()
            with conn.cursor() as cursor:
                # TODO: Temporary workaround

                # _select_schema(cursor, workspace_id)

                # get the current values, we only insert values that are not
                # already in the table
                curr_values = self.get_corp_values(workspace_id)

                for value in values:
                    # check if the value is already in the table
                    if value not in curr_values:
                        # cursor.execute("""
                        #     INSERT INTO corp_values (corp_value) VALUES (%s);
                        # """, (value,))

                        t = f"INSERT INTO {workspace_id}.corp_values (corp_value) VALUES ('{value}')"

                        cursor.execute(t)
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to add values '{values}' to workspace with id '{workspace_id}'")
            print(e, file=sys.stderr)
            self.get_connection().rollback()
            return False

    def delete_corp_values(self, workspace_id: str, values: List[str]) -> bool:
        # TODO: Fix this
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
                # TODO:
                # Temporary work around

                t = f'select corp_value from {workspace_id}.corp_values'
                cursor.execute(t)

                values = []
                for row in cursor.fetchall():
                    values.append(row[0])

                return values
        except Exception as e:
            logger.error(f"Failed to get corp values from workspace with id '{workspace_id}'")
            print(e, file=sys.stderr)
            return ['DATABASE ERROR']

    def get_user_kudos(self, workspace_id: str, user_id: str,
                       start_time: int = 1,
                       end_time: int = datetime.timestamp(datetime.now())) -> Tuple[int, dict[str, int]]:
        # TODO: Figure out what's going with our schema things
        try:
            logger.info(f"Getting kudos stats of the user with id: {user_id}")
            logger.info(f"Start time is (UNIX): {start_time}")
            logger.info(f"End time is (UNIX): {end_time}")
            # get connection
            conn = self.get_connection()
            with conn.cursor() as cursor:
                # TODO: Temporary work around

                t = f"""
                SELECT corp_values.corp_value, COUNT(*) as kudos_count
                FROM {workspace_id}.messages
                JOIN {workspace_id}.kudos ON messages.id = kudos.message_id
                JOIN {workspace_id}.corp_values ON kudos.corp_value_id = corp_values.id
                WHERE messages.to_slack_id = '{user_id}' AND
                time <= to_timestamp({end_time}) AND time >= to_timestamp({start_time})
                GROUP BY kudos.corp_value_id, corp_values.corp_value;
                """

                cursor.execute(t)

                # cursor.execute(
                #     """
                #     SELECT corp_values.corp_value, COUNT(*) as kudos_count
                #     FROM messages
                #     JOIN kudos ON messages.id = kudos.message_id
                #     JOIN corp_values ON kudos.corp_value_id = corp_values.id
                #     WHERE messages.to_slack_id = 'your_user_id'
                #     GROUP BY kudos.corp_value_id, corp_values.corp_value;
                #     """,
                #     (user_id,)
                # )

                stats = {}
                for kudo in cursor.fetchall():
                    stats[kudo[0]] = kudo[1]

            return sum(stats.values()), stats
        except Exception as e:
            logger.error(f"Failed to get corp values from the user with id '{user_id}'")
            print(e, file=sys.stderr)
            return 0, {}

    def _connect(self):
        return pg.connect(host=self.hostname, port=self.port,
                          dbname=self.dbname, user=self.user,
                          password=self.password)

    def get_connection(self):
        logger.info("Getting connection to PostgreSQL database...")

        # Try to get connection 5 times, if failed, raise exception
        i = 0
        while self._connection.closed and i < 5:
            logger.info("Connection closed, reconnecting...")
            self._connection = self._connect()
            i += 1

        if i == 5:
            raise Exception('Connection failed!')

        logger.info('Successfully obtained connection')

        return self._connection
