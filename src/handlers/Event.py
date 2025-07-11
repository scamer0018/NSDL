from libs import Void
from neonize.events import (
    GroupInfoEv,
    JoinedGroupEv,
    CallOfferEv,
)


class Event:
    def __init__(self, client: Void):
        self.__client = client

    def on_call(self, event: CallOfferEv):
        user_id = event.basicCallMeta.callCreator.User
        jid = self.__client.build_jid(user_id)

        self.__client.db.update_user_ban(user_id, True, "Called the bot!")
        self.__client.send_message(
            jid,
            "🚫 You have been *blocked* for calling the bot.\nPlease refrain from calling bots in the future."
        )
        self.__client.update_blocklist(jid, self.__client.BlocklistAction.BLOCK)

    def on_joined(self, event: JoinedGroupEv):
        self.__client.send_message(
            event.JID,
            f"👋 Thanks for adding me to *{event.GroupInfo.GroupName.Name}*!"
        )

    def on_groupevent(self, event: GroupInfoEv):
        group = self.__client.db.get_group_by_number(event.JID.User)

        if not group.events:
            return

        jid = event.JID

        if event.Leave and len(event.Leave) > 0:
            user = event.Leave[0].User
            self.__client.send_message(jid, f"👋 @{user} left the chat.")
        elif event.Join and len(event.Join) > 0:
            user = event.Join[0].User
            self.__client.send_message(jid, f"👤 @{user} joined the chat.")
        elif event.Promote and len(event.Promote) > 0:
            user = event.Promote[0].User
            promoter = event.Sender.User
            self.__client.send_message(jid, f"⬆️ @{user} was *promoted* by @{promoter}.")
        elif event.Demote and len(event.Demote) > 0:
            user = event.Demote[0].User
            demoter = event.Sender.User
            self.__client.send_message(jid, f"⬇️ @{user} was *demoted* by @{demoter}.")
        elif event.Announce:
            status = "enabled" if event.Announce.IsAnnounce else "disabled"
            self.__client.send_message(
                jid,
                f"📢 Announcement mode was *{status}* by @{event.Sender.User}."
            )
