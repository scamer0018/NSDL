import sys
import os
import time
from config import get_config
from libs import Void
from utils import Log


def main():
    config = get_config()

    number = config.number or input("📱 Enter your phone number: ").strip()

    if not number:
        Log.error("❌ Phone number is required.")
        sys.exit(1)

    client = Void(config.session, config, Log)
    client.PairPhone(phone=number, show_push_notification=True)


if __name__ == "__main__":
    while True:
        try:
            main()
            break
        except Exception as e:
            Log.critical(f"🚨 Unexpected error occurred: {e}")
            time.sleep(1)
            Log.info("🔄 Restarting script due to error...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
