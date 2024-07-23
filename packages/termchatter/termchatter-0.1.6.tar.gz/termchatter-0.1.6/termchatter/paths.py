import os

base_path = os.path.expanduser('~/.config/termchatter/')
id_config = os.path.join(base_path, 'termchatter_appid')
key_config = os.path.join(base_path, 'termchatter_appkey')
secret_config = os.path.join(base_path, 'termchatter_secret')
cluster_config = os.path.join(base_path, 'termchatter_cluster')
channel_name = os.path.join(base_path, 'termchatter_channel')
user_name = os.path.join(base_path, 'termchatter_username')

def initialize_directories():
    os.makedirs(base_path, exist_ok=True)

# Call the function to ensure the directory is created
initialize_directories()
