import random
from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "gif",
                "category": "search",
                "aliases": ["tenor", "giphy"],
                "description": {
                    "content": "Search and send a random GIF from Tenor.",
                    "usage": "<query>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        query = contex.text.strip()
        if not query:
            return self.client.reply_message(
                f"⚠️ You forgot to give a search term. Try using *{self.client.config.prefix}gif happy*.",
                M,
            )

        try:
            url = f"https://g.tenor.com/v1/search?q={query}&key=LIVDSRZULELA&limit=100"
            data = self.client.utils.fetch(url)

            results = data.get("results", [])
            if not results:
                return self.client.reply_message(
                    f"😕 No GIFs found for *{query}*.", M
                )

            gif = self.client.utils.get_random_item(results)
            media = gif = self.client.utils.get_random_item(gif["media"])
            gif_url = media["mp4"]["url"]
            title = gif.get("title") or f"A random *{query}* GIF"

            media_buffer = self.client.utils.fetch_buffer(gif_url)

            self.client.send_video(
                M.gcjid, media_buffer, f"🎬 {title}", M, gifplayback=True
            )

        except Exception as e:
            self.client.reply_message(
                "⚠️ Couldn't fetch the GIF. Please try again later.", M
            )
            self.client.log.error(f"[TenorGIFError] {e}")
