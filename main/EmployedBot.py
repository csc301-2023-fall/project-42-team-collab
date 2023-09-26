import os
import config

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

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, config.SLACK_APP_TOKEN).start()
