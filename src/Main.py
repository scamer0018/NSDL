import logging
import os
import sys
from neonize.events import (
    ConnectedEv,
    MessageEv,
    PairStatusEv,
    ReceiptEv,
    JoinedGroupEv,
    CallOfferEv,
)
from Structures.Client import Client
from Handlers.MessageHandler import MessageHandler
from Structures.Message import Message

sys.path.insert(0, os.getcwd())

client = Client(name="db.sqlite3", uuid="db.sqlite3",
                prefix="#", uri="www.google.com")

client.log.setLevel(logging.INFO)


@client.event(ConnectedEv)
def on_connected(_: Client, __: ConnectedEv):
    client.log.info("⚡ Connected")


@client.event(JoinedGroupEv)
def on_joined(client: Client, data: JoinedGroupEv):
    client.send_message(
        data.GroupInfo.JID, f"Thanks for add me in {data.GroupInfo.GroupName.Name}!!")


@client.event(ReceiptEv)
def on_receipt(_: Client, receipt: ReceiptEv):
    client.log.debug(receipt)


@client.event(CallOfferEv)
def on_call(_: Client, call: CallOfferEv):
    client.log.debug(call)


c = MessageHandler(client=client)
c.load_classes("src/Commands")


@client.event(MessageEv)
def on_message(client: Client, message: MessageEv):
    c.handler(Message(client, message).build())


def handler(client: Client, M: Message):
    match M.content:
        case "ping":
            client.reply_message("Pong", M)


@client.event(PairStatusEv)
def PairStatusMessage(_: Client, message: PairStatusEv):
    client.log.info(f"logged as {message.ID.User}")


client.connect()
