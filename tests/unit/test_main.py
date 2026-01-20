"""Test main module."""

import pytest

import main


def test_main_sends_weekly_chores(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main function sends weekly chores correctly."""
    fake_tasks = {
        "user_1": ["Take out trash", "Vacuum"],
        "user_2": ["Clean bathroom"],
        "user_3": [],
    }
    fake_project_url = "https://todoist.com/app/project/123"

    sent_messages = []

    monkeypatch.setattr(main, "get_tasks_by_assignee", lambda: (fake_tasks, fake_project_url))

    monkeypatch.setattr(
        main,
        "get_user_whatsapp_map",
        lambda: {
            "user_1": "whatsapp:+111",
            "user_2": "whatsapp:+222",
        },
    )

    monkeypatch.setattr(
        main,
        "send_whatsapp",
        lambda to, msg: sent_messages.append((to, msg)),
    )

    main.main()

    assert len(sent_messages) == 2  # noqa: PLR2004

    to1, msg1 = sent_messages[0]
    assert to1 == "whatsapp:+111"
    assert "Take out trash" in msg1
    assert "Vacuum" in msg1
    assert fake_project_url in msg1
    assert "🧹 *Your chores this week*" in msg1

    to2, msg2 = sent_messages[1]
    assert to2 == "whatsapp:+222"
    assert "Clean bathroom" in msg2
    assert fake_project_url in msg2
    assert "🧹 *Your chores this week*" in msg2
