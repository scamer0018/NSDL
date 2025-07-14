from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "waifu",
                "category": "anime",
                "aliases": ["wife"],
                "description": {"content": "Send a random waifu image."},
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, _):
        try:
            res = self.client.utils.fetch("https://nekos.best/api/v2/waifu")
            results = res.get("results", [])

            if not results:
                return self.client.reply_message(
                    "❌ Couldn't find a waifu image right now. Try again later.",
                    M,
                )

            waifu = results[0]
            image = self.client.utils.fetch_buffer(waifu["url"])

            message = f"""💖 *Here's a Waifu for you!*
🎨 *Artist:* {waifu['artist_name']}
🔗 *Source:* {waifu['source_url']}
👤 *Artist Profile:* {waifu['artist_href']}
🖼 *Image:* {waifu['url']}"""

            self.client.send_image(M.gcjid, image, message.strip(), M)

        except Exception as e:
            self.client.reply_message("⚠️ Failed to fetch waifu image.", M)
            self.client.log.error(f"[WaifuError] {e}")
