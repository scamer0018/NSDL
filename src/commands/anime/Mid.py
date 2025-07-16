from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "mid",
                "category": "anime",
                "aliases": ["mangaid"],
                "description": {
                    "content": "Get detailed info of a manga using its ID.",
                    "usage": "<manga_id>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        query = contex.text.strip().split() if contex.text else []
        if not query or not query[0].isdigit():
            return self.client.reply_message(
                "❌ Looks like you forgot to type the *manga ID*.", M
            )

        manga_id = query[0]

        try:
            url = f"https://weeb-api.vercel.app/manga?search={manga_id}"
            results = self.client.utils.fetch(url)

            if not results:
                return self.client.reply_message(
                    "🤔 Hmm... I couldn't find anything matching that manga ID.",
                    M,
                )

            manga = results[0]

            title = manga["title"]
            message = ""
            message += f"📚 *{title['english']}* | *{title['romaji']}*\n"
            message += f"🈶 *Japanese:* {title['native']}\n"
            message += f"📦 *Type:* {manga['format']}\n"
            message += f"⚠️ *Is Adult:* {'Yes' if manga['isAdult'] else 'No'}\n"
            message += f"📌 *Status:* {manga['status']}\n"
            message += f"📖 *Chapters:* {manga['chapters']}\n"
            message += f"📦 *Volumes:* {manga['volumes']}\n"
            message += f"⏳ *First Aired:* {manga['startDate']}\n"
            message += f"🕰️ *Last Aired:* {manga['endDate']}\n"
            message += f"🎭 *Genres:* {', '.join(manga['genres'])}\n"
            message += f"🎬 *Trailer:* https://youtu.be/{manga['trailer']['id'] if manga.get('trailer') else 'null'}\n\n"
            message += f"📄 *Description:*\n_{manga['description']}_"

            image = self.client.utils.fetch_buffer(manga["coverImage"])
            self.client.send_image(M.gcjid, image, message.strip(), M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ Failed to fetch manga info. Please try again later.", M
            )
            self.client.log.error(f"[MangaDetailError] {e}")
