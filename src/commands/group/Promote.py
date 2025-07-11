from libs import BaseCommand, MessageClass
from neonize.utils import ParticipantChange

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(client, handler, {
            'command': 'promote',
            'category': 'group',
            'description': {
                'content': 'Promote a member to admin.',
                'usage': '<@mention> | <quote>'
            },
            'admin': True,
            'group': True,
            'exp': 2
        })

    def exec(self, M: MessageClass, _):
        try:
            targets = M.mentioned or ([M.quoted_user] if M.quoted_user else [])
            if not targets:
                return self.client.reply_message("👤 Please *mention or quote* to a user to promote.", M)

            self.client.update_group_participants(
                M.gcjid,
                [self.client.build_jid(u.number) for u in targets],
                ParticipantChange.PROMOTE
            )

            self.client.reply_message("✅ User(s) promoted to *admin*.", M)

        except Exception as e:
            self.client.reply_message("❗ Failed to promote user(s).", M)
            self.client.log.error(f"[promote] {e}")
