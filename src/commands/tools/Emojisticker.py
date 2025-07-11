import regex as re
from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(client, handler, {
            "command": "emojisticker",
            "category": "fun",
            "description": {
                "content": "Send an emoji as a sticker.",
                "usage": "<emoji>"
            },
            "aliases": ["estick"],
            "exp": 1
        })

    def is_emoji(self, s: str) -> bool:
        return bool(re.fullmatch(r"\p{Emoji}", s))

    def exec(self, M: MessageClass, contex):
        emoji = (contex.text or "").strip()

        if not emoji:
            return self.client.reply_message("❗ Please provide an emoji.\n\nExample: `🙂`", M)

        if not self.is_emoji(emoji):
            return self.client.reply_message("🚫 That doesn't look like a valid emoji.", M)

        try:
            url = f"https://www.emoji.family/api/emojis/{emoji}/noto/png/287"
            buffer = self.client.utils.fetch_buffer(url)
            self.client.send_sticker(M.gcjid, buffer, quoted=M, name="Emoji", packname="EmojiSticker")
        except Exception as e:
            self.client.reply_message("⚠️ Failed to send emoji as sticker. Try another one.", M)
            self.client.log.error(f"[EmojiSticker] Error: {e}")
