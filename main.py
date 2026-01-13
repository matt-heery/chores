"""Get chores and send message."""

from tasks import get_weekly_chores
from whatsapp import send_whatsapp


def main() -> None:
    """Glues functions together."""
    message = get_weekly_chores()
    send_whatsapp(message)

if __name__ == "__main__":
    main()
