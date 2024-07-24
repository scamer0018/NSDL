from Structures.Client import Client
from Helpers.DynamicConfig import DynamicConfig


class BaseCommand:
    def __init__(self, client: Client, handler, config):
        self.client = client
        self.handler = handler
        self.config = DynamicConfig(config)

    def exec(msg, arg):
        raise "Exec Function must be decleared"
