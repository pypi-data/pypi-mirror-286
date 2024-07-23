import os
import requests


class DMessage:
    WEBHOOK_BASE_URL = "https://discord.com/api/webhooks/"

    def __init__(self):
        self.webhook_id: str | None = os.getenv("WEBHOOK_ID")
        self.webhook_token: str | None = os.getenv("WEBHOOK_TOKEN")
        self.webhook_url: str | None = os.getenv("WEBHOOK_URL")

        if self.webhook_id and self.webhook_token:
            self.set_webhook(self.webhook_id, self.webhook_token)

    def set_webhook(self, webhook_id: str, webhook_token: str) -> None:
        """Set the webhook URL using the provided ID and token."""
        self.webhook_id = webhook_id
        self.webhook_token = webhook_token
        self.webhook_url = f"{self.WEBHOOK_BASE_URL}{
            webhook_id}/{webhook_token}"

    def send(self, message: str):
        """Send a message to the Discord webhook."""
        if not self.webhook_url:
            raise ValueError(
                "Webhook URL is not set. Use set_webhook() first.")

        data = {"content": message}
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            self.webhook_url, json=data, headers=headers)
        response.raise_for_status()
