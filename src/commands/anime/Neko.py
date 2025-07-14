from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "neko",
                "category": "anime",
                "aliases": ["catgirl"],
                "description": {"content": "Send a cute neko image."},
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, _):
        try:
            res = self.client.utils.fetch("https://nekos.best/api/v2/neko")
            results = res.get("results", [])

            if not results:
                return self.client.reply_message(
                    "❌ Couldn't find a neko image right now. Try again later.",
                    M,
                )

            neko = results[0]
            image = self.client.utils.fetch_buffer(neko["url"])

            message = f"""🐾 *Here's a Neko for you!*
🎨 *Artist:* {neko['artist_name']}
🔗 *Source:* {neko['source_url']}
👤 *Artist Profile:* {neko['artist_href']}
🖼 *Image:* {neko['url']}"""

            self.client.send_image(M.gcjid, image, message.strip(), M)

        except Exception as e:
            self.client.reply_message("⚠️ Failed to fetch neko image.", M)
            self.client.log.error(f"[NekoError] {e}")
