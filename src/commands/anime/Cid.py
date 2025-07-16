from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "cid",
                "category": "anime",
                "aliases": ["charid", "characterid"],
                "description": {
                    "content": "Get anime character info by ID.",
                    "usage": "<character_id>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        query = contex.text.strip() if contex.text else None

        if not query or not query.isdigit():
            return self.client.reply_message(
                "❌ Looks like you forgot to type a valid *character ID*.", M
            )

        try:
            url = f"https://weeb-api.vercel.app/character?search={query}"
            result = self.client.utils.fetch(url)
            if not result:
                return self.client.reply_message(
                    "🤔 Hmm... I couldn't find anything matching that character ID.",
                    M,
                )

            character = result[0]
            gender = character.get("gender", "Unknown")
            symbol = (
                "🚺"
                if gender == "Female"
                else "🚹" if gender == "Male" else "🚻"
            )

            message = f"""👤 *Name:* {character['name']['full']}
💠 *Native:* {character['name']['native']}
🆔 *ID:* {character['id']}
🗓 *Age:* {character.get('age', 'Unknown')}
🔗 *Gender:* {gender} {symbol}
🔗 *AniList:* {character.get('siteUrl', 'N/A')}

📝 *Description:*
{character.get('description', 'No description available.')}
""".strip()

            image = self.client.utils.fetch_buffer(character["imageUrl"])
            self.client.send_image(M.gcjid, image, message, M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ Failed to fetch character info. Please try again later.", M
            )
            self.client.log.error(f"[CharacterIDError] {e}")
