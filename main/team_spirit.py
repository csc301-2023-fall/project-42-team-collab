import config
from design import *

from database import *
from typing import Tuple
from datetime import datetime

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import logging
logger = logging.getLogger(__name__)

app = App(
    token=config.SLACK_BOT_TOKEN
)

DAO = get_DAO()


# #############################################################################
# Basic feature for team_spirit
# #############################################################################
@app.event("app_mention")
def event_test(event, say):
    say(f"Hi there, <@{event['user']}>!")


@app.command("/echo")
def echo(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(f"{command['text']}")


# #############################################################################
# Set up helper function
# #############################################################################
def fetch_kudos_for_user(workspace_id: str, user_id: str) -> Tuple[int, str]:
    """
    Helper function to fetch kudos data for a user
    Args:
        workspace_id: current workspace id
        user_id: given user id

    Returns:
        kudos_count: amount of total kudos received with given user
        kudos_values_status: string contain given user's received corp values history.
    """
    logger.info(f"Fetching kudos data for user {user_id}")
    user_kudos_data = DAO.get_user_kudos(workspace_id, user_id)
    kudos_count = user_kudos_data[0]
    corp_values = user_kudos_data[1]

    kudos_values_status = "\n".join([f"• {kudos}: {count}" for kudos, count in corp_values.items()])

    return kudos_count, kudos_values_status


# #############################################################################
# COMMAND HANDLER: /kudos_overview
# #############################################################################
@app.command("/kudos_overview")
def kudos_overview(ack, command, client, payload) -> None:
    """
    Open kudos_overview modal on given client slack
    Args:
        ack: Acknowledgement function to respond to Slack's request.
        command: Stores information about this invoked command.
        client: Slack's API client for performing actions like sending messages.
        payload: Additional data about the event that triggered the function.
    """
    ack()
    logger.info("/kudos_overview - Command received")

    workspace_id = payload['team_id']
    DAO.create_workspace(workspace_id)

    logger.info("/kudos_overview - Submission event received")

    # Define a modal that includes a user selection block
    view = set_up_overview_modal()

    # Open the modal
    client.views_open(trigger_id=command['trigger_id'], view=view)


@app.view("view_kudos_modal")
def handle_kudos_view(ack, body, client) -> None:
    """
    Handles the modal view for displaying kudos information of selecting user.
    Args:
        ack: Acknowledgement function to respond to Slack's request.
        body: The request body that triggered the view.
        client: The Slack client to interact with the Slack API.
    """
    ack()

    # Extract the selected user ID
    try:
        selected_user_id = body['view']['state']['values']['user_select']['user_selected']['selected_user']
    except KeyError as e:
        # Log the error and body for debugging
        logger.error(f"/kudos_overview - EmptySelectError: selected_user is None {e}")
        logger.error(body)
        return

    workspace_id = body['team']['id']

    # Fetch and format the kudos data for the selected user
    kudos_count, kudos_value_status = fetch_kudos_for_user(workspace_id, selected_user_id)

    # Fetch the user's info to get the username
    try:
        user_info = client.users_info(user=selected_user_id)
        username = user_info['user']['name']
    except Exception as e:
        logger.error(f"/kudos_overview - Error fetching user info: {e}")
        username = selected_user_id  # Fallback to user ID if fetch fails

    # Define a modal that shows the kudos overview
    view = set_up_kudos_overview_top(username, kudos_count)

    # Add kudos details section if kudos details are present
    if kudos_value_status.strip():
        kudos_details_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"\n{kudos_value_status}"
            }
        }
        view["blocks"].append(kudos_details_block)
    else:
        no_kudos_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "_No kudos received yet._"
            }
        }
        view["blocks"].append(no_kudos_block)

    # Open the modal
    client.views_open(trigger_id=body['trigger_id'], view=view)


# #############################################################################
# COMMAND HANDLER: /kudos
# #############################################################################
@app.command("/kudos")
def open_modal(ack, command, client, payload) -> None:
    """
    Open modal for giving teammate kudos.
    Args:
        ack: Acknowledgement function to respond to Slack's request.
        command: Stores information about this invoked command.
        client: Slack's API client for performing actions like sending messages.
        payload: Additional data about the event that triggered the function, including IDs and team_id.
    """
    ack()
    logger.info(f"/kudos - Command received")
    # Open the modal

    workspace_id = payload['team_id']
    DAO.create_workspace(workspace_id)

    corp_vals = DAO.get_corp_values(workspace_id)

    client.views_open(trigger_id=command["trigger_id"], view=set_up_kudos_modal(corp_vals))


@app.view("kudos_modal")
def handle_submission(ack, body, view, client, payload) -> None:
    """
    Processes the submission of the 'kudos_modal' and sends kudos messages based on user input.

    Args:
        ack: Acknowledges the view_submission event to Slack to avoid timeouts.
        body: Contains information about the user who triggered the modal.
        view: Contains the state and input values of the modal.
        client: Slack's API client for performing actions like sending messages.
        payload: Additional data about the view_submission event, including IDs and team_id.
    """
    # Acknowledge the view_submission event
    ack()

    workspace = payload['team_id']
    DAO.create_workspace(workspace)

    logger.info("/kudos - Submission event received")

    sender_id = body["user"]["id"]
    logger.info(f"/kudos - Selecting sender id as {sender_id}")
    try:
        # Extract recipient ID from view
        recipient_id = view['state']['values']["recipient_select_block"]["user_select_action"]["selected_user"]
        logger.info(f"/kudos - Selecting recipient id as {recipient_id}")

        # Extract channel ID from view
        channel_id = view['state']['values']['channel_select_block']['channel_select_action']['selected_channel']
        logger.info(f"/kudos - Selecting channel id as {channel_id}")

        # Extract selected corporation values from view
        selected_values = view['state']['values']['corp_select_block']['multi_static_select-action']['selected_options']
        selected_value_texts = [option['text']['text'] for option in selected_values]
        logger.info(f"/kudos - Selecting value text as {selected_value_texts}")

        # Extract message text from view
        message_text = view['state']['values']['message_input_block']['plain_text_input-action']['value']
        logger.info(f"/kudos - Inputting message as {message_text}")

        # Extract checkbox values find out which checkbox is selected
        selected_checkbox_options = view['state']['values']['checkboxes_block']['checkboxes_action']['selected_options']
        notify_recipient_selected = False
        announce_kudos_selected = False

        for option in selected_checkbox_options:
            if option['value'] == 'notify_recipient':
                notify_recipient_selected = True
            elif option['value'] == 'announce_kudos':
                announce_kudos_selected = True

        values_recognized = '\n'.join([f"\t\t{value}" for value in selected_value_texts])
        message = (
            ":tada: *Kudos Announcement* :tada:\n"
            f"From: <@{sender_id}>\n\n"
            f"To: <@{recipient_id}>\n\n"
            f"At Channel: <#{channel_id}>\n\n"
            "Values Recognized: \n"
            f"{values_recognized}\n\n"
            "Message:\n"
            f"{message_text}\n"
        )

        # This is actually view ID, but it's also unique, so it should be good
        message_id = payload['id']

        from_username = app.client.users_info(user=sender_id)['user']['profile']['display_name']
        to_username = app.client.users_info(user=recipient_id)['user']['profile']['display_name']
        channel_name = app.client.conversations_info(channel=channel_id)['channel']['name']

        DAO.add_message(workspace_id=workspace,
                        channel_id=channel_id,
                        channel_name=channel_name,
                        msg_id=message_id,
                        time=datetime.now(),
                        from_slack_id=sender_id,
                        from_username=from_username,
                        to_slack_id=recipient_id,
                        to_username=to_username,
                        text=message_text,
                        kudos_value=selected_value_texts)

        # Send a direct message to the recipient if the checkbox is selected
        if notify_recipient_selected:
            client.chat_postMessage(
                channel=recipient_id,
                text=message
            )

        # Send a message to the channel if the checkbox is selected
        if announce_kudos_selected:
            client.chat_postMessage(
                channel=channel_id,
                text=message
            )

        # Send a confirmation message to the user.
        client.chat_postMessage(
            channel=sender_id,
            text="Kudos sent successfully!"
        )
    except Exception as e:
        logger.error(f"/kudos - Error received in handle_submission: {e}")
        client.chat_postMessage(
            channel=sender_id,
            text="Kudos failed to send. Please try again."
        )


# #############################################################################
# COMMAND HANDLER: /kudos_customize
# #############################################################################
@app.command("/kudos_customize")
def open_customize_corp_value_modal(ack, command, client, payload) -> None:
    """
    Open customize corp value modal
    Args:
        ack: Acknowledges the view_submission event to Slack to avoid timeouts.
        command: Stores information about this invoked command.
        client: Slack's API client for performing actions like sending messages.
        payload: Additional data about the event is triggered, including IDs and team team_id.
    """
    ack()
    logger.info(f"/kudos_customize - Command received")

    workspace_id = payload['team_id']
    DAO.create_workspace(workspace_id)

    client.views_open(trigger_id=command["trigger_id"], view=set_up_customize_modal())


@app.view("custom_value_modal")
def handle_custom_submission(ack, body, client, view, payload) -> None:
    """
    Processes the submission of the '/kudos_customize' and notify user with their new added corp value.

    Args:
        ack: Acknowledges the view_submission event to Slack to avoid timeouts.
        body: Contains information about the user who triggered the modal.
        view: Contains the state and input values of the modal.
        client: Slack's API client for performing actions like sending messages.
        payload: Additional data about the view_submission event, including id and team_id
    """
    # Acknowledge the view_submission event
    ack()
    logger.info(f"/kudos_customize -  Submission event received")

    workspace_id = payload['team_id']
    DAO.create_workspace(workspace_id)

    # Extract values from the view
    new_corp_value = view['state']['values']["new_value_block"]["new_corp_value_input"]["value"]

    DAO.add_corp_values(workspace_id, [new_corp_value])
    logger.info(f"/kudos_customize - New corp value {new_corp_value} added")

    # Give the user a success message
    sender_id = body["user"]["id"]
    client.chat_postMessage(
        channel=sender_id,
        text=f"Successfully added {new_corp_value} to the list of corp values!"
    )


@app.action("checkboxes_action")
def handle_checkbox_action(ack) -> None:
    """
    Acknowledges slack API on checkbox action.
    Args:
        ack: Acknowledges the view_submission event to Slack to avoid timeouts.
    """
    ack()


def run() -> None:
    """
    Run team_spirit slack bot
    """
    SocketModeHandler(app, config.SLACK_APP_TOKEN).start()


# Start your slack app on standalone
if __name__ == "__main__":
    import logging.config

    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('database')
    logger.info(f"Running team_spirit.py standalone")

    run()
