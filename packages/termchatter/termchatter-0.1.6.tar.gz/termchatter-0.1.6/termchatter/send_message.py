import sys
sys.dont_write_bytecode = True
import os.path
import pusher
from . import pusher_checker
from . import paths

def main():
    app_id = ''
    app_key = ''
    secret = ''
    cluster = ''
    if(not os.path.exists(paths.channel_name) or not os.path.exists(paths.user_name) or not pusher_checker.checker()):
        print(os.path.exists(paths.channel_name))
        print(os.path.exists(paths.user_name))
        print(pusher_checker.checker())
        print("Channel, username, or Pusher not setup")
        exit()
    else:
        file = open(paths.channel_name, 'r')
        channel = file.read().replace('\n', '')
        file = open(paths.user_name, 'r')
        username = file.read().replace('\n', '')
        file = open(paths.id_config, 'r')
        app_id = file.read().replace('\n', '')
        file = open(paths.key_config, 'r')
        app_key = file.read().replace('\n', '')
        file = open(paths.secret_config, 'r')
        secret = file.read().replace('\n', '')
        file = open(paths.cluster_config, 'r')
        cluster = file.read().replace('\n', '')
        

    pusher_client = pusher.Pusher(
    app_id=app_id,
    key=app_key,
    secret=secret,
    cluster=cluster,
    ssl=True
    )

    while(True):
        print("\n" * 100)
        message = input(">> ")
        pusher_client.trigger(channel, 'message', {'username': username, 'message': message})