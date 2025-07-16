from libs import BaseCommand, MessageClass

ANIMAL_OPTIONS = ["bird", "cat", "dog", "fox", "koala", "panda"]


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "animal",
                "aliases": ANIMAL_OPTIONS,
                "category": "fun",
                "description": {
                    "content": "Send a random image and fact of an animal.",
                    "usage": "<animal_type>",
                },
                "exp": 5,
            },
        )

    def exec(self, M: MessageClass, contex):
        cmd = contex.cmd.lower()
        query = contex.text.strip().lower() if contex.text else None

        # Determine actual animal
        animal = cmd if cmd in ANIMAL_OPTIONS else query

        if not animal or animal not in ANIMAL_OPTIONS:
            list_text = "\n- " + "\n- ".join(
                [a.capitalize() for a in ANIMAL_OPTIONS]
            )
            msg = f"🐾 *Available Animal Facts:*{list_text}\n\n🛠️ *Usage:* {self.client.config.prefix}animal <option>\nExample: {self.client.config.prefix}cat"
            return self.client.reply_message(msg, M)

        try:
            fact_data = self.client.utils.fetch(
                f"https://some-random-api.com/facts/{animal}"
            )
            img_data = self.client.utils.fetch(
                f"https://some-random-api.com/img/{animal}"
            )

            fact = fact_data.get("fact", "No fact found.")
            image_url = img_data.get("link")

            if not image_url:
                return self.client.reply_message("⚠️ Couldn’t fetch image.", M)

            buffer = self.client.utils.fetch_buffer(image_url)
            self.client.send_image(M.gcjid, buffer, f"*_{fact}_*", M)

        except Exception as e:
            self.client.reply_message("⚠️ Failed to fetch animal data.", M)
            self.client.log.error(f"[AnimalCommandError] {e}")
