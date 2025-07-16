from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "enable",
                "category": "dev",
                "aliases": [],
                "description": {
                    "content": "Globally enable a disabled command.",
                    "usage": "<command_name>",
                },
                "devOnly": True,
                "exp": 0,
            },
        )

    def exec(self, M: MessageClass, contex):
        cmd_name = contex.text.strip().lower()
        if not cmd_name:
            return self.client.reply_message(
                "⚠️ Please specify a command to enable.", M
            )

        cmd = self.handler.commands.get(cmd_name) or next(
            (
                c
                for c in self.handler.commands.values()
                if cmd_name in getattr(c.config, "aliases", [])
            ),
            None,
        )

        if not cmd:
            return self.__client.reply_message(
                f"❌ *Unknown command:* {cmd_name}",
                M,
            )

        info = self.client.db.get_cmd_info(cmd.config.command)

        if info.enable:
            return self.client.reply_message(
                f"✅ *{cmd.config.command}* is already enabled.", M
            )

        self.client.db.enable_command(
            cmd.config.command, reason="Yes", enable=True
        )
        self.client.reply_message(
            f"🔓 Command *{cmd.config.command}* has been *enabled* globally.", M
        )
