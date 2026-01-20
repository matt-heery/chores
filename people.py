"""Get whatsapp numbers."""

import json
import os


def get_user_whatsapp_map() -> dict[str, str]:
    """Return mapping of whatsapp numbers."""
    raw = os.environ.get("TODOIST_USER_MAP", "{}")
    id_to_key = json.loads(raw)

    mapping = {}
    for todoist_id, key in id_to_key.items():
        env_key = f"WA_{key}"
        if env_key in os.environ:
            mapping[todoist_id] = os.environ[env_key]

    return mapping
