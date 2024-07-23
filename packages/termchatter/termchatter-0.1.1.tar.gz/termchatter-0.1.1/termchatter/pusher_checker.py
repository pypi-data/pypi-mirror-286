import sys
sys.dont_write_bytecode = True
import os

def checker():
    id_config = '.appid'
    key_config = '.appkey'
    secret_config = '.secret'
    cluster_config = '.cluster'
    if(not os.path.exists(id_config) or not os.path.exists(key_config) or not os.path.exists(secret_config) or not os.path.exists(cluster_config)):
        return False
    return True