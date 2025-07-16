from libs import BaseCommand, MessageClass


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "grouplink",
                "aliases": ["link"],
                "category": "group",
                "description": {
                    "content": "Sends you the current group’s invite link"
                },
                "exp": 1,
                "group": True,
            },
        )

    def exec(self, M: MessageClass, _):
        link = self.client.get_group_invite_link(M.gcjid)
        self.client.reply_message(f"*{link}*", M)
