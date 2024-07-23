import sys
sys.dont_write_bytecode = True
import os
from . import paths

def checker():
    if(not os.path.exists(paths.id_config) or not os.path.exists(paths.key_config) or not os.path.exists(paths.secret_config) or not os.path.exists(paths.cluster_config)):
        return False
    return True