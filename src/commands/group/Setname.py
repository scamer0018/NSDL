from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "setname",
                "category": "group",
                "description": {
                    "content": "Change the group subject/name.",
                    "usage": "<new_name>",
                },
                "group": True,
                "admin": True,
                "exp": 2,
            },
        )

    def exec(self, M: MessageClass, contex):
        try:
            if not contex.text:
                return self.client.reply_message(
                    f"✏️ Please provide the new group name.\nExample: `{self.client.config.prefix}setname Cool Group`",
                    M,
                )

            new_name = contex.text.strip()

            if len(new_name) > 100:
                return self.client.reply_message(
                    "🚫 Group name must be under 100 characters.", M
                )

            self.client.set_group_name(M.gcjid, new_name)
            self.client.reply_message(
                f"✅ Group name changed to *{new_name}*.", M
            )

        except Exception as e:
            self.client.reply_message(
                "❗ An error occurred while changing the group name.", M
            )
            self.client.log.error(f"[setname] {e}")
