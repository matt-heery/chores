"""Test whatsapp functionality."""

import os

import pytest

import whatsapp


def test_send_whatsapp(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test sending whatsapp message."""
    os.environ["TWILIO_ACCOUNT_SID"] = "AC_TEST"
    os.environ["TWILIO_AUTH_TOKEN"] = "AUTH_TEST"  # noqa: S105
    os.environ["WHATSAPP_FROM"] = "whatsapp:+14155238886"
    os.environ["WHATSAPP_TO"] = "whatsapp:+15551234567"

    created_messages = {}

    class FakeMessages:
        def create(self, body: str, from_: str, to: str) -> None:
            """Create fake message."""
            created_messages["body"] = body
            created_messages["from_"] = from_
            created_messages["to"] = to

    class FakeClient:
        def __init__(self, sid: str, token: str) -> None:
            """Initialize fake client."""
            assert sid == "AC_TEST"
            assert token == "AUTH_TEST"  # noqa: S105
            self.messages = FakeMessages()

    monkeypatch.setattr(whatsapp, "Client", FakeClient)

    whatsapp.send_whatsapp("hello chores")

    assert created_messages == {
        "body": "hello chores",
        "from_": "whatsapp:+14155238886",
        "to": "whatsapp:+15551234567",
    }
