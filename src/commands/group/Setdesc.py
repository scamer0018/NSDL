from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "setdesc",
                "category": "group",
                "description": {
                    "content": "Change the group description.",
                    "usage": "<new_description>",
                },
                "group": True,
                "admin": True,
                "exp": 2,
            },
        )

    def exec(self, M: MessageClass, contex):
        try:
            desc = self.client.extract_text(M.quoted) or contex.text
            if not desc:
                return self.client.reply_message(
                    f"📝 Please provide the new group description — Example: *{self.client.config.prefix}settopic Welcome to the Void Group!*",
                    M,
                )

            new_topic = desc.strip()

            if len(new_topic) > 500:
                return self.client.reply_message(
                    "🚫 Description must be under 500 characters.", M
                )

            self.client.set_group_topic(M.gcjid, new_topic)
            self.client.reply_message(
                "✅ Group description updated successfully.", M
            )

        except Exception as e:
            self.client.reply_message(
                "❗ An error occurred while updating the group description.", M
            )
            self.client.log.error(f"[settopic] {e}")
