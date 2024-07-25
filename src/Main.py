import logging
import os
import sys
from neonize.events import (
    ConnectedEv,
    MessageEv,
    PairStatusEv,
    GroupInfoEv,
    JoinedGroupEv,
    CallOfferEv,
)
from Config import get_config
from Handlers.Eventhandler import Event
from Structures.Client import Client
from Handlers.MessageHandler import MessageHandler
from Structures.Message import Message

sys.path.insert(0, os.getcwd())

config = get_config()
client = Client(uuid="db.sqlite3", config=config)
instance = MessageHandler(client)
event_instance = Event(client)

client.log.setLevel(logging.INFO)


@client.event(ConnectedEv)
def on_connected(_: Client, __: ConnectedEv):
    instance.load_commands("src/Commands")
    client.log.info("⚡ Connected")


@client.event(JoinedGroupEv)
def on_joined(_: Client, event: JoinedGroupEv): event_instance.on_joined(event)


@client.event(CallOfferEv)
def on_call(_: Client, call: CallOfferEv): event_instance.on_call(call)


@client.event(GroupInfoEv)
def on_groupevent(
    _: Client, event: GroupInfoEv): event_instance.on_groupevent(event)


@client.event(MessageEv)
def on_message(client: Client, message: MessageEv): instance.handler(
    Message(client, message).build())


@client.event(PairStatusEv)
def PairStatusMessage(_: Client, message: PairStatusEv):
    client.log.info(f"logged as {message.ID.User}")


client.connect()
