import datetime
from typing import List

import config

import logging
logger = logging.getLogger(__name__)


# #############################################################################
# BLOCK DESIGNED: kudos modal generated by `/kudos`
# #############################################################################
def set_up_kudos_modal(corp_vals: List[str], initial_users: List[str],
                       initial_channel: str, prefill_msg: str,
                       values: List[str]) -> dict:
    """
    set up kudos modal
    Args:
        corp_vals: default corp value and customized corp value
        initial_users: a list of users to be pre-selected
        initial_channel: the initial channel that will be pre-filled into the modal view
        prefill_msg: the initial message that is parsed and filled into the message box
        values: the parsed list of values that will be pre-filled into the kudos box

    Returns:
        kudos modal in JSON format
    """
    corp_value = set_up_corp_value(corp_vals, initial_values=values)

    # Define the view (modal content)
    return {
        "type": "modal",
        "callback_id": "kudos_modal",
        "title": {
            "type": "plain_text",
            "text": "Kudos",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
            "emoji": True
        },
        "blocks": [
            set_up_recipient(initial_users),
            set_up_recipient_footnote(),
            set_up_channel(initial_channel),
            set_up_channel_footnote(),
            corp_value,
            set_up_corp_value_footnote(),
            set_up_message(prefill_msg),
            # set_up_message_footnote(),
            set_up_checkbox()
        ]
    }


def set_up_recipient(initial_users: List[str]) -> dict:
    """
    set up recipient block for kudos modal

    Returns:
        recipient block in JSON format
    """
    return {
        # The recipient block that will sometimes be prefilled
        "type": "input",
        "block_id": "recipient_select_block",
        "element": {
            "type": "multi_users_select",
            # Pre filled users
            "initial_users": initial_users,
            "placeholder": {
                "type": "plain_text",
                "text": "Select user to send kudos"
            },
            "action_id": "user_select_action"
        },
        "label": {
            "type": "plain_text",
            "text": "Recipient"
        }
    }


def set_up_channel(initial_channel: str) -> dict:
    """
    set up channel block for kudos modal

    Returns:
        channel block in JSON format
    """
    input_block = {
        # The channel blocks for selection
        "type": "input",
        "block_id": "channel_select_block",
        "label": {
            "type": "plain_text",
            "text": "Channel"
        },
        "element": {
            "type": "channels_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select a channel"
            },
            "action_id": "channel_select_action"
        }
    }

    if initial_channel != "":
        input_block["element"]["initial_channel"] = initial_channel

    return input_block


def set_up_corp_value(custom_values: List[str], initial_values: List[str]) -> dict:
    """
    Set up corp value(including customized) block for kudos modal
    Args:
        custom_values: list of customized corporate values
        initial_values: list of initial values that are pre-filled

    Returns:
        corp_value: all corp values labeled in JSON format

    """
    corporate_values = custom_values

    initial_values = set(initial_values)
    custom_values = set(custom_values)

    actual_prefilled = initial_values & custom_values

    # Generate options programmatically
    options = []
    for index, value in enumerate(corporate_values):
        option = {
            "text": {
                "type": "plain_text",
                "text": f"{value}",
                "emoji": True
            },
            "value": f"value-{index}"  # Generate a value ID dynamically based on the index
        }
        options.append(option)

    logger.info(options)

    corp_val = {
        # This is the message block for the corp values options that we have
        "type": "input",
        "block_id": "corp_select_block",
        "element": {
            "type": "multi_static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select options",
                "emoji": True
            },
            # These lists out all the options
            "options": options,
            "action_id": "multi_static_select-action"
        },
        "label": {
            "type": "plain_text",
            "text": "Corporation Values",
            "emoji": True
        }
    }

    if len(actual_prefilled) != len(initial_values):
        corp_val['label']['text'] = "Corporation Values (*Prefill failed for at least 1 value!*)"

    if len(actual_prefilled) > 0:
        initial_options = []

        for value in actual_prefilled:
            # Look through in the options list
            for option in options:
                # option is a dict with fields text (contains the value I'm looking for)
                if option['text']['text'] == value:
                    initial_options.append(option)

        corp_val['element']['initial_options'] = initial_options

    return corp_val


def set_up_message(prefill_msg: str) -> dict:
    """
    set up message input block for kudos modal

    Maximum length 300 characters, enforced by "max_length"

    Returns:
        message input block in JSON format
    """
    return {
        # This is the message block to type in information about the kudos
        "type": "input",
        "block_id": "message_input_block",
        "element": {
            "type": "plain_text_input",
            "multiline": True,
            "max_length": config.MESSAGE_LENGTH_MAX,
            "action_id": "plain_text_input-action",
            "initial_value": prefill_msg.strip(),
            "placeholder": {
                "type": "plain_text",
                "text": "Feel free to kudos to others",
                "emoji": True
            }
        },
        "label": {
            "type": "plain_text",
            "text": "Message",
            "emoji": True
        }
    }


def set_up_recipient_footnote() -> dict:
    """
    set up recipient footnote block for kudos modal

    Returns:
        recipient footnote block in JSON format
    """
    return {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": "You can send kudos to multiple people (at least one)."
            }
        ]
    }


def set_up_channel_footnote() -> dict:
    """
    set up channel footnote block for kudos modal

    Returns:
        channel footnote block in JSON format
    """
    return {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": "You can only send kudos to *ONE* channel at a time."
            }
        ]
    }


def set_up_corp_value_footnote() -> dict:
    """
    set up corp value footnote block for kudos modal

    Returns:
        corp value footnote block in JSON format
    """
    return {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": "You can select *MULTIPLE* corporation values."
            }
        ]
    }


def set_up_message_footnote() -> dict:
    """
    set up message footnote block for kudos modal

    Returns:
         message footnote block in JSON format
    """
    return {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": f"Character limits: *{config.MESSAGE_LENGTH_MAX}* characters."
            }
        ]
    }


def set_up_checkbox() -> dict:
    """
    set up checkbox selected block for kudos modal

    Returns:
        checkbox selected block in JSON format
    """
    announce_in_channel = {
        "text": {
            "type": "mrkdwn",
            "text": "*Announce kudos in the chosen channel*"
        },
        "value": "announce_kudos"
    }

    notify_recipient = {
        "text": {
            "type": "mrkdwn",
            "text": "*Notify recipient with direct message about this kudos*"
        },
        "value": "notify_recipient"
    }

    return {
        "type": "actions",
        "block_id": "checkboxes_block",
        "elements": [
            {
                # This is the checkbox to choose the different options
                "type": "checkboxes",
                "action_id": "checkboxes_action",
                "options": [
                    notify_recipient,
                    announce_in_channel
                ],
                # Select the "announce in channel" by default
                "initial_options": [announce_in_channel]
            }
        ]
    }


# #############################################################################
# BLOCK DESIGNED: customize modal generated by `\kudos_customize`
# #############################################################################
def set_up_customize_modal() -> dict:
    """
    Set up customize modal

    values are limited from config.VALUE_LENGTH_MIN to config.VALUE_LENGTH_MAX characters
    enforced by max_length

    Returns:
        customize modal block labeled in JSON format
    """
    return {
        "type": "modal",
        "callback_id": "custom_value_modal",
        "title": {
            "type": "plain_text",
            "text": "Add Value",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
            "emoji": True
        },
        "blocks": [
            {
                # This is the block for value that will be added
                # The input block
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "min_length": config.VALUE_LENGTH_MIN,
                    "max_length": config.VALUE_LENGTH_MAX,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Name your new corporate value"
                    },
                    "action_id": "new_corp_value_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": f"New Corporate Value ({config.VALUE_LENGTH_MIN} - {config.VALUE_LENGTH_MAX} characters)",
                    "emoji": True
                },
                "block_id": "new_value_block"
            }
        ]
    }


# #############################################################################
# BLOCK DESIGNED: overview modal generated by `/kudos_overview`
# #############################################################################
def set_up_overview_modal() -> dict:
    """
    set up overview modal, let client overview user's kudos history.
    also supports a time frame selection so that we can filter information

    Returns:
        user select panel labeled in JSON format
    """
    # Calculate the Unix timestamp for the current time minus one year
    one_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)
    one_year_ago_timestamp = int(datetime.datetime.timestamp(one_year_ago))
    return {
        "type": "modal",
        "callback_id": "view_kudos_modal",
        "title": {"type": "plain_text", "text": "View Kudos"},
        "blocks": [
            {
                # This is the user picker
                "type": "input",
                "block_id": "user_select",
                "element": {
                    "type": "users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a user"
                    },
                    "action_id": "user_selected"
                },
                "label": {"type": "plain_text", "text": "Who do you want to view kudos for?"}
            },
            {
                # This is the start date time picker
                "type": "input",
                "block_id": "start_time_pick",
                "element": {
                    "type": "datetimepicker",
                    "action_id": "datetimepicker-start_time",
                    # Unix time 1 means starting from the first moment,
                    # i.e. pick earliest time possible
                    # I didn't use time 0 because somehow it shows nothing in Slack
                    "initial_date_time": one_year_ago_timestamp
                },
                "hint": {
                    "type": "plain_text",
                    "text": "Start date & time that you want to view for this person",
                    "emoji": True
                },
                "label": {
                    "type": "plain_text",
                    "text": "Start date & time",
                    "emoji": True
                }
            },
            {
                # This is the end date time picker
                "type": "input",
                "block_id": "end_time_pick",
                "element": {
                    "type": "datetimepicker",
                    "action_id": "datetimepicker-end_time",
                    # The time up until this point you called the window
                    "initial_date_time": int(datetime.datetime.timestamp(datetime.datetime.now()))
                },
                "hint": {
                    "type": "plain_text",
                    "text": "End date & time that you want to view for this person",
                    "emoji": True
                },
                "label": {
                    "type": "plain_text",
                    "text": "End date & time",
                    "emoji": True
                }
            }
        ],
        "submit": {"type": "plain_text", "text": "View"}
    }


def set_up_kudos_overview_top(username: str, kudos_count: int) -> dict:
    """
    set up modal for displaying user's kudos history
    Args:
        username: target user's username
        kudos_count: total amount of kudos target user received

    Returns:
        kudos history detail of target user.

    """
    return {
        "type": "modal",
        "title": {"type": "plain_text", "text": "Kudos Overview"},
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"Kudos for @{username}"}
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Total Kudos Received:* {kudos_count}\n\n*Kudos Details:*"
                }
            }
        ]
    }
