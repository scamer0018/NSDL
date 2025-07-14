from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "husbu",
                "category": "anime",
                "aliases": ["husbando"],
                "description": {"content": "Send a husbando image."},
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, _):
        try:
            res = self.client.utils.fetch("https://nekos.best/api/v2/husbando")
            results = res.get("results", [])

            if not results:
                return self.client.reply_message(
                    "❌ Couldn't find a husbando image right now. Try again later.",
                    M,
                )

            husbando = results[0]
            image = self.client.utils.fetch_buffer(husbando["url"])

            message = f"""🧔 *Here's a Husbando for you!*
🎨 *Artist:* {husbando['artist_name']}
🔗 *Source:* {husbando['source_url']}
👤 *Artist Profile:* {husbando['artist_href']}
🖼 *Image:* {husbando['url']}"""

            self.client.send_image(M.gcjid, image, message.strip(), M)

        except Exception as e:
            self.client.reply_message("⚠️ Failed to fetch husbando image.", M)
            self.client.log.error(f"[HusbandoError] {e}")
