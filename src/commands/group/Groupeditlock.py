from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(client, handler, {
            'command': 'groupeditlock',
            'category': 'group',
            'description': {
                'content': 'Toggle group edit lock (only admins can edit).',
                'usage': '<on/off>'
            },
            'group': True,
            'admin': True,
            'exp': 2
        })

    def exec(self, M: MessageClass, contex):
        try:
            if not contex.args:
                return self.client.reply_message("⚠️ Please specify `on` or `off`.\nExample: `.groupeditlock on`", M)

            value = contex.args[0].lower()
            if value not in ['on', 'off']:
                return self.client.reply_message("❌ Invalid option. Use `on` or `off`.", M)

            locked = value == 'on'
            self.client.set_group_locked(M.gcjid, locked)

            self.client.reply_message(
                f"🔒 Group editing is now *{'locked' if locked else 'unlocked'}*.", M
            )

        except Exception as e:
            self.client.reply_message("❗ An error occurred while updating group lock.", M)
            self.client.log.error(f"[groupeditlock] {e}")
