from datetime import datetime
from zoneinfo import ZoneInfo
from pymodm import connect
from pymodm.errors import DoesNotExist
from Models import User, Group, Command
from utils import DynamicConfig


class Database(
    Command,
    Group,
    User
):
    def __init__(self, uri):
        connect(uri)

    def update_user_ban(self, number, ban, reason):
        try:
            user = User.objects.raw({"number": number}).first()
            user.ban = ban
            user.reason = reason
            user.banned_at = datetime.now(ZoneInfo("Asia/Kolkata"))
            user.save()
        except DoesNotExist:
            User(
                number=number,
                ban=ban,
                reason=reason,
                banned_at=datetime.now(ZoneInfo("Asia/Kolkata")),
                created_at=datetime.now(ZoneInfo("Asia/Kolkata"))
            ).save()

    def add_exp(self, number, exp):
        try:
            user = User.objects.raw({"number": number}).first()
            user.exp += exp
            user.save()
        except DoesNotExist:
            User(
                number=number,
                exp=exp,
                created_at=datetime.now(ZoneInfo("Asia/Kolkata"))
            ).save()

    def set_group_events(self, number, events_status):
        try:
            group = Group.objects.raw({"number": number}).first()
            group.events = events_status
            group.save()
        except DoesNotExist:
            Group(
                number=number,
                events=events_status,
                created_at=datetime.now(ZoneInfo("Asia/Kolkata"))
            ).save()

    def set_group_mod(self, number, mod_status):
        try:
            group = Group.objects.raw({"number": number}).first()
            group.mod = mod_status
            group.save()
        except DoesNotExist:
            Group(
                number=number,
                mod=mod_status,
                created_at=datetime.now(ZoneInfo("Asia/Kolkata"))
            ).save()

    def set_user_icon(self, number, icon_url):
        try:
            user = User.objects.raw({"number": number}).first()
            user.icon = icon_url
            user.save()
        except DoesNotExist:
            User(
                number=number,
                icon=icon_url,
                created_at=datetime.now(ZoneInfo("Asia/Kolkata"))
            ).save()

    def set_user_bio(self, number, bio):
        try:
            user = User.objects.raw({"number": number}).first()
            user.bio = bio
            user.save()
        except DoesNotExist:
            User(
                number=number,
                bio=bio,
                created_at=datetime.now(ZoneInfo("Asia/Kolkata"))
            ).save()

    def set_user_username(self, number, username):
        try:
            user = User.objects.raw({"number": number}).first()
            user.username = username
            user.save()
        except DoesNotExist:
            User(
                number=number,
                username=username,
                created_at=datetime.now(ZoneInfo("Asia/Kolkata"))
            ).save()

    def get_user_by_number(self, number):
        try:
            user = User.objects.raw({"number": number}).first()
            return user
        except DoesNotExist:
            User(
                number=number,
                created_at=datetime.now(ZoneInfo("Asia/Kolkata"))
            ).save()
            return DynamicConfig({
                "number": number,
                "exp": 0,
                "ban": False
            })

    def get_group_by_number(self, number):
        try:
            group = Group.objects.raw({"number": number}).first()
            return group
        except DoesNotExist:
            Group(
                number=number
            ).save()
            return DynamicConfig({
                "number": number,
                "mod": False,
                "events": False
            })

    def enable_command(self, config, reason, enable):
        try:
            command = Command.objects.raw({"name": config.name}).first()
            command.name = config.name
            command.aliases = config.aliases if hasattr(
                config, "aliases") else []
            command.reason = reason
            command.enable = enable
            command.created_at = datetime.now(ZoneInfo("Asia/Kolkata"))
            command.save()
        except DoesNotExist:
            Command(
                name=config.name,
                aliases=config.aliases if hasattr(
                    config, "aliases") else [],
                reason=reason,
                enable=enable,
                created_at=datetime.now(ZoneInfo("Asia/Kolkata"))
            ).save()

    def get_cmd_info(self, name):
        try:
            command = Command.objects.raw({"name": name}).first()
            return command
        except DoesNotExist:
            Command(
                name=name
            ).save()
            return DynamicConfig({
                "name": name,
                "aliases": [],
                "reason": "",
                "enable": True
            })
