import sys
from config import get_config
from libs import Void
from utils import Log

config = get_config()

if __name__ == "__main__":
    try:
        number = config.number
        if not config.number:
            Log.critical("Please enter your phone number below to continue.")
            number = input("-> ")
        Void(config.session, config, Log).PairPhone(phone=number, show_push_notification=True)
    except Exception as e:
        print(e)
        sys.exit(0)
