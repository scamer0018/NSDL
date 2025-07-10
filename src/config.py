import os
from dotenv import load_dotenv
from utils import DynamicConfig

load_dotenv()

def get_config():
    return DynamicConfig({
        'name': os.getenv('NAME', 'Void'),
        'session': os.getenv('SESSION', 'db.sqlite3'),
        'number': os.getenv('NUMBER', '27782087369'),
        'prefix': os.getenv('PREFIX', '#'),
        'uri': os.getenv('URI', 'mongodb+srv://stumnmake:abhinavvijay@cluster0.kbpomy2.mongodb.net/Alice?retryWrites=true&w=majority'),
        'mods': os.getenv('MODS', '').split(',') if os.getenv('MODS') else []
    })
