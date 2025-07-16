from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "disable",
                "category": "dev",
                "aliases": [],
                "description": {
                    "content": "Globally disable a command with optional reason.",
                    "usage": "<command_name> | <reason>",
                },
                "devOnly": True,
                "exp": 0,
            },
        )

    def exec(self, M: MessageClass, contex):
        text = contex.text.strip()
        if not text:
            return self.client.reply_message(
                f"⚠️ Please specify a command to disable. Use like {self.client.config.prefix}disable anime|Too much load",
                M,
            )

        parts = text.split("|", 1)
        cmd_name = parts[0].strip().lower()
        reason = parts[1].strip() if len(parts) > 1 else "No reason provided."

        cmd = self.handler.commands.get(cmd_name) or next(
            (
                c
                for c in self.handler.commands.values()
                if cmd_name in getattr(c.config, "aliases", [])
            ),
            None,
        )

        if not cmd:
            return self.client.reply_message(
                f"❌ *Unknown command:* {cmd_name}", M
            )

        if cmd.config.command in ["enable", "disable", "ban", "unban"]:
            return self.client.reply_message(
                f"🚫 You cannot disable core moderation commands.", M
            )

        info = self.client.db.get_cmd_info(cmd.config.command)

        if not info.enable:
            return self.client.reply_message(
                f"❌ *{cmd.config.command}* is already disabled.", M
            )

        self.client.db.enable_command(
            cmd.config.command, reason=reason, enable=False
        )

        self.client.reply_message(
            f"🔒 Command *{cmd.config.command}* has been *disabled* globally.\n📌 *Reason:* {reason}",
            M,
        )
