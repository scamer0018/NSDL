import sys
from config import get_config
from libs import Void
from utils import Log


def main():
    config = get_config()

    try:
        number = config.number or input("📱 Enter your phone number: ").strip()

        if not number:
            Log.error("❌ Phone number is required.")
            sys.exit(1)

        client = Void(config.session, config, Log)
        client.PairPhone(phone=number, show_push_notification=True)

    except Exception as e:
        Log.critical(f"🚨 Unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
