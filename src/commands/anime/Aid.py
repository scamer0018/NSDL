from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "aid",
                "category": "anime",
                "aliases": ["animeid"],
                "description": {
                    "content": "Get detailed info of anime by ID.",
                    "usage": "<anime_id>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        if not contex.text or not contex.text.strip().isdigit():
            return self.client.reply_message(
                "❌ Looks like you forgot to type the anime ID.", M
            )

        anime_id = contex.text.strip()

        try:
            data = self.client.utils.fetch(
                f"https://weeb-api.vercel.app/anime?search={anime_id}"
            )

            if not data:
                return self.client.reply_message(
                    "🤔 Hmm... I couldn't find anything matching your search.",
                    M,
                )

            anime = data[0]

            message = ""
            message += f"🎬 *{anime['title']['english']}* *|* {anime['title']['romaji']}\n"
            message += f"💠 *Japanese Name:* {anime['title']['native']}\n"
            message += f"📀 *Type:* {anime['format']}\n"
            message += f"🔖 *Is Adult:* {'Yes' if anime['isAdult'] else 'No'}\n"
            message += f"📡 *Status:* {anime['status']}\n"
            message += f"🎞 *Episodes:* {anime['episodes']}\n"
            message += f"🕒 *Duration:* {anime['duration']} min per episode\n"
            message += f"🗓 *First Aired:* {anime['startDate']}\n"
            message += f"📅 *Last Aired:* {anime['endDate']}\n"
            message += f"🎨 *Genres:* {', '.join(anime['genres'])}\n"
            message += f"🏢 *Studios:* {anime['studios']}\n"
            message += f"🎥 *Trailer:* https://youtu.be/{anime['trailer']['id'] if anime.get('trailer') else 'null'}\n\n"
            message += f"📖 *Description:*\n{anime['description']}"

            image = self.client.utils.fetch_buffer(anime["imageUrl"])
            self.client.send_image(M.gcjid, image, message, M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ An error occurred while fetching anime data.", M
            )
            self.client.log.error(f"[AnimeID Error] {e}")
