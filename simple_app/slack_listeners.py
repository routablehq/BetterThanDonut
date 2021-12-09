import logging
import os
from ohmuffin import models
import json

from slack_bolt import App

logger = logging.getLogger(__name__)

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    # disable eagerly verifying the given SLACK_BOT_TOKEN value
    token_verification_enabled=False,
)


@app.event("app_mention")
def handle_app_mentions(logger, event, say):
    slack_user_id = event["user"]
    slack_user_profile = app.client.users_info(user=slack_user_id).data["user"]["profile"]
    interests = models.Interest.objects.all()
    first_name = slack_user_profile["first_name"]
    last_name = slack_user_profile["last_name"]
    message = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Welcome to the Oh, Muffin"
        }
    }
    options = [{
        "text": {
            "type": "plain_text",
            "text": interest.name,
            "emoji": True
        },
        "value": str(interest.id)
    } for interest in interests]
    interest_section = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Please enter your interest so that we can match you with other muffin users."
        },
        "accessory": {
            "type": "multi_static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select interests",
                "emoji": True
            },
            "options": options,
            "action_id": "multi_static_select-action"
        }
    }
    models.Profile.objects.get_or_create(slack_id=slack_user_id, first_name=first_name, last_name=last_name)
    app.client.chat_postEphemeral(channel=event["channel"], user=slack_user_id, blocks=[message, interest_section])
