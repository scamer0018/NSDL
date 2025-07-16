from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "character",
                "category": "anime",
                "aliases": ["char", "csearch"],
                "description": {
                    "content": "Search for anime character details.",
                    "usage": "<character_name>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        query = contex.text.strip() if contex.text else None
        if not query:
            return self.client.reply_message(
                f"❌ Looks like you forgot to type the *character name*.",
                M,
            )

        try:
            url = f"https://weeb-api.vercel.app/character?search={query}"
            characters = self.client.utils.fetch(url)

            if not characters:
                return self.client.reply_message(
                    "🤔 Hmm... I couldn't find any *character* matching your search. Maybe double-check the name?",
                    M,
                )

            message = f"👤 *Character Search Results* 👤\n\nHere’s what I found for *{query}* ⚡︎\n\n"

            for i, char in enumerate(characters):
                gender = char.get("gender", "Unknown")
                symbol = (
                    "🚺"
                    if gender == "Female"
                    else "🚹" if gender == "Male" else "🚻"
                )
                message += f"""*#{i+1}*
🌀 *Full name:* {char['name']['full']}
💠 *Native name:* {char['name']['native']}
🔗 *Gender:* {gender} {symbol}
🔎 *More Info:* {self.client.config.prefix}cid {char['id']}\n\n"""

            self.client.reply_message(message.strip(), M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ Failed to fetch character data. Please try again later.", M
            )
            self.client.log.error(f"[CharacterSearchError] {e}")
