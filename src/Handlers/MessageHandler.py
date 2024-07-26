import os
import importlib.util
from Structures.Client import Client
from Structures.Message import Message
from Helpers.Ranks import get_rank
from Helpers.DynamicConfig import DynamicConfig


class MessageHandler:

    commands = {}

    def __init__(self, client: Client):
        self.__client = client

    def handler(self, M: Message):
        contex = DynamicConfig(self.parse_args(M.content))
        isCommand = M.content.startswith(self.__client.config.prefix)

        chat_type = "[CMD]: " if isCommand else "[MSG]: "
        _from = M.group.GroupName.Name if M.chat == "group" else "Direct Message"
        self.__client.log.info(
            f"{chat_type} from {M.sender.username} in {_from}")

        if not isCommand:
            return

        if M.content == self.__client.config.prefix:
            return self.__client.reply_message(f"Enter a command following {self.__client.config.prefix}", M)

        cmd = self.commands[contex.cmd] if contex.cmd in self.commands.keys(
        ) else None

        user = self.client.db.get_user_by_jid(
            M.sender.jid) if self.client.db.get_user_by_jid(M.sender.jid) else DynamicConfig({
                "jid": M.sender.jid,
                "exp": 0,
                "ban": False
            })

        if not cmd:
            return self.__client.reply_message("Command does not avilable!!", M)

        if hasattr(cmd.config, "group") and M.chat == "dm":
            return self.__client.reply_message(
                "This command can only be used in groups", M)
        if hasattr(cmd.config, "admin") and not M.isAdminMessage:
            return self.__client.reply_message("Only admins are allowed to use this command", M)

        self.__client.db.add_exp(M.sender.jid, cmd.config.exp)

        new_exp = user.exp + cmd.config.exp

        # Get the old and new ranks
        old_rank = get_rank(user.exp)
        new_rank = get_rank(new_exp)

        # Check if the rank has changed
        if old_rank['name'] != new_rank['name']:
            self.__client.reply_message(
                f"(Ranked UP): {M.sender.username} has ranked up from {old_rank['name']} {old_rank['emoji']} "
                f"to {new_rank['name']} {new_rank['emoji']}", M)

        cmd.exec(M, contex)

    def load_commands(self, folder_path):
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
                self.commands[instance.config.command] = instance
                aliases = instance.config.aliases if hasattr(
                    instance.config, "aliases") else []
                for alias in aliases:
                    self.commands[alias] = instance

                self.__client.log.info("Loaded all the commands!")

    def parse_args(self, raw):
        args = raw.split(' ')
        cmd = args.pop(0).lower()[
            len(self.__client.config.prefix):] if args else ''
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
