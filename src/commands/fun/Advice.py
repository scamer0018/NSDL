from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "advice",
                "category": "fun",
                "aliases": ["tip", "lifeadvice"],
                "description": {"content": "Get a random life advice."},
                "exp": 2,
            },
        )

    def exec(self, M: MessageClass, contex):
        try:
            res = self.client.utils.fetch("https://api.adviceslip.com/advice")
            advice = res["slip"]["advice"]

            msg = f"💡 *Advice of the Day:*\n\n_{advice}_"
            self.client.reply_message(msg, M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ Couldn’t fetch any advice right now. Try again later.", M
            )
            self.client.log.error(f"[AdviceError] {e}")
