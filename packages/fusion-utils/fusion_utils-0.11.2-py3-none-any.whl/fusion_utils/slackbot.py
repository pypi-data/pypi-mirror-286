import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackBot:
    def __init__(self, token):
        self.client = WebClient(token=token)

    def send_message(self, channel, text):
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=text
            )
            assert response["message"]["text"] == text
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")




