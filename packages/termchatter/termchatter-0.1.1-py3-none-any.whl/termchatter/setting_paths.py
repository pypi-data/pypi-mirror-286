import sys
sys.dont_write_bytecode = True
import os
import json

def load_settings():
    settings_path = os.path.join(os.path.dirname(__file__), 'settings', 'config.json')
    with open(settings_path) as f:
        config = json.load(f)
    return config
