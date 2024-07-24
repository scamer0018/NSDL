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
        self.client.reply_message("hey", M)
