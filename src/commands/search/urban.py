from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "urban",
                "category": "search",
                "aliases": ["ud", "urbandictionary"],
                "description": {
                    "content": "Get the Urban Dictionary definition for a term.",
                    "usage": "<term>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        prefix = self.client.config.prefix
        term = contex.text.strip() if contex.text else None

        if not term:
            return self.client.reply_message(
                f"⚠️ Oops! You didn’t define a term — Use `{prefix}urban hello` to look up words.",
                M,
            )

        url = f"https://api.urbandictionary.com/v0/define?term={term}"

        try:
            data = self.client.utils.fetch(url)

            if not data.get("list"):
                return self.client.reply_message(
                    f"📚 No definitions found for *{term}*.", M
                )

            entry = data["list"][0]
            word = entry.get("word", term)
            definition = (
                entry.get("definition", "")
                .replace("[", "")
                .replace("]", "")
                .strip()
            )
            example = (
                entry.get("example", "")
                .replace("[", "")
                .replace("]", "")
                .strip()
            )
            thumbs_up = entry.get("thumbs_up", 0)
            thumbs_down = entry.get("thumbs_down", 0)

            reply = f"""📘 *{word}* (Urban Dictionary)

🔹 *Definition:*  
{definition}

📌 *Example:*  
{example or 'No example provided.'}

👍 {thumbs_up}   👎 {thumbs_down}
"""
            self.client.reply_message(reply, M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ Failed to fetch definition. Please try again later.", M
            )
            self.client.log.error(f"[UrbanError] {e}")
