from Structures.Client import Client
from neonize.events import MessageEv


class Message:

    urls = []

    numbers = []

    mentioned = []

    def __init__(self, client: Client, message: MessageEv):
        self.__M = message
        self.Info = self.__M.Info
        self.Message = self.__M.Message
        self.__client = client
        jid = self.Info.MessageSource.Sender.User
        self.sender = {
            "jid": jid,
            "username": self.__client.contact.get_contact(self.__client.build_jid(jid)).PushName
        }
        self.chat = "group" if self.Info.MessageSource.IsGroup else "dm"
        self.gcjid = self.Info.MessageSource.Chat
        self.type = self.__client.get_message_type(message)
        self.content = self.__client.extract_text(message.Message)

        if (self.Message.extendedTextMessage.contextInfo.quotedMessage.extendedTextMessage.contextInfo.mentionedJID):
            for mention in self.Message.extendedTextMessage.contextInfo.quotedMessage.extendedTextMessage.contextInfo.mentionedJID:
                self.mentioned.append({
                    "jid": self.__client.build_jid(mention).User,
                    "username": self.__client.contact.get_contact(self.__client.build_jid(mention)).PushName
                })
        elif (self.Message.extendedTextMessage.contextInfo.participant):
            self.mentioned.append({
                "jid": self.__client.build_jid(self.Message.extendedTextMessage.contextInfo.participant).User,
                "username": self.__client.contact.get_contact(self.__client.build_jid(self.Message.extendedTextMessage.contextInfo.participant)).PushName
            })

    def build(self):
        for url in self.__client.utils.get_urls(self.content):
            self.urls.append(url)

        for number in self.__client.utils.extract_numbers(self.content):
            self.numbers.append(number)

        self.group = self.__client.get_group_info(self.gcjid)
        self.isAdmin = self.sender['jid'] in self.__client.filter_admin_users(
            self.group.Participants)
        return self

    def raw(self):
        return self.__M
