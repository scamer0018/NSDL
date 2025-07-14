from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "manga",
                "category": "anime",
                "aliases": ["mang", "manhwa"],
                "description": {
                    "content": "Search for manga details.",
                    "usage": "<manga_name>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        query = contex.text.strip() if contex.text else None
        if not query:
            return self.client.reply_message(
                f"❌ Looks like you forgot to type the manga name.", M
            )

        try:
            url = f"https://weeb-api.vercel.app/manga?search={query}"
            mangas = self.client.utils.fetch(url)

            if not mangas:
                return self.client.reply_message(
                    "🤔 Hmm... I couldn't find anything matching your search. Maybe try a different name?",
                    M,
                )

            message = f"📚 *Manga Search Results* 📚\n\nHere’s what I found for *{query}* ⚡︎\n\n"

            for i, manga in enumerate(mangas):
                symbol = "🔞" if manga.get("isAdult") else "🌀"
                message += f"""*#{i+1}*
📖 *English name:* {manga['title']['english']}
🌐 *Alternative Name:* {manga['title']['romaji']}
📌 *Status:* {manga['status']}
⚠️ *Is Adult:* {manga['isAdult']} {symbol}
🔎 *More Info:* {self.client.config.prefix}mid {manga['id']}\n\n"""

            self.client.reply_message(message.strip(), M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ Failed to fetch manga info. Please try again later.", M
            )
            self.client.log.error(f"[MangaSearchError] {e}")
