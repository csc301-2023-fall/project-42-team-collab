import logging
logger = logging.getLogger(__name__)

SLACK_BOT_TOKEN = "xoxb-5933772890579-5945241825189-YUY5SWx1bvaMp3opBV8qeTq0"
SLACK_SIGNING_SECRET = "48928ff7a9457f0f4264af506b5b6bcf"
SLACK_APP_TOKEN = "xapp-1-A05TW1NB0CB-5948193295891-720a67e31f92b0c273bbe5ff3525501b3cdf79421f7aa4143d61ba6cc9d08c53"

PORT = 3000

# Report debug information
logger.debug(f'Slack bot token: {SLACK_BOT_TOKEN}')
logger.debug(f'Slack signing secret token: {SLACK_SIGNING_SECRET}')
logger.debug(f'Slack app token: {SLACK_APP_TOKEN}')
logger.debug(f'Port: {PORT}')