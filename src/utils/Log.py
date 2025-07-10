from datetime import datetime, timezone, timedelta
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class Log:
    IST = timezone(timedelta(hours=5, minutes=30))

    # Color definitions (all bold via Style.BRIGHT)
    LEVEL_COLORS = {
        "info": Style.BRIGHT + Fore.GREEN,
        "debug": Style.BRIGHT + Fore.BLUE,
        "warn": Style.BRIGHT + Fore.MAGENTA,   # Pink-ish
        "error": Style.BRIGHT + Fore.RED,
        "critical": Style.BRIGHT + Fore.RED,
    }

    @staticmethod
    def _print(level: str, message: str):
        now = datetime.now(Log.IST).strftime("%Y-%m-%d %H:%M:%S (+0530)")
        level_tag = level.upper()
        color = Log.LEVEL_COLORS.get(level, Style.BRIGHT)
        reset = Style.RESET_ALL

        print(f"[{now}] [{color}{level_tag}{reset}] {color}{message}{reset}")

    @staticmethod
    def info(message: str):
        Log._print("info", message)

    @staticmethod
    def debug(message: str):
        Log._print("debug", message)

    @staticmethod
    def warn(message: str):
        Log._print("warn", message)

    @staticmethod
    def error(message: str):
        Log._print("error", message)

    @staticmethod
    def critical(message: str):
        Log._print("critical", message)
