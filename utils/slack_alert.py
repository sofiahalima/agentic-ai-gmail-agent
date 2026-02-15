import requests
import os

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_slack_alert(message: str):
    if not SLACK_WEBHOOK_URL:
        print("Slack webhook missing")
        return

    requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": message},
        timeout=5
    )
