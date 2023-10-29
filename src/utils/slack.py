import json
import textwrap

import requests


def notify(title: str, message: str, slack_channel: str):
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

    requests.post(slack_channel, json.dumps(slack_message))
