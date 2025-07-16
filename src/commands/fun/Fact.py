import requests
from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "fact",
                "category": "fun",
                "aliases": ["randomfact"],
                "description": {"content": "Get a random fun fact."},
                "exp": 2,
            },
        )

    def exec(self, M: MessageClass, contex):
        try:
            data = self.client.utils.fetch("https://nekos.life/api/v2/fact")
            fact = data.get("fact", "No fact found.")

            reply = f"📚 *Did you know?*\n\n{fact}"
            self.client.reply_message(reply, M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ Failed to fetch a fun fact. Try again later.", M
            )
            self.client.log.error(f"[FactError] {e}")
