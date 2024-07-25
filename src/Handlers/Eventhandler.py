from neonize.events import (
    GroupInfoEv,
    JoinedGroupEv,
    CallOfferEv,
)


class Event:

    def __init__(self, client):
        self.__client = client

    def on_call(self, event: CallOfferEv):
        jid = self.__client.build_jid(
            event.basicCallMeta.callCreator.User)
        self.__client.send_message(
            jid, "MF you have been blocked for fucking calling a bot!\nLearn to behave yourself.")
        self.__client.update_blocklist(
            jid, self.__client.BlocklistAction.BLOCK)

    def on_joined(self, event: JoinedGroupEv):
        self.__client.send_message(
            event.GroupInfo.JID, f"Thanks for adding me in {event.GroupInfo.GroupName.Name}!!")

    def on_groupevent(self, event: GroupInfoEv):
        if event.Leave:
            self.__client.send_message(
                event.JID, f"@{event.Leave[0].User} Left the chat")
        elif event.Join:
            self.__client.send_message(
                event.JID, f"@{event.Join[0].User} Joined the chat")
        elif event.Promote:
            self.__client.send_message(
                event.JID, f"@{event.Promote[0].User} Got promoted by @{event.Sender.User}")
        elif event.Demote:
            self.__client.send_message(
                event.JID, f"@{event.Demote[0].User} Got demoted by @{event.Sender.User}")
        elif event.Announce:
            self.__client.send_message(
                event.JID, f"@{event.Sender.User} Turned Announcement: {event.Announce.IsAnnounce}")
