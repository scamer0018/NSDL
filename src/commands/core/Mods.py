from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(client, handler, {
            'command': 'mods',
            'category': 'core',
            'aliases': ['modlist', 'developers'],
            'description': {
                'content': 'Displays the list of bot moderators.'
            },
            'exp': 1
        })

    def exec(self, M: MessageClass, _):
        mods = self.client.config.mods 
        if not mods:
            return self.client.reply_message("⚠️ No moderators are currently assigned.", M)

        lines = []
        for number in mods:
            jid = self.client.build_jid(number)
            try:
                contact = self.client.contact.get_contact(jid)
                name = contact.PushName or "Unknown"
            except Exception:
                name = "Unknown"
            lines.append(f"• {name} (https://wa.me/{number})")

        text = "🧑‍💻 *Bot Moderators:*\n\n" + "\n".join(lines)
        self.client.reply_message(text, M)
