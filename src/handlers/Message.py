from datetime import datetime
import os
import importlib.util
import re
from models.User import User
from models.Command import Command
from libs import Void, MessageClass
from utils import get_rank, DynamicConfig


class Message:
    def __init__(self, client: Void):
        self.__client = client
        self.commands = {}

    def handler(self, M: MessageClass):
        contex = DynamicConfig(self.parse_args(M.content))
        is_command = M.content.startswith(self.__client.config.prefix)

        chat_type = "CMD" if is_command else "MSG"
        chat_name = M.group.GroupName.Name if M.chat == "group" else "DM"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.wa_link_detector(M)

        if is_command:
            command = contex.cmd
            arg_count = len(contex.args) - 1
            self.__client.log.info(
                f"{chat_type} {self.__client.config.prefix}{command}[{arg_count}] from {M.sender.username} in {chat_name} at {timestamp}"
            )
        else:
            return self.__client.log.info(
                f"{chat_type} from {M.sender.username} in {chat_name} at {timestamp}"
            )

        if M.content == self.__client.config.prefix:
            return self.__client.reply_message(
                f"💬 *Please enter a command* starting with *{self.__client.config.prefix}*.",
                M,
            )

        cmd = self.commands.get(contex.cmd.lower()) or next(
            (
                c
                for c in self.commands.values()
                if contex.cmd.lower() in getattr(c.config, "aliases", [])
            ),
            None,
        )

        if not cmd:
            return self.__client.reply_message(
                f"❌ *Unknown command!* Use *{self.__client.config.prefix}help* to see all available commands.",
                M,
            )

        user: User = self.__client.db.get_user_by_number(M.sender.number)
        command_info: Command = self.__client.db.get_cmd_info(
            cmd.config.command
        )

        if user.ban:
            return self.__client.reply_message(
                f"🚫 *Oops!* It looks like you are *banned* from using this bot.\n📝 *Reason:* {user.reason}\n🕒 *Banned at:* {user.banned_at.strftime('%Y-%m-%d %H:%M:%S (%z)')}\n\nIf you believe this is a mistake, please contact the admin. 🤖",
                M,
            )

        if not command_info.enable:
            return self.__client.reply_message(
                f"🚫 Sorry! The command *{cmd.config.command}* is currently disabled.\n\n"
                f"*Banned at:* {command_info.created_at.strftime('%Y-%m-%d %H:%M:%S (%z)')}\n"
                f"*Reason:* {command_info.reason}\n\n"
                "If you think this is a mistake, please contact the admin. 🤖",
                M,
            )

        if getattr(cmd.config, "group", False) and M.chat == "dm":
            return self.__client.reply_message(
                "👥 These commands are *group-only*, please try them inside a group.",
                M,
            )

        if getattr(cmd.config, "dm", False) and M.chat == "group":
            return self.__client.reply_message(
                "💬 Please use this command in *private chat* only.", M
            )

        if (
            getattr(cmd.config, "devOnly", False)
            and M.sender.number not in self.__client.config.mods
        ):
            return self.__client.reply_message(
                "⚠️ *Oops!* Some of these commands are *exclusively for developers*.",
                M,
            )

        if getattr(cmd.config, "admin", False) and not M.isAdminMessage:
            if (
                self.__client.get_me().JID.User
                not in self.__client.filter_admin_users(M.group.Participants)
            ):
                return self.__client.reply_message(
                    "🤖 The *bot must be an admin* to execute these commands properly.",
                    M,
                )
            return self.__client.reply_message(
                "🚫 *Sorry!* You don’t have the required permissions to use this command. Kindly become an *admin* first.",
                M,
            )

        # Add EXP and check rank up
        self.__client.db.add_exp(M.sender.number, cmd.config.exp)
        new_exp = user.exp + cmd.config.exp

        old_rank = get_rank(user.exp)
        new_rank = get_rank(new_exp)

        if old_rank["name"] != new_rank["name"]:
            self.__client.reply_message(
                f"🎉 *Congratulations*! {M.sender.username} has ranked up from *{old_rank['name']} {old_rank['data']['emoji']}* "
                f"to *{new_rank['name']} {new_rank['data']['emoji']}*",
                M,
            )

        cmd.exec(M, contex)

    def wa_link_detector(self, M: MessageClass):
        group = self.__client.db.get_group_by_number(M.gcjid.User)

        if not group.mod:
            return
        pattern = re.compile(r"https://chat\.whatsapp\.com/\S+", re.IGNORECASE)
        admins = self.__client.filter_admin_users(M.group.Participants)

        if not M.isAdminMessage:
            for url in M.urls:
                if pattern.search(url):
                    try:
                        link_info = self.__client.get_group_info_from_link(
                            url.split("?")[0]
                        )
                        if link_info.GroupName.Name != M.group.GroupName.Name:
                            if self.__client.get_me().JID.User in admins:
                                from neonize.utils import ParticipantChange

                                self.__client.update_group_participants(
                                    M.gcjid,
                                    [self.__client.build_jid(M.sender.number)],
                                    ParticipantChange.REMOVE,
                                )

                            mentions = [f"@{admin}" for admin in admins]
                            text = (
                                "🚫 A *suspicious group link* was detected in the chat.\n\n"
                                + " ".join(mentions)
                            )

                            self.__client.send_message(M.gcjid, text)

                    except Exception as e:
                        self.__client.log.error(f"[WA_LINK_DETECTOR] {e}")

    def load_commands(self, folder_path):
        self.__client.log.info("Loading commands...")

        all_files = self.__client.utils.readdir_recursive(folder_path)

        for file_path in all_files:
            if not file_path.endswith(".py") or os.path.basename(
                file_path
            ).startswith("_"):
                continue

            try:
                module_name = os.path.splitext(os.path.basename(file_path))[0]

                spec = importlib.util.spec_from_file_location(
                    module_name, file_path
                )
                if not spec or not spec.loader:
                    raise ImportError(f"Cannot load spec for {file_path}")

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                CommandClass = getattr(module, "Command", None)
                if not CommandClass:
                    raise AttributeError(
                        f"No class 'Command' found in {file_path}"
                    )

                command_instance = CommandClass(self.__client, self)
                command_id = command_instance.config.command
                self.commands[command_id] = command_instance

                self.__client.log.info(
                    f"✅ Loaded: {command_id} from {command_instance.config.get('category', 'Uncategorized')}"
                )

            except Exception as e:
                self.__client.log.error(f"❌ Failed to load {file_path}: {e}")

        self.__client.log.info(
            f"✅ Successfully loaded {len(self.commands)} commands."
        )

    def parse_args(self, raw):
        args = raw.split(" ")
        cmd = (
            args.pop(0).lower()[len(self.__client.config.prefix) :]
            if args
            else ""
        )
        text = " ".join(args)
        flags = {}

        for arg in args:
            if arg.startswith("--") and "=" in arg:
                key, value = arg[2:].split("=", 1)
                flags[key] = value
            elif arg.startswith("-"):
                flags[arg] = ""

        return {
            "cmd": cmd,
            "text": text,
            "flags": flags,
            "args": args,
            "raw": raw,
        }
