import config
import database
from design import *

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(
    token=config.SLACK_BOT_TOKEN,
)


@app.event("app_mention")
def event_test(event, say):
    say(f"Hi there, <@{event['user']}>!")


@app.command("/echo")
def echo(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(f"{command['text']}")


@app.command("/kudos_overview")
def kudos_overview(ack, command, client):
    ack()

    # Define a modal that includes a user selection block
    view = set_up_overview_modal()

    # Open the modal
    client.views_open(trigger_id=command['trigger_id'], view=view)


@app.view("view_kudos_modal")
def handle_kudos_view(ack, body, client):
    ack()

    # Extract the selected user ID
    try:
        selected_user_id = body['view']['state']['values']['user_select']['user_selected']['selected_user']
    except KeyError as e:
        # Log or print the error and body for debugging
        print(f"KeyError: {e}")
        print(body)
        return

    # Fetch and format the kudos data for the selected user
    kudos_count, kudos_value_status = fetch_kudos_for_user(selected_user_id)

    # Fetch the user's info to get the username
    try:
        user_info = client.users_info(user=selected_user_id)
        username = user_info['user']['name']
    except Exception as e:
        print(f"Error fetching user info: {e}")
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


# Helper function to fetch kudos data for a user
def fetch_kudos_for_user(user_id):
    user_kudos_data = database.load_user_kudos_status(user_id)
    kudos_count = user_kudos_data.get("total_kudos", 0)
    corp_values = user_kudos_data.get("corp_values", {})

    kudos_values_status = "\n".join([f"• {kudos}: {count}" for kudos, count in corp_values.items()])

    return kudos_count, kudos_values_status


@app.command("/kudos")
def open_modal(ack, command, client):
    # TODO: if there is new user or channel added, add them to the database
    ack()
    # Open the modal
    client.views_open(trigger_id=command["trigger_id"], view=set_up_kudos_modal())


@app.command("/kudos_customize")
def open_customize_corp_value_modal(ack, command, client):
    ack()
    print("Customize Corp Value Command Received")
    client.views_open(trigger_id=command["trigger_id"], view=set_up_customize_modal())


@app.view("custom_value_modal")
def handle_custom_submission(ack, body, client, view):
    # Acknowledge the view_submission event
    ack()
    print("view_submission event received")
    # Extract values from the view
    new_corp_value = view['state']['values']["new_value_block"]["new_corp_value_input"]["value"]
    database.add_new_corp_value(new_corp_value)
    # Give the user a success message
    sender_id = body["user"]["id"]
    client.chat_postMessage(
        channel=sender_id,
        text=f"Successfully added {new_corp_value} to the list of corp values!"
    )


@app.view("kudos_modal")
def handle_submission(ack, body, view, client):
    # Acknowledge the view_submission event
    ack()
    print("view_submission event received")

    sender_id = body["user"]["id"]
    print("sender_id: ", sender_id)

    try:
        # Extract recipient ID from view
        recipient_id = view['state']['values']["recipient_select_block"]["user_select_action"]["selected_user"]
        print("recipient_id: ", recipient_id)

        # Extract channel ID from view
        channel_id = view['state']['values']['channel_select_block']['channel_select_action']['selected_channel']
        print("channel_input: ", channel_id)

        # Extract selected corporation values from view
        selected_values = view['state']['values']['corp_select_block']['multi_static_select-action']['selected_options']
        selected_value_texts = [option['text']['text'] for option in selected_values]
        print("selected_values: ", selected_value_texts)

        # Extract message text from view
        message_text = view['state']['values']['message_input_block']['plain_text_input-action']['value']
        print("message_text: ", message_text)

        # Extract checkbox values find out which checkbox is selected
        selected_checkbox_options = view['state']['values']['checkboxes_block']['checkboxes_action']['selected_options']
        notify_recipient_selected = any([option['value'] == 'notify_recipient' for option in selected_checkbox_options])
        announce_kudos_selected = any([option['value'] == 'announce_kudos' for option in selected_checkbox_options])

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

        # TODO: Add real database function to add kudos here
        database.add_kudos(recipient_id, selected_value_texts)
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
        print(e)
        client.chat_postMessage(
            channel=sender_id,
            text="Kudos failed to send. Please try again."
        )


@app.action("checkboxes_action")
def handle_checkbox_action(ack):
    ack()


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, config.SLACK_APP_TOKEN).start()
