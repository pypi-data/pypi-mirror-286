import sys
sys.dont_write_bytecode = True
import pysher
import time
import re
import os
from . import pusher_checker
from . import paths

def main():
    target_channel = ''
    app_key = ''
    cluster = ''
    if(not os.path.exists(paths.channel_name) or not pusher_checker.checker()):
        print("Channel or Pusher not setup")
        exit()
    else:
        file = open(paths.channel_name, 'r')
        target_channel = file.read().replace('\n', '')
        file = open(paths.key_config, 'r')
        app_key = file.read().replace('\n', '')
        file = open(paths.cluster_config, 'r')
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