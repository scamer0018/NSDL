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
                "description": {"content": "Display user's information."},
                "exp": 2,
            },
        )

    def exec(self, M: MessageClass, _):
        # Determine target user (self, quoted, or mentioned)
        target = M.quoted_user or (M.mentioned[0] if M.mentioned else M.sender)
        jid = self.client.build_jid(target.number)
        username = target.username

        # Get user data from DB
        user = self.client.db.get_user_by_number(jid.User)
        rank = get_rank(user.exp)

        # Get user bio
        try:
            bio = self.client.get_user_info(jid)[0].UserInfo.Status
        except Exception:
            bio = "None"

        # Get profile picture URL
        try:
            pfp_url = self.client.get_profile_picture(jid).URL
        except Exception:
            pfp_url = "https://www.pngall.com/wp-content/uploads/5/Profile-PNG-File.png"

        # Ban info if banned
        ban_info = ""
        if user.ban:
            ban_info = (
                f"\n\n📝 *Reason:* {user.reason}"
                f"\n⏰ *Banned At:* {user.banned_at.strftime('%d %b %Y, %I:%M %p')}"
            )

        # Final message
        message = (
            f"👤 *User Profile* 👤\n\n"
            f"📛 *Username:* {username}\n"
            f"📱 *Number:* {jid.User}\n"
            f"💬 *Bio:* {bio}\n"
            f"🎖️ *Rank:* {rank['name']} {rank['data']['emoji']}\n"
            f"✨ *EXP:* {user.exp}\n"
            f"📅 *Joined On:* {user.created_at.strftime('%d %b %Y, %I:%M %p')}\n\n"
            f"{'🚫 *Status:* Banned' + ban_info if user.ban else '✅ *Status:* Active'}\n\n"
            f"(Use *{self.client.config.prefix}rank* to see ranks and more user info.)"
        )

        # Send profile image with caption
        image_msg = self.client.build_image_message(
            self.client.utils.fetch_buffer(pfp_url), caption=message, quoted=M
        )
        self.client.send_message(M.gcjid, message=image_msg)