import logging
import os

from slack_bolt import App

logger = logging.getLogger(__name__)

app = App(
    token="xoxb-2802274197799-2814051712533-UPHFZeT7G2cjvMZJR06tgAwj",
    signing_secret="cdaf815192ed345c83c5e500fd8edd32",
    # disable eagerly verifying the given SLACK_BOT_TOKEN value
    token_verification_enabled=False,
)


@app.event("app_mention")
def handle_app_mentions(logger, event, say):
    logger.info(event)
    say(f"Hi there, <@{event['user']}>")
