import json
import textwrap

import requests

from utils.utils import env_var

SLACK_CHANNEL = env_var("INPUT_SLACK_WEBHOOK")


def notify(title: str, message: str):
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "emoji": True,
                "text": title
            }
        },
    ]
    if len(message) > 1500:
        for part in textwrap.wrap(message, 1500):
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": part
                }
            })
    else:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": message
            }
        })
    slack_message = {
        "response_type": "in_channel",
        "blocks": blocks
    }

    requests.post(SLACK_CHANNEL, json.dumps(slack_message))
