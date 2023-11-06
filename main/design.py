from typing import List

import logging
logger = logging.getLogger(__name__)


def set_up_recipient() -> dict:
    return {
        "type": "input",
        "block_id": "recipient_select_block",
        "element": {
            "type": "users_select",
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


def set_up_channel() -> dict:
    return {
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


def set_up_corp_value(custom_values: List[str]) -> dict:
    # Default list of corporate values and their corresponding emojis
    corporate_values = custom_values

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
        "type": "input",
        "block_id": "corp_select_block",
        "element": {
            "type": "multi_static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select options",
                "emoji": True
            },
            "options": options,
            "action_id": "multi_static_select-action"
        },
        "label": {
            "type": "plain_text",
            "text": "Corporation Values",
            "emoji": True
        }
    }

    return corp_val


def set_up_message() -> dict:
    return {
        "type": "input",
        "block_id": "message_input_block",
        "element": {
            "type": "plain_text_input",
            "multiline": True,
            "action_id": "plain_text_input-action",
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
    return {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": "You can only send kudos to *ONE* people at a time."
            }
        ]
    }


def set_up_channel_footnote() -> dict:
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
    return {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": "Word limit: *100* words."
            }
        ]
    }


def set_up_checkbox() -> dict:
    return {
        "type": "actions",
        "block_id": "checkboxes_block",
        "elements": [
            {
                "type": "checkboxes",
                "action_id": "checkboxes_action",
                "options": [
                    {
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Notify recipient with direct message about this kudos*"
                        },
                        "value": "notify_recipient"
                    },
                    {
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Announce kudos in the chosen channel*"
                        },
                        "value": "announce_kudos"
                    }
                ],
            }
        ]
    }


def set_up_customize_modal() -> dict:
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
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Name your new corporate value"
                    },
                    "action_id": "new_corp_value_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "New Corporate Value",
                    "emoji": True
                },
                "block_id": "new_value_block"
            }
        ]
    }


def set_up_kudos_modal(corp_vals: List[str]) -> dict:

    corp_value = set_up_corp_value(corp_vals)

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
            set_up_recipient(),
            set_up_recipient_footnote(),
            set_up_channel(),
            set_up_channel_footnote(),
            corp_value,
            set_up_corp_value_footnote(),
            set_up_message(),
            # set_up_message_footnote(),
            set_up_checkbox()
        ]
    }


def set_up_overview_modal() -> dict:
    return {
        "type": "modal",
        "callback_id": "view_kudos_modal",
        "title": {"type": "plain_text", "text": "View Kudos"},
        "blocks": [
            {
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
            }
        ],
        "submit": {"type": "plain_text", "text": "View"}
    }


def set_up_kudos_overview_top(username: str, kudos_count: int) -> dict:
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
