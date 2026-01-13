"""Send whatsapp message."""

import os

from twilio.rest import Client


def send_whatsapp(message: str) -> None:
    """Send message to whatsapp."""
    client = Client(
        os.environ["TWILIO_ACCOUNT_SID"],
        os.environ["TWILIO_AUTH_TOKEN"]
    )

    client.messages.create(
        body=message,
        from_=os.environ["WHATSAPP_FROM"],
        to=os.environ["WHATSAPP_TO"]
    )

