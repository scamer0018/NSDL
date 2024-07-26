import datetime
from pymodm import connect
from Models.Command import Command
from Models.Group import Group
from pymodm.errors import DoesNotExist
from Models.User import User


class Database(
    Command,
    Group,
    User
):
    def __init__(self, uri):
        connect(uri)

    def update_user_ban(self, jid, ban, reason):
        try:
            user = User.objects.raw({"jid": jid}).first()
            user.ban = ban
            user.reason = reason
            user.banned_at = datetime.datetime.now()
            user.save()
        except DoesNotExist:
            User(
                jid=jid,
                ban=ban,
                reason=reason,
                banned_at=datetime.datetime.now(),
                created_at=datetime.datetime.now()
            ).save()

    def add_exp(self, jid, exp):
        try:
            user = User.objects.raw({"jid": jid}).first()
            user.exp += exp
            user.save()
        except DoesNotExist:
            User(
                jid=jid,
                exp=exp,
                created_at=datetime.datetime.now()
            ).save()

    def set_group_events(self, jid, events_status):
        try:
            group = Group.objects.raw({"jid": jid}).first()
            group.events = events_status
            group.save()
        except DoesNotExist:
            Group(
                jid=jid,
                events=events_status,
                created_at=datetime.datetime.now()
            ).save()

    def set_group_mod(self, jid, mod_status):
        try:
            group = Group.objects.raw({"jid": jid}).first()
            group.mod = mod_status
            group.save()
        except DoesNotExist:
            Group(
                jid=jid,
                mod=mod_status,
                created_at=datetime.datetime.now()
            ).save()

    def set_user_icon(self, jid, icon_url):
        try:
            user = User.objects.raw({"jid": jid}).first()
            user.icon = icon_url
            user.save()
        except DoesNotExist:
            User(
                jid=jid,
                icon=icon_url,
                created_at=datetime.datetime.now()
            ).save()

    def set_user_bio(self, jid, bio):
        try:
            user = User.objects.raw({"jid": jid}).first()
            user.bio = bio
            user.save()
        except DoesNotExist:
            User(
                jid=jid,
                bio=bio,
                created_at=datetime.datetime.now()
            ).save()

    def set_user_username(self, jid, username):
        try:
            user = User.objects.raw({"jid": jid}).first()
            user.username = username
            user.save()
        except DoesNotExist:
            User(
                jid=jid,
                username=username,
                created_at=datetime.datetime.now()
            ).save()

    def get_user_by_jid(self, jid):
        try:
            user = User.objects.raw({"jid": jid}).first()
            return user
        except DoesNotExist:
            User(
                jid=jid,
                created_at=datetime.datetime.now()
            ).save()
            return None

    def get_group_by_jid(self, jid):
        try:
            group = Group.objects.raw({"jid": jid}).first()
            return group
        except DoesNotExist:
            Group(
                jid=jid
            ).save()
            return None
