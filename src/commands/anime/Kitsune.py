from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "kitsune",
                "category": "anime",
                "aliases": ["foxgirl"],
                "description": {"content": "Send a cute kitsune image."},
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, _):
        try:
            res = self.client.utils.fetch("https://nekos.best/api/v2/kitsune")
            results = res.get("results", [])

            if not results:
                return self.client.reply_message(
                    "❌ Couldn't find a kitsune image right now. Try again later.",
                    M,
                )

            kitsune = results[0]
            image = self.client.utils.fetch_buffer(kitsune["url"])

            message = f"""🦊 *Here's a Kitsune for you!*
🎨 *Artist:* {kitsune['artist_name']}
🔗 *Source:* {kitsune['source_url']}
👤 *Artist Profile:* {kitsune['artist_href']}
🖼 *Image:* {kitsune['url']}"""

            self.client.send_image(M.gcjid, image, message.strip(), M)

        except Exception as e:
            self.client.reply_message("⚠️ Failed to fetch kitsune image.", M)
            self.client.log.error(f"[KitsuneError] {e}")
