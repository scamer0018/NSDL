from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "toggle",
                "category": "group",
                "aliases": ["tog"],
                "description": {
                    "content": "Enable or disable group features like mod or event.",
                    "usage": "<mod|event>",
                },
                "group": True,
                "admin": True,
                "exp": 0,
            },
        )

    def exec(self, M: MessageClass, contex):
        if not contex.text:
            return self.client.reply_message(
                "❌ *Missing input!*\nUse: `#toggle <mod|events>` to enable or disable group features.",
                M,
            )

        feature = contex.text.strip().lower()
        number = M.gcjid.User.split("@")[0]

        if feature not in ("mod", "events"):
            return self.client.reply_message(
                "❌ Only *mod* or *events* features can be toggled.", M
            )

        group = self.client.db.get_group_by_number(number)
        current_status = getattr(group, feature, False)
        new_status = not current_status

        if feature == "mod":
            self.client.db.set_group_mod(number, new_status)
        else:
            self.client.db.set_group_events(number, new_status)

        emoji = "✅" if new_status else "🚫"
        msg = f"{emoji} *{feature.upper()}* feature has been *{'enabled' if new_status else 'disabled'}* for this group."
        self.client.reply_message(msg, M)
