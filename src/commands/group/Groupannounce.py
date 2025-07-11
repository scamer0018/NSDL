from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(client, handler, {
            'command': 'groupannounce',
            'category': 'group',
            'description': {
                'content': 'Toggle announcement mode (only admins can send messages).',
                'usage': '<on/off>'
            },
            'group': True,
            'admin': True,
            'exp': 2
        })

    def exec(self, M: MessageClass, contex):
        try:
            if not contex.args:
                return self.client.reply_message(
                    "⚠️ Please specify `on` or `off`.\nExample: `.groupannounce on`", M
                )

            option = contex.args[0].lower()
            if option not in ['on', 'off']:
                return self.client.reply_message("❌ Invalid option. Use `on` or `off`.", M)

            is_announce = option == 'on'
            self.client.set_group_announce(M.gcjid, is_announce)

            self.client.reply_message(
                f"📢 Group announcement mode is now *{'enabled' if is_announce else 'disabled'}*.", M
            )

        except Exception as e:
            self.client.reply_message("❗ An error occurred while toggling group announcement.", M)
            self.client.log.error(f"[groupannounce] {e}")
