from datetime import datetime
import os
import importlib.util
from Models.User import User
from Models.Command import Command
from libs import Void
from libs import MessageClass
from utils import get_rank
from utils import DynamicConfig


class Message:

    commands = {}

    def __init__(self, client: Void):
        self.__client = client

    def handler(self, M: MessageClass):
        contex = DynamicConfig(self.parse_args(M.content))
        isCommand = M.content.startswith(self.__client.config.prefix)

        chat_type = "CMD" if isCommand else "MSG"
        chat_name = M.group.GroupName.Name if M.chat == "group" else "DM"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if isCommand:
            command = contex.cmd
            arg_count = len(contex.args) - 1
            self.__client.log.info(
                f"{chat_type} {self.__client.config.prefix}{command}[{arg_count}] from {M.sender.username} in {chat_name} at {timestamp}"
            )
        else:
            self.__client.log.info(
                f"{chat_type} from {M.sender.username} in {chat_name} at {timestamp}"
            )
        
        if not isCommand:
            return

        if M.content == self.__client.config.prefix:
            return self.__client.reply_message(f"💬 *Please enter a command* starting with *{self.__client.config.prefix}*.", M) 
        
        cmd = self.commands[contex.cmd] if contex.cmd in self.commands.keys() else None
        user: User = self.__client.db.get_user_by_number(M.sender.number)
        command: Command = self.__client.db.get_cmd_info(cmd.config.command) 

        if user.ban:
            return self.__client.reply_message(f"🚫 *Oops!* It looks like you are *banned* from using this bot.\n📝 *Reason:* {user.reason}\n🕒 *Banned at:* {user.banned_at.strftime('%Y-%m-%d %H:%M:%S (%z)')}\n\nIf you believe this is a mistake, please contact the admin. 🤖", M)

        if not cmd:
            return self.__client.reply_message(f"❌ *Command not available!* This command doesn't exist or has been disabled. Please check *{self.__client.config.prefix}help* to see all available commands.", M)

        if not command.enable:
            return self.__client.reply_message(f"🚫 Sorry! The command *${cmd.config.command}* is currently banned.\n\n*Banned at:* ${command.created_at.strftime('%Y-%m-%d %H:%M:%S (%z)')}\n*Reason:* ${command.reason}\n\nIf you think this is a mistake, please contact the admin. 🤖", M)
                                              
        if hasattr(cmd.config, "group") and M.chat == "dm":
            return self.__client.reply_message(
                "👥 These commands are *group-only*, please try them inside a group.", M)
        
        if hasattr(cmd.config, "dm") and M.chat == "group":
            return self.__client.reply_message(
                "💬 Please use this command in *private chat* only.", M)
        
        if hasattr(cmd.config, "devOnly") and M.Info.Sender.User not in self.__client.config.mods:
            return self.__client.reply_message(
                "⚠️ *Oops!* Some of these commands are *exclusively for developers*.", M)
        
        if hasattr(cmd.config, "admin") and not M.isAdminMessage:
            if (self.__client.build_jid(self.__client.get_me().JID) in self.__client.filter_admin_users(
                self.group.Participants)):
                return self.__client.reply_message("🤖 The *bot must be an admin* to execute these commands properly.", M)
            return self.__client.reply_message("🚫 *Sorry!* You don’t have the required permissions to use this command. Kindly become an *admin* first.", M)

        self.__client.db.add_exp(M.sender.number, cmd.config.exp)

        new_exp = user.exp + cmd.config.exp

        # Get the old and new ranks
        old_rank = get_rank(user.exp)
        new_rank = get_rank(new_exp)

        # Check if the rank has changed
        if old_rank['name'] != new_rank['name']:
            self.__client.reply_message(
                f"🎉 *Congratuations*! {M.sender.username} has ranked up from *{old_rank['name']} {old_rank.data['emoji']}* " + 
                f"to *{new_rank['name']} {new_rank.data['emoji']}*", M)

        cmd.exec(M, contex)

    def load_commands(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith('.py'):
                module_name = filename[:-3]
                file_path = os.path.join(folder_path, filename)
    
                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    if not spec or not spec.loader:
                        raise ImportError(f"Cannot load spec for {file_path}")
    
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
    
                    class_ = getattr(module, "Command")
                    instance = class_(self.__client, self)
                    self.commands[instance.config.command] = instance
    
                    self.__client.log.info(f"Loaded {instance.config.command} from {file_path}")
    
                    aliases = getattr(instance.config, "aliases", [])
                    for alias in aliases:
                        self.commands[alias] = instance
    
                except Exception as e:
                    self.__client.log.error(f"Failed to load {filename}: {e}")
    
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
