from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(client, handler, {
            'command': 'hi',
            'category': 'core',
            'description': {
                'content': 'Say hello to the bot'
            },
            'exp': 1
        })

    def exec(self, M: Message, contex):
        exp = self.client.db.get_user_by_jid(
            M.sender.jid).exp if self.client.db.get_user_by_jid(M.sender.jid) else 0
        self.client.reply_message(
            f"Hey @{M.sender.jid} your exp: {exp}", M)
