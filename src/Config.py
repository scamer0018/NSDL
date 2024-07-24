import os
from dotenv import load_dotenv

load_dotenv()


def get_config():
    return {
        'name': os.getenv('NAME', 'Alica'),
        'prefix': os.getenv('PREFIX', '#'),
        'uri': os.getenv('URI', ''),
        'mods': os.getenv('MODS', '').split(',') if os.getenv('MODS') else []
    }
