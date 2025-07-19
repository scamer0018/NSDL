# WhatsApp-Botto-Py  

A WhatsApp bot built with [neonize](https://github.com/krypton-byte/neonize) (Python). This is my first open source Python project feel free to open issues if you spot mistakes!  

⚠️ **Disclaimer**:  
WhatsApp does not allow bots/unofficial clients. While this code works, I cannot guarantee your account won’t be blocked. Use at your own risk.  


## **Bot Overview**  
- **Name**: `WhatsApp-Botto-Py`  
- **Language**: Python  
- **Core Library**: [neonize](https://github.com/krypton-byte/neonize)  
- **Database**: MongoDB (Termux: `tur repo` variant)
- **Setup**: Copy-paste terminal commands (Termux friendly).  


## **Features**  
✅ Plug and play Termux installation  
✅ MongoDB 
✅ Modular command system  
✅ Compatible with Termux, VPS, Linux, and Windows  


## **Configuration**  
Edit `.env` or config file:  

```env
NAME=Void              # Bot instance name  
SESSION=db.sqlite3      # Session storage file  
NUMBER=27782xxxxxx      # Bot's WhatsApp number (required)  
PREFIX=#               # Command prefix  

URI=mongodb://127.0.0.1:27017/database  
# Keep this URI if using Termux (tur-mongodb)  

MODS=27782xxxxxx,91700xxxxxx  # Moderator numbers (comma-separated)  
```

**Important**:  
- `NUMBER` must be the bot’s linked WhatsApp number.  
- Do **not** modify the MongoDB URI for Termux.  


## **Code Examples**  
### **Sending a Reply**  
```python
self.client.reply_message("Your reply here", M)  
```

### **Creating a Custom Command**  
1. Navigate to `commands/` and create a file (e.g., `hello.py`).  
2. Extend `BaseCommand`:  

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
        self.client.reply_message(f"🎯 Hey *@{M.sender.number}*!", M)  
```


## **Command List**  
| Command   | Description                  |  
|-----------|-----------------------------|  
| `help`    | Show all commands           |  
| `sticker` | Convert media to sticker    |  
| *(More in `src/commands/`)* |  

Type `#help` in WhatsApp to see all commands.  


## **🚀 Termux Installation**  
1. **Set Up Environment**:  
   ```bash
> pkg update -y && pkg upgrade -y  
> pkg install -y wget  
> wget -O - https://raw.githubusercontent.com/Debanjan-San/WhatsApp-Botto-Py/main/setup.sh | bash  
   ```  

2. **Clone & Run**:  
   ```bash
> git clone https://github.com/Debanjan-San/WhatsApp-Botto-Py.git  
> cd WhatsApp-Botto-Py  
> pip install -r requirements.txt  
> python3 src/main.py  
   ```  

## **Contributing**  
1. Fork the repo.  
2. Create a branch: `git checkout -b my-feature`.  
3. Commit changes: `git commit -am "Add feature"`.  
4. Push: `git push origin my-feature`.  
5. Open a pull request.  


## **📜 License**  
MIT © [Debanjan Das](https://github.com/Debanjan-San).  
