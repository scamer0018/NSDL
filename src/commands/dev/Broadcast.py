from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "broadcast",
                "aliases": ["bc"],
                "category": "dev",
                "description": {
                    "content": "Broadcast a message to all groups.",
                    "usage": "<message>",
                },
                "exp": 0,
                "devOnly": True,
            },
        )

    def exec(self, M: MessageClass, contex):
        if not contex.text:
            return self.client.reply_message(
                "⚠️ Please provide a message to broadcast.", M
            )

        text = contex.text.strip()
        sent = 0

        try:
            all_chats = self.client.get_joined_groups()
            for chat in all_chats:
                self.client.send_message(chat.JID, f"📢 *Broadcast:*\n{text}")
                sent += 1

            self.client.reply_message(
                f"✅ Broadcast sent to *{sent}* groups.", M
            )

        except Exception as e:
            self.client.reply_message("❌ Broadcast failed.", M)
            self.client.log.error(f"[BroadcastError] {e}")
