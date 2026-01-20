"""Test reminder module."""

import pytest

import reminder


def test_main_sends_reminders(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main function sends reminders correctly."""
    fake_tasks = {
        "user_1": ["Take out rubbish", "Vacuum"],
        "user_2": ["Clean bathroom"],
        "user_3": [],
    }
    fake_project_url = "https://todoist.com/app/project/123"

    sent_messages = []

    monkeypatch.setattr(reminder, "get_tasks_by_assignee", lambda: (fake_tasks, fake_project_url))

    monkeypatch.setattr(
        reminder,
        "get_user_whatsapp_map",
        lambda: {
            "user_1": "whatsapp:+111",
            "user_2": "whatsapp:+222",
        },
    )

    monkeypatch.setattr(
        reminder,
        "send_whatsapp",
        lambda to, msg: sent_messages.append((to, msg)),
    )

    reminder.main()

    assert len(sent_messages) == 2  # noqa: PLR2004

    to, msg = sent_messages[0]
    assert to == "whatsapp:+111"
    assert "Take out rubbish" in msg
    assert "Vacuum" in msg
    assert fake_project_url in msg

    to, msg = sent_messages[1]
    assert to == "whatsapp:+222"
    assert "Clean bathroom" in msg
    assert fake_project_url in msg
