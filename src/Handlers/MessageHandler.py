import os
import importlib.util
from Structures.Client import Client
from Structures.Message import Message


class MessageHandler:

    commands = {}

    def __init__(self, client: Client):
        self.__client = client

    def handler(self, M: Message):
        contex = self.parse_args(M.content)
        isCommand = M.content.startswith(self.__client.prifix)
        if not isCommand:
            return
        cmd = self.commands[contex.get("cmd")] or None
        if not cmd:
            return self.__client.reply_message("Command does not avilable!!")
        cmd.exec(M, contex)

    def load_classes(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith('.py'):
                module_name = filename[:-3]
                file_path = os.path.join(folder_path, filename)

                spec = importlib.util.spec_from_file_location(
                    module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                class_ = getattr(module, "Command")
                instance = class_(self.__client, self)
                self.commands[instance.config["command"]] = instance
                aliases = instance.config["aliases"] if hasattr(
                    instance.config, "aliases") else []

                for alias in aliases:
                    self.commands[alias] = instance

    def parse_args(self, raw):
        args = raw.split(' ')
        cmd = args.pop(0).lower()[
            len(self.__client.prifix):] if args else ''
        text = ' '.join(args)
        flags = {}

        for arg in args:
            if arg.startswith('--'):
                key, value = arg[2:].split('=', 1)
                flags[key] = value
            elif arg.startswith('-'):
                flags[arg] = ''
        return {
            'cmd': cmd,
            'text': text,
            'flags': flags,
            'args': args,
            'raw': raw
        }
