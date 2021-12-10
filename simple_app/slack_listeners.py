import logging
import os

from ohmuffin import models

from slack_bolt import App

from ohmuffin.match import dumb_match

logger = logging.getLogger(__name__)

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    # disable eagerly verifying the given SLACK_BOT_TOKEN value
    token_verification_enabled=False,
)


@app.event("member_joined_channel")
def initial_join(logger, event):
    channel_id = event["channel"]
    if channel_id == os.environ["SLACK_MUFFIN_CHANNEL_ID"]:
        send_interest_form(event["user"], channel_id)


@app.command("/update_muffin")
def update_command(ack, body):
    ack()
    send_interest_form(body["user_id"], body["channel_id"])


def send_interest_form(slack_user_id, channel_id):
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
            "action_id": "interest-selection"
        }
    }
    models.Profile.objects.get_or_create(slack_id=slack_user_id, first_name=first_name, last_name=last_name)
    app.client.chat_postEphemeral(channel=channel_id, user=slack_user_id, blocks=[message, interest_section])


@app.action("interest-selection")
def receive_interests(body, ack, say):
    ack()
    slack_id = body["user"]["id"]
    user = models.Profile.objects.get(slack_id=slack_id)
    selected_interests = body['actions'][0]["selected_options"]
    interest_ids = [interest["value"] for interest in selected_interests]
    user.interests.clear()
    user.interests.add(*interest_ids)

