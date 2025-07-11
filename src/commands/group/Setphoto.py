from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(client, handler, {
            'command': 'setphoto',
            'category': 'group',
            'description': {
                'content': 'Change the group profile picture.'
            },
            'group': True,
            'admin': True,
            'exp': 2
        })

    def exec(self, M: MessageClass, _):
        try:
            source = M.quoted or M.Message
            media_type = self.client.detect_message_type(source)

            if media_type != "IMAGE":
                return self.client.reply_message(
                    f"🖼️ Please reply to or send an image with *{self.client.config.prefix}setphoto* to update the group photo.",
                    M
                )

            image_data = self.client.download_any(source)
            self.client.set_group_photo(M.gcjid, image_data)

            self.client.reply_message("✅ Group photo updated successfully.", M)

        except Exception as e:
            self.client.reply_message("❗ An error occurred while updating the group photo.", M)
            self.client.log.error(f"[setphoto] {e}")
