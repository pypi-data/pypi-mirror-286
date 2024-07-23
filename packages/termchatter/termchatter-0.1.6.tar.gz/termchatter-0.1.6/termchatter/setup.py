import sys
sys.dont_write_bytecode = True
import os
from . import paths

def main(args):
    if len(args) == 0:
        print("Type 'chat help' for guidance")
        return
    
    command = args[0]
    
    if command == 'pusher' and len(args) == 5:
        app_id, app_key, secret, cluster = args[1:5]
        save_config(paths.id_config, app_id)
        save_config(paths.key_config, app_key)
        save_config(paths.secret_config, secret)
        save_config(paths.cluster_config, cluster)
    elif len(args) == 1:
        save_config(paths.channel_name, args[0])
    elif len(args) == 2:
        save_config(paths.channel_name, args[0])
        save_config(paths.user_name, args[1])
    else:
        print("Type 'chat help' for guidance")

def save_config(config_path, data):
    with open(config_path, 'w') as file:
        file.write(data)