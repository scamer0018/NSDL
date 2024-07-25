import datetime
from pymodm import connect
from Models.Command import Command
from Models.Group import Group
from Models.User import User


class Database(
    Command,
    Group,
    User
):
    def __init__(self, uri):
        connect(uri)

    def update_user_ban(self, jid, ban, reason):
        if User.objects.raw({jid}).count() > 0:
            User(
                jid,
                ban,
                reason,
                banned_at=datetime.now(),
                created_at=datetime.now()
            )

        else:
            User.objects.raw({jid}).update({
                "$set": {
                    "ban": ban,
                    "reason": reason,
                    "banned_at": datetime.now()
                }
            })

    def add_exp(self, jid, exp):
        if User.objects.raw({jid}).count() > 0:
            User(
                jid,
                exp,
                created_at=datetime.now()
            )

        else:
            User.objects.raw({jid}).update({
                "$inc": {
                    "exp": exp
                }
            })
