import json
import os

CONFIG_PATH = '/data/options.json'

with open(CONFIG_PATH) as config_file:
    config = json.load(config_file)

os.environ['API_KEY'] = config['api_key']
os.environ['NETWORK'] = config['network']

# Run the Twingate Connector
os.system('/usr/bin/twingate-connector')