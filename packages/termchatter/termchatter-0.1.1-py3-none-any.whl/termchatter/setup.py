import sys
sys.dont_write_bytecode = True
import os

def main(args):
    if len(args) == 0:
        print("Type 'chat help' for guidance")
        return
    
    command = args[0]
    
    if command == 'pusher' and len(args) == 5:
        app_id, app_key, secret, cluster = args[1:5]
        save_config('.appid', app_id)
        save_config('.appkey', app_key)
        save_config('.secret', secret)
        save_config('.cluster', cluster)
    elif len(args) == 1:
        save_config('.channel', args[0])
    elif len(args) == 2:
        save_config('.channel', args[0])
        save_config('.username', args[1])
    else:
        print("Type 'chat help' for guidance")

def save_config(filename, data):
    config_path = os.path.join(os.getcwd(), filename)
    with open(config_path, 'w') as file:
        file.write(data)