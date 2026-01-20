"""Send WhatsApp reminders for pending Todoist chores."""

from people import get_user_whatsapp_map
from tasks import get_tasks_by_assignee
from whatsapp import send_whatsapp


def main() -> None:
    """Get pending chores and send WhatsApp reminders."""
    tasks_by_user, project_url = get_tasks_by_assignee()
    todoist_in_whatsapp = get_user_whatsapp_map()

    for user_id, chores in tasks_by_user.items():
        if not chores:
            continue

        if user_id not in todoist_in_whatsapp:
            continue

        msg = "⏰ *Reminder: chores still pending*\n\n"
        msg += "\n".join(f"• {c}" for c in chores)
        msg += f"\n\n{project_url}"

        send_whatsapp(todoist_in_whatsapp[user_id], msg)


if __name__ == "__main__":
    main()
