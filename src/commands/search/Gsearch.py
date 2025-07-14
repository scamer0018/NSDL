from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "gsearch",
                "category": "search",
                "aliases": ["google", "search"],
                "description": {
                    "content": "Search Google and get the top 10 results.",
                    "usage": "<query>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        query = contex.text.strip()
        if not query:
            return self.client.reply_message(
                f"🔍 You forgot to type a search query! Try: *{self.client.config.prefix}gsearch how to learn python*",
                M,
            )

        API_KEY = "AIzaSyDMbI3nvmQUrfjoCJYLS69Lej1hSXQjnWI"
        CX = "baf9bdb0c631236e5"
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}&num=10"

        try:
            data = self.client.utils.fetch(url)
            items = data.get("items", [])

            if not items:
                return self.client.reply_message(
                    f"❌ No results found for *{query}*.", M
                )

            msg = f"🔎 *Top 10 Google Search Results for:* _{query}_\n\n"
            for i, item in enumerate(items, 1):
                title = item.get("title", "No Title")
                link = item.get("link", "")
                snippet = item.get("snippet", "").strip()
                msg += f"*{i}. {title}*\n🔗 {link}\n📝 {snippet}\n\n"

            self.client.reply_message(msg.strip(), M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ Failed to fetch Google results. Please try again later.",
                M,
            )
            self.client.log.error(f"[GoogleSearchError] {e}")
