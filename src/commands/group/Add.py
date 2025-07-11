from libs import BaseCommand, MessageClass
from neonize.utils import ParticipantChange

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(client, handler, {
            'command': 'add',
            'category': 'group',
            'description': {
                'content': 'Add a user to the group.',
                'usage': '<@mention> | <quote>'
            },
            'admin': True,
            'group': True,
            'exp': 2
        })

    def exec(self, M: MessageClass, contex):
        try:
            numbers = self.client.utils.extract_numbers(contex.text)
            if not numbers:
                return self.client.reply_message("➕ Please provide valid *number(s)* to add.", M)

            jids = [self.client.build_jid(str(n)) for n in numbers]
            self.client.update_group_participants(M.gcjid, jids, ParticipantChange.ADD)

            self.client.reply_message("✅ User(s) added to the group.", M)

        except Exception as e:
            self.client.reply_message("❗ Failed to add user(s).", M)
            self.client.log.error(f"[add] {e}")
