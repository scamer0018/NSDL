from datetime import datetime
from zoneinfo import ZoneInfo
from pymodm import connect
from pymodm.errors import DoesNotExist
from models import User, Group, Command
from utils import DynamicConfig


class Database:
    def __init__(self, uri):
        connect(uri)

    @staticmethod
    def now():
        return datetime.now(ZoneInfo("Asia/Kolkata"))

    def _update_or_create_user(self, number, updates: dict):
        try:
            user = User.objects.raw({"number": number}).first()
            for k, v in updates.items():
                setattr(user, k, v)
            user.save()
        except DoesNotExist:
            updates["number"] = number
            updates["created_at"] = self.now()
            User(**updates).save()

    def _update_or_create_group(self, number, updates: dict):
        try:
            group = Group.objects.raw({"number": number}).first()
            for k, v in updates.items():
                setattr(group, k, v)
            group.save()
        except DoesNotExist:
            updates["number"] = number
            Group(**updates).save()

    def update_user_ban(self, number, ban, reason):
        self._update_or_create_user(number, {
            "ban": ban,
            "reason": reason,
            "banned_at": self.now()
        })

    def add_exp(self, number, exp):
        try:
            user = User.objects.raw({"number": number}).first()
            user.exp += exp
            user.save()
        except DoesNotExist:
            self._update_or_create_user(number, {"exp": exp})

    def set_user_icon(self, number, icon_url):
        self._update_or_create_user(number, {"icon": icon_url})

    def set_user_bio(self, number, bio):
        self._update_or_create_user(number, {"bio": bio})

    def set_user_username(self, number, username):
        self._update_or_create_user(number, {"username": username})

    def set_group_events(self, number, events_status):
        self._update_or_create_group(number, {"events": events_status})

    def set_group_mod(self, number, mod_status):
        self._update_or_create_group(number, {"mod": mod_status})

    def get_user_by_number(self, number):
        try:
            return User.objects.raw({"number": number}).first()
        except DoesNotExist:
            self._update_or_create_user(number, {})
            return DynamicConfig({
                "number": number,
                "exp": 0,
                "ban": False
            })

    def get_group_by_number(self, number):
        try:
            return Group.objects.raw({"number": number}).first()
        except DoesNotExist:
            self._update_or_create_group(number, {})
            return DynamicConfig({
                "number": number,
                "mod": False,
                "events": False
            })

    def enable_command(self, config, reason, enable):
        try:
            command = Command.objects.raw({"name": config.name}).first()
            command.aliases = getattr(config, "aliases", [])
            command.reason = reason
            command.enable = enable
            command.created_at = self.now()
            command.save()
        except DoesNotExist:
            Command(
                name=config.name,
                aliases=getattr(config, "aliases", []),
                reason=reason,
                enable=enable,
                created_at=self.now()
            ).save()

    def get_cmd_info(self, name):
        try:
            return Command.objects.raw({"name": name}).first()
        except DoesNotExist:
            Command(name=name).save()
            return DynamicConfig({
                "name": name,
                "aliases": [],
                "reason": "",
                "enable": True
            })
