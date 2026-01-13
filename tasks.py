"""Fetch chores from google api client."""

from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/tasks.readonly"]
LIST_NAME = "House Chores"

def get_tasks_service() -> build:
    """Get tasks from google cloud."""
    creds = None
    if Path("token.json").exists:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
        with Path("token.json").open("w") as token:
            token.write(creds.to_json())

    return build("tasks", "v1", credentials=creds)

def get_weekly_chores() -> str:
    """Get tasks from chores."""
    service = get_tasks_service()
    lists = service.tasklists().list().execute().get("items", [])

    chores_list = next((it for it in lists if it["title"] == LIST_NAME), None)
    if not chores_list:
        return "No chores list found 🤷‍♂️"

    tasks = service.tasks().list(
        tasklist=chores_list["id"]
    ).execute().get("items", [])

    chores = [t["title"] for t in tasks if t.get("status") != "completed"]

    if not chores:
        return "🎉 No chores this week!"

    msg = "🧹 *This Week's Chores*\n\n"
    msg += "\n".join(f"• {c}" for c in chores)
    return msg
