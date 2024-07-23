import sys
sys.dont_write_bytecode = True
import pysher
import time
import re
import os
from . import pusher_checker

def main():
    key_config = '.appkey'
    cluster_config = '.cluster'
    channel_name = '.channel'
    target_channel = ''
    app_key = ''
    cluster = ''
    if(not os.path.exists(channel_name) or not pusher_checker.checker()):
        print("Channel or Pusher not setup")
        exit()
    else:
        file = open(channel_name, 'r')
        target_channel = file.read().replace('\n', '')
        file = open(key_config, 'r')
        app_key = file.read().replace('\n', '')
        file = open(cluster_config, 'r')
        cluster = file.read().replace('\n', '')

    pusher = pysher.Pusher(app_key, cluster=cluster)

    def my_func(data):
        data = re.findall(r'{"username": "(.*?)", "message": "(.*?)"}', data)[0]
        username = data[0]
        message = data[1]
        print(username, '>> ', message)

    def connect_handler(data):
        channel = pusher.subscribe(target_channel)
        channel.bind('message', my_func)


    pusher.connection.bind('pusher:connection_established', connect_handler)
    pusher.connect()

    print("\n" * 100)
    print("Listening to -", target_channel)

    while True:
        time.sleep(1)