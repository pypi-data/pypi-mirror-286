import sys
sys.dont_write_bytecode = True
import os.path
import pusher
from . import pusher_checker

def main(args):
    id_config = '.appid'
    key_config = '.appkey'
    secret_config = '.secret'
    cluster_config = '.cluster'
    channel_name = '.channel'
    user_name = '.username'
    app_id = ''
    app_key = ''
    secret = ''
    cluster = ''
    if(not os.path.exists(channel_name) or not os.path.exists(user_name) or not pusher_checker.checker()):
        print("Channel, username, or Pusher not setup")
        exit()
    else:
        file = open(channel_name, 'r')
        channel = file.read().replace('\n', '')
        file = open(user_name, 'r')
        username = file.read().replace('\n', '')
        file = open(id_config, 'r')
        app_id = file.read().replace('\n', '')
        file = open(key_config, 'r')
        app_key = file.read().replace('\n', '')
        file = open(secret_config, 'r')
        secret = file.read().replace('\n', '')
        file = open(cluster_config, 'r')
        cluster = file.read().replace('\n', '')
        

    pusher_client = pusher.Pusher(
    app_id=app_id,
    key=app_key,
    secret=secret,
    cluster=cluster,
    ssl=True
    )

    if(len(args) == 1):
        message = args[0]
    else:
        print("Put your message as argument, use quotes to send messages with spaces")
        exit()

    pusher_client.trigger(channel, 'message', {'username': username, 'message': message})