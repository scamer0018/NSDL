from libs import Void
from utils import DynamicConfig

class BaseCommand:
    def __init__(self, client: Void, handler, config):
        self.client = client
        self.handler = handler
        self.config = DynamicConfig(config)

    def exec(self, M, arg):
        self.client.error("Exec Function must be decleared")
