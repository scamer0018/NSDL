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
from Structures.Message import Message

sys.path.insert(0, os.getcwd())

client = Client("db.sqlite3", "db.sqlite3", "#", "www.google.com")

client.log.setLevel(logging.INFO)

@client.event(ConnectedEv)
def on_connected(_: Client, __: ConnectedEv):
    client.log.info("⚡ Connected")

@client.event(JoinedGroupEv)
def on_joined(client: Client, data: JoinedGroupEv):
    client.send_message(data.GroupInfo.JID, f"Thanks for add me in {data.GroupInfo.GroupName.Name}!!")


@client.event(ReceiptEv)
def on_receipt(_: Client, receipt: ReceiptEv):
    client.log.debug(receipt)


@client.event(CallOfferEv)
def on_call(_: Client, call: CallOfferEv):
    client.log.debug(call)


@client.event(MessageEv)
def on_message(client: Client, message: MessageEv):
    handler(client, Message(client, message).build())

def handler(client: Client, M: Message):
    match M.content:
        case "ping":
            client.reply_message("Pong", M.raw())


@client.event(PairStatusEv)
def PairStatusMessage(_: Client, message: PairStatusEv):
    client.log.info(f"logged as {message.ID.User}")


client.connect()