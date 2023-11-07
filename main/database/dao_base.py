from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Tuple


class DAOBase(ABC):
    """
    The base class for all DAOs. This class defines the interface for all DAOs.

    For backend guys: Do NOT initialize any instance of the subclasses of this
                      class manually.
                      Instead, use the get_DAO() function in __init__.py.
    """

    @abstractmethod
    def create_workspace(self, workspace_id: str) -> bool:
        """
        Create a new workspace in the database.

        :param workspace_id: The unique identifier of the workspace.
        :return: If the workspace was created successfully.
        """
        raise NotImplementedError

    @abstractmethod
    def add_user(self, workspace_id: str, slack_id: str, name: str) -> bool:
        """
        Add a new user to the workspace.

        :param workspace_id: The unique identifier of the workspace that this
                             user belongs to.
        :param slack_id: The unique identifier of the user in Slack.
        :param name: The name of the user in Slack.
        :return: If the user was added successfully.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_user(self, workspace_id: str, slack_id: str) -> bool:
        """
        Delete a user from the workspace. Note that this does not delete
        the message this user sent/recieved.

        :param workspace_id: The unique identifier of the workspace that this
        :param slack_id: The unique identifier of the user in Slack.
        :return: If the user was deleted successfully.
        """
        raise NotImplementedError

    @abstractmethod
    def add_channel(self, workspace_id: str,
                    channel_id: str, name: str) -> bool:
        """
        Add a new channel to the workspace.

        :param workspace_id: The unique identifier of the workspace that this
                             channel belongs to.
        :param channel_id: The unique identifier of the channel in Slack.
        :param name: The name of the channel in Slack.
        :return: If the channel was added successfully.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_channel(self, workspace_id: str, channel_id: str) -> bool:
        """
        Delete a channel from the workspace. Note that this does not delete
        the messages in this channel.

        :param workspace_id: The unique identifier of the workspace that this
                             channel belongs to.
        :param channel_id: The unique identifier of the channel in Slack.
        :return: If the channel was deleted successfully.
        """
        raise NotImplementedError

    @abstractmethod
    def add_message(self, workspace_id: str, channel_id: str, channel_name: str, msg_id: str,
                    time: datetime, from_slack_id: str, to_slack_id: str,
                    from_username: str, to_username: str,
                    text: str, kudos_value: List[str] = None) -> bool:
        """
        Add a new message to the workspace and record its kudos value.

        TODO: Fix this docstring
        :param channel_name:
        :param from_username:
        :param to_username:
        :param workspace_id: The unique identifier of the workspace that this
                             message belongs to.
        :param channel_id: The unique identifier of the channel that this
                           message belongs to.
        :param msg_id: The unique identifier of the message in Slack.
        :param time: The time the message was sent.
        :param from_slack_id: The unique identifier of the user who sent the
                              message.
        :param to_slack_id: The unique identifier of the user who received the
                            message.
        :param text: The text of the message.
        :param kudos_value: The kudos values (if any) of the message.
        :return: If the message was added successfully.
        """
        raise NotImplementedError

    @abstractmethod
    def add_corp_values(self, workspace_id: str, values: List[str]) -> bool:
        """
        Add a new corporate value to the workspace.

        :param workspace_id: The unique identifier of the workspace that this
                             corporate value belongs to.
        :param values: The corporate value to add.
        :return: If the corporate value was added successfully.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_corp_values(self, workspace_id: str, values: List[str]) -> bool:
        """
        Delete a corporate value from the workspace.
        This function will also delete all relevant kudos associated with the
        values.

        :param workspace_id: The unique identifier of the workspace that this
                             corporate value belongs to.
        :param values: The corporate values to delete.
        :return: If the corporate value was deleted successfully.
        """
        raise NotImplementedError

    @abstractmethod
    def get_corp_values(self, workspace_id: str) -> List[str]:
        """
        Get all corporate values from the workspace.

        :param workspace_id: The unique identifier of the workspace to get
                             corporate values from.
        :return: A list of corporate values.
        """
        raise NotImplementedError

    @abstractmethod
    def get_user_kudos(self, workspace_id: str, user_id: str) -> Tuple[int, dict[str, int]]:
        """
        Get all corporate values from the workspace.

        :param workspace_id: The unique identifier for workspace
        :param user_id: The unique identifier of the user to get kudos from
        :return: A list of corporate values.
        """
        raise NotImplementedError
