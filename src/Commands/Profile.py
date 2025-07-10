from libs import BaseCommand, MessageClass
from utils import get_rank


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "whoami",
                "category": "core",
                "aliases": ["profile"],
                "description": {
                    "content": "Display user's information."
                },
                "exp": 2,
            },
        )

    def exec(self, M: MessageClass, _):
        jid = self.client.build_jid(M.sender.number)
        username = M.sender.username

        if M.quoted_user:
            jid = self.client.build_jid(M.quoted_user.number)
            username = M.quoted_user.username
        elif M.mentioned:
            jid = self.client.build_jid(M.mentioned[0].number)
            username = M.mentioned[0].username

        user = self.client.db.get_user_by_number(jid.User)
        rank = get_rank(user.exp)

        bio = ""
        try:
            bio = self.client.get_user_info(jid)[0].UserInfo.Status
        except Exception as e:
            bio = "None"

        pfp = ""
        try:
            pfp = self.client.get_profile_picture(jid).URL
        except:
            pfp = "https://www.pngall.com/wp-content/uploads/5/Profile-PNG-File.png"

        ban_info = ""
        if user.ban:
            ban_info = f"\n\n📝 *Reason:* {user.reason}\n⏰ *Banned At:* {user.banned_at.strftime('%d %b %Y, %I:%M %p')}"

        message = f"""👤 *User Profile* 👤

📛 *Username:* {username}

📱 *Number:* {jid.User}

💬 *Bio:* {bio}

🎖️ *Rank:* {rank['name']} {rank['data']['emoji']}

✨ *EXP:* {user.exp}

📅 *Joined On:* {user.created_at.strftime('%d %b %Y, %I:%M %p')}

{f'🚫 *Status:* Banned {ban_info}' if user.ban else '✅ *Status:* Active'}

(Use *{self.client.config.prefix}rank* to see ranks and more user info.)"""

        image_msg = self.client.build_image_message(
            self.client.utils.fetch_buffer(pfp), caption=message, quoted=M)
        self.client.send_message(M.gcjid, message=image_msg)
