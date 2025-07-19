# WhatsApp-Botto-Py

## ✅ Bot Overview
- **Bot Name**: `WhatsApp-Botto-Py`
- **Built With**: Python
- **Primary Library**: [`neonize`](https://github.com/krypton-byte/neonize) (WhatsApp Web API for Python)
- **Database**: MongoDB
- **For Termux**: Uses `tur-repo` MongoDB variant
- **Session File**: No QR scanning, uses direct session generation (`db.sqlite3`)
- **Terminal Command Setup**: Copy-paste and run link system (Termux support)

## ✅ Features
- Easy plug-and-play installation via Termux
- MongoDB + local SQLite combo
- In-built session file generator to avoid QR hassle
- Modular command handler
- Fully compatible with Termux, VPS, and local machines

## ✅ Hosting Options
- **Termux** (preferred for local)
- **VPS / Ubuntu / Linux machine**
- **Windows**

## ✅ Configuration Explained
Inside your `.env` or config file:

```env
NAME=Void  # The instance name for your bot
SESSION=db.sqlite3  # SQLite3 file used to store session info
NUMBER=27782xxxxxx  # Bot’s phone number (required)

PREFIX=#  # The prefix for commands

URI=mongodb://127.0.0.1:27017/database
# MongoDB URI. ⚠️ DO NOT CHANGE THIS IF YOU ARE HOSTING ON TERMUX

MODS=27782xxxxxx,91700xxxxxx,91983xxxxxx
# Comma-separated moderator numbers
```

✅ **Note**:
- Make sure `NUMBER` is set to your bot's number, or it won’t connect.
- **Do not modify the MongoDB URI** if you're using Termux – it’s tailored for local hosting via `tur-mongodb`.

## ✅ Example: Sending a Message in Code

You can respond to messages or send messages manually using:

```python
self.client.reply_message(message, "Your reply here")
```

## ✅ Creating Your Own Command

1. Go to the `commands/` folder.
2. Create a new Python file (e.g., `hello.py`)
3. Extend `BaseCommand` and define your logic.

```python
from libs import BaseCommand, MessageClass


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "hi",
                "category": "core",
                "description": {"content": "Say hello to the bot"}
            },
        )

    def exec(self, M: MessageClass, _):
        self.client.reply_message(
            f"🎯 Hey *@{M.sender.number}*!", M
        )

```

## 📄 All Available Commands

| Command   | Description                  |
| --------- | ---------------------------- |
| help      | Shows all commands           |
| sticker   | Converts media to sticker    |
| (More...) | Check `src/commands/` folder |

You can easily explore all commands by typing `#help` or `#menu` in your WhatsApp chat with the bot.

## 🚀 Termux Installation Guide

Follow these steps to install and run **WhatsApp-Botto-Py** on Termux:

1. **Install Required Packages and Script Environment**

```bash
pkg update -y && pkg upgrade -y
pkg install -y git python tur-repo
pkg install -y mongodb
````

2. **Clone the Bot Repository**

```bash
git clone https://github.com/your-username/WhatsApp-Botto-Py.git
```

3. **Navigate to the Bot Directory**

```bash
cd WhatsApp-Botto-Py
```

4. **Install Python Requirements**

```bash
pip install -r requirements.txt
```

5. **Start the Bot**

```bash
python3 src/main.py
```

---

📝 **Note:**

* Do **not change** the MongoDB URI if you're running the bot on Termux.
* Make sure you've configured the `.env` file correctly with:

  * `NUMBER` = your bot number (linked with WhatsApp)
  * `URI` = keep `mongodb://127.0.0.1:27017/database`
  * `SESSION` = local SQLite3 file
