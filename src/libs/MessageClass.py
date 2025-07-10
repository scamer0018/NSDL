from libs import Void
from utils import DynamicConfig
from neonize.events import MessageEv


class MessageClass:

    urls = []

    quoted_user = None

    numbers = []

    mentioned = []

    def __init__(self, client: Void, message: MessageEv):
        self.__M = message
        self.Info = self.__M.Info
        self.Message = self.__M.Message
        self.__client = client
        number = self.Info.MessageSource.Sender.User
        self.sender = DynamicConfig({
            "number": number,
            "username": self.__client.contact.get_contact(self.__client.build_jid(number)).PushName
        })
        self.chat = "group" if self.Info.MessageSource.IsGroup else "dm"
        self.gcjid = self.Info.MessageSource.Chat
        self.content = self.__client.extract_text(self.Message)
        self.quoted = self.Message.extendedTextMessage.contextInfo.quotedMessage
        self.context_info = self.Message.extendedTextMessage.contextInfo

        if message.Message.extendedTextMessage.contextInfo.participant:
                self.quoted_user = DynamicConfig({
                    "number": message.Message.extendedTextMessage.contextInfo.participant.split("@")[0],
                    "username": self.__client.contact.get_contact(self.__client.build_jid(message.Message.extendedTextMessage.contextInfo.participant.split("@")[0])).PushName
                })

        if hasattr(self.context_info, "mentionedJID"):
            for jid in getattr(self.context_info, "mentionedJID", []):
                number = jid.split("@")[0]
                self.mentioned.append(DynamicConfig({
                    "number": number,
                    "username": self.__client.contact.get_contact(self.__client.build_jid(number)).PushName
                }))

    def build(self):
        for url in self.__client.utils.get_urls(self.content):
            self.urls.append(url)

        for number in self.__client.utils.extract_numbers(self.content):
            self.numbers.append(number)

        if self.chat == "group":
            self.group = self.__client.get_group_info(self.gcjid)
            self.isAdminMessage = self.sender.number in self.__client.filter_admin_users(
                self.group.Participants)

        return self

    def raw(self):
        return self.__M
