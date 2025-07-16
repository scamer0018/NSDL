from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "anime",
                "category": "anime",
                "aliases": ["ani"],
                "description": {
                    "content": "Search for anime details.",
                    "usage": "<anime_name>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        query = contex.text.strip() if contex.text else None
        if not query:
            return self.client.reply_message(
                "❌ Looks like you forgot to type the *anime name*.", M
            )

        try:
            animes = self.client.utils.fetch(
                f"https://weeb-api.vercel.app/anime?search={query}"
            )

            if not animes:
                return self.client.reply_message(
                    "🤔 Hmm... I couldn't find anything matching your search. Maybe try a different name?",
                    M,
                )

            message = f"🎬 *Anime Search Results*\n\nHere’s what I found for *{query}* ⚡︎\n\n"

            for i, anime in enumerate(animes):
                message += f"""*#{i+1}*
🎬 *English name:* {anime['title']['english']}
💠 *Alternative name:* {anime['title']['romaji']}
📀 *Type:* {anime['format']}
📡 *Status:* {anime['status']}
🔎 *More Info:* {self.client.config.prefix}aid {anime['id']}\n\n"""

            self.client.reply_message(message.strip(), M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ Something went wrong while fetching the anime data.", M
            )
            self.client.log.error(f"[AnimeSearchError] {e}")
