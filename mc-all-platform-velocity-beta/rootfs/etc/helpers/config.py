#! /usr/bin/env python3
# config.py

import json
import logging
import os
import random
import re
import requests
import shutil
import string
import tomlkit
import uuid
from ruamel.yaml import YAML

LOG_LEVEL = 4
ROOT_DIR = ''

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

def check_dir(path: str):
  if not os.path.isdir(ROOT_DIR+path):
    log_norm(f"Directory {path} does not exist, creating...")
    os.makedirs(ROOT_DIR+path, exist_ok=True)

def file_exists(path):
  return os.path.isfile(ROOT_DIR+path)

def read_file(path: str):
  with open(ROOT_DIR+path, 'r', encoding='utf-8') as file:
    return file.read()
def write_file_a(path: str, to_write: str):
  with open(ROOT_DIR+path, 'a', encoding='utf-8') as file:
    return file.write(to_write)
def write_file_w(path: str, to_write: str):
  with open(ROOT_DIR+path, 'w', encoding='utf-8') as file:
    return file.write(to_write)

def log_finest(msg: str):
  if LOG_LEVEL >= 5: log.info(msg)
def log_finer(msg: str):
  if LOG_LEVEL >= 4: log.info(msg)
def log_fine(msg: str):
  if LOG_LEVEL >= 3: log.info(msg)
def log_norm(msg: str):
  if LOG_LEVEL >= 2: log.info("\033[92m"+msg+"\033[0m")
def log_warn(msg: str):
  if LOG_LEVEL >= 1: log.warning(msg)

def minimsg_to_leg(minimessage):
    colors = {
        "<black>": "&0", "<dark_blue>": "&1", "<dark_green>": "&2",
        "<dark_aqua>": "&3", "<dark_red>": "&4", "<dark_purple>": "&5",
        "<gold>": "&6", "<gray>": "&7", "<dark_gray>": "&8",
        "<blue>": "&9", "<green>": "&a", "<aqua>": "&b",
        "<red>": "&c", "<light_purple>": "&d", "<yellow>": "&e",
        "<white>": "&f", "<reset>": "&r"
    }
    formats = {
        "<obfuscated>": "&k", "<bold>": "&l", "<strikethrough>": "&m",
        "<underline>": "&n", "<italic>": "&o"
    }
    result = minimessage

    # Handle hex colors with closest legacy match
    hex_pattern = r'<#([0-9a-fA-F]{6})>'
    for match in re.finditer(hex_pattern, result):
        hex_color = match.group(1)
        # Map hex to nearest legacy color
        result = result.replace(f'<#{hex_color}>', "&b")

    # Handle gradients
    gradient_pattern = r'<gradient[^>]*>.*?</gradient>'
    result = re.sub(gradient_pattern, lambda m: "&b" + re.sub(r'<[^>]+>', '', m.group(0)), result)

    # Convert basic colors and formats
    for mini, legacy in {**colors, **formats}.items():
        result = result.replace(mini, legacy)

    # Handle special tags
    result = re.sub(r'<click[^>]*>.*?</click>', lambda m: re.sub(r'<[^>]+>', '', m.group(0)), result)
    result = re.sub(r'<hover[^>]*>.*?</hover>', lambda m: re.sub(r'<[^>]+>', '', m.group(0)), result)

    # Remove any remaining tags
    result = re.sub(r'<[^>]+>', '', result)

    return result


with open(ROOT_DIR+"/data/options.json", "r") as file:
  addon_conf = json.load(file)

## ----------------------------------- ##

if not file_exists("/config/uuid.txt"):
  log_norm("No uuid.txt found, generating one...")
  new_uuid = str(uuid.uuid4())
  log_finer(f"Generated UUID: {new_uuid}")
  write_file_a("/config/uuid.txt", new_uuid)
UUID = read_file("/config/uuid.txt")
log_fine(f"UUID: {UUID}")

if not file_exists("/config/forwarding.secret.txt"):
  log_norm("No forwarding.secret.txt found, generating one...")
  new_secret = ''.join(random.choices(string.ascii_letters+string.digits, k=10))
  log_fine(f"Generated forwarding secret: {new_secret}")
  write_file_a("/config/forwarding.secret.txt", new_secret)

###########

if not file_exists("/config/versions.yaml"):
  log_norm("No versions.yaml found, copying from default config...")
  shutil.copy(ROOT_DIR+"/default_config/versions.yaml", ROOT_DIR+"/config/versions.yaml")

vers_data = yaml.load(read_file("/config/versions.yaml"))

# load default versions.yaml to update the packaged_plugins section
vers_default = yaml.load(read_file("/default_config/versions.yaml"))
vers_data['packaged_plugins'] = vers_default['packaged_plugins']
vers_data['velocity'] = vers_default['velocity']

MAX_PLAYERS = addon_conf['max_players']
SERVER_NAME = addon_conf['server_name']

log_fine(f"Max Players: {MAX_PLAYERS}")
log_fine(f"Server Name: {SERVER_NAME}")

## ----------------------------------- ##

VEL_ROOT_CONFIG = addon_conf['rootConfig']
VEL_SERVERS = addon_conf['servers']
VEL_SERV_ATT_JOIN_ORD = addon_conf['serverAttemptJoinOrder']
VEL_FORCED_HOSTS = addon_conf['forcedHosts']
VEL_ADVANCED = addon_conf['advanced']

if not file_exists("/config/velocity.toml"):
  log_norm("No velocity.toml found, copying from default config...")
  shutil.copy(ROOT_DIR+"/default_config/velocity.toml", ROOT_DIR+"/config/velocity.toml")

# Load the TOML file
vel_toml = tomlkit.parse(read_file("/config/velocity.toml"))


for setting in VEL_ROOT_CONFIG:
  log_finer(f"{setting}: {VEL_ROOT_CONFIG[setting]}")
  vel_toml[setting] = VEL_ROOT_CONFIG[setting]

vel_toml['show-max-players'] = MAX_PLAYERS
vel_toml['motd'] = addon_conf['motd'][0]+"\n"+addon_conf['motd'][1]

vel_toml['servers'] = {}
for server in VEL_SERVERS:
  log_finer(f"{server}: {VEL_SERVERS[server]}")
  vel_toml['servers'][server] = VEL_SERVERS[server]

log_finer(f"try: {VEL_SERV_ATT_JOIN_ORD}")
vel_toml['servers']['try'] = VEL_SERV_ATT_JOIN_ORD

vel_toml['forced-hosts'] = {}
for host in VEL_FORCED_HOSTS:
  log_finer(f"{host}: {VEL_FORCED_HOSTS[host]}")
  if host == 'null':
    log_fine('Skipping null host')
    continue
  vel_toml['forced-hosts'][host] = VEL_FORCED_HOSTS[host]

for setting in VEL_ADVANCED:
  log_finer(f"{setting}: {VEL_ADVANCED[setting]}")
  vel_toml['advanced'][setting] = VEL_ADVANCED[setting]

log_finest(vel_toml)

# Save the updated TOML file
write_file_w("/config/velocity.toml", tomlkit.dumps(vel_toml))

## ----------------------------------- ##

def get_url(identifier: str, data: dict):
  log_finer(f"Data: {data}")
  
  url = data['url']
  for placeholder in re.findall(r'\{(\w+)\}', url):
    log_finer(f"Found placeholder: {placeholder}")
    url = url.replace(f"{{{placeholder}}}", str(data[placeholder]))
  return url


def download_jar(url: str, jar_name: str, path='/config/plugins/'):
  log_norm(f"Downloading {jar_name} from {url}...")
  response = requests.get(url)
  if response.status_code == 200:
    with open(ROOT_DIR+path+jar_name, "wb") as file:
      file.write(response.content)
    log_fine("JAR file downloaded successfully!")
    return True
  else:
    log.error("Failed to download the file.")
    return False

# velocity download
if not file_exists("/config/velocity.jar"):
  log_norm("No velocity.jar found, downloading...")
  download_jar(get_url('velocity', vers_data['velocity']), 'velocity.jar', '/config/')

check_dir("/config/plugins")

def download_plugins(main_group: str, override_group: str):
  log_norm(f"Downloading plugins from '{main_group}' with overrides from '{override_group}'")
  if vers_data[main_group] is None: return
  for plugin in vers_data[main_group]:
    log_finer(f"Plugin: {plugin}")
    plugin_data = dict(vers_data[main_group][plugin])
    log_finest(f"Plugin data: {plugin_data}")
    
    over_group = vers_data[override_group] if override_group != '' else {}
    over_data = {} if plugin not in over_group or over_group is None else over_group[plugin]
    log_finest(f"Override data: {over_data}")
      
    for key in over_data:
      log_finer(f"Overriding {key} with {over_data[key]}")
      plugin_data[key] = over_data[key]
    log_finer(f"Plugin data: {plugin_data}")
    
    if plugin_data is None: continue
    elif 'enabled' in plugin_data:
      enabled = plugin_data['enabled']
    else: enabled = True
    if not enabled:
      log_norm(f"Plugin '{plugin}' is disabled, skipping...")
      continue
    
    url = get_url(plugin, plugin_data)
    urls = vers_data['current_installed_urls']
    jar = plugin_data['jar']
    
    plugin_outdated = urls is None or plugin not in urls or urls[plugin] != url
  
    if plugin_outdated or not file_exists("/config/plugins/"+jar):
      success = download_jar(url, jar)
      if success:
        if vers_data['current_installed_urls'] is None:
          vers_data['current_installed_urls'] = {}
        vers_data['current_installed_urls'][plugin] = url

download_plugins('packaged_plugins', 'packaged_plugins_overrides')
download_plugins('custom_plugins', '')

with open(ROOT_DIR+"/config/versions.yaml", "w") as file:
  yaml.dump(vers_data, file)
  log_fine("Updated versions.yaml")

## ----------------------------------- ##

EAG_CONFIG = addon_conf['eagConfig']
EAG_SKIN = addon_conf['eagSkins']
EAG_VOICE = addon_conf['eagVoice']
EAG_UP_SERVICE = addon_conf['eagUpdateService']
EAG_UP_CHECKER = addon_conf['eagUpdateChecker']

check_dir("/config/plugins/eaglerxserver")
if not file_exists("/config/plugins/eaglerxserver/settings.toml"):
  log_norm("No eaglerxserver settings.toml found, copying from default config...")
  shutil.copy(
    ROOT_DIR+"/default_config/eag_settings.toml",
    ROOT_DIR+"/config/plugins/eaglerxserver/settings.toml")

eag_toml = tomlkit.parse(read_file("/config/plugins/eaglerxserver/settings.toml"))

eag_toml['server_uuid'] = UUID
eag_toml['server_name'] = SERVER_NAME

for setting in EAG_CONFIG:
  log_finer(f"{setting}: {EAG_CONFIG[setting]}")
  eag_toml[setting] = EAG_CONFIG[setting]

for setting in EAG_SKIN:
  log_finer(f"{setting}: {EAG_SKIN[setting]}")
  eag_toml['skin_service'][setting] = EAG_SKIN[setting]

for setting in EAG_VOICE:
  log_finer(f"{setting}: {EAG_VOICE[setting]}")
  eag_toml['voice_service'][setting] = EAG_VOICE[setting]

for setting in EAG_UP_SERVICE:
  log_finer(f"{setting}: {EAG_UP_SERVICE[setting]}")
  eag_toml['update_service'][setting] = EAG_UP_SERVICE[setting]

for setting in EAG_UP_CHECKER:
  log_finer(f"{setting}: {EAG_UP_CHECKER[setting]}")
  eag_toml['update_checker'][setting] = EAG_UP_CHECKER[setting]


log_finest(eag_toml)
write_file_w("/config/plugins/eaglerxserver/settings.toml", tomlkit.dumps(eag_toml))

# ------------------- #

EAG_LISTENER = addon_conf['eagListener']

if not file_exists("/config/plugins/eaglerxserver/listeners.toml"):
  log_norm("No eaglerxserver listeners.toml found, copying from default config...")
  shutil.copy(
    ROOT_DIR+"/default_config/eag_listeners.toml",
    ROOT_DIR+"/config/plugins/eaglerxserver/listeners.toml")

eag_list_toml = tomlkit.parse(read_file("/config/plugins/eaglerxserver/listeners.toml"))

eag_list_toml['listener_list'][0]['server_motd'] = [
  minimsg_to_leg(addon_conf['motd'][0]), 
  minimsg_to_leg(addon_conf['motd'][1])
]

for setting in EAG_LISTENER:
  log_finer(f"{setting}: {EAG_LISTENER[setting]}")
  eag_list_toml['listener_list'][0][setting] = EAG_LISTENER[setting]


log_finest(eag_list_toml)
write_file_w("/config/plugins/eaglerxserver/listeners.toml", tomlkit.dumps(eag_list_toml))

## ----------------------------------- ##

FLOOD = addon_conf["floodgate"]
FLOOD_DISCONNECT = addon_conf["floodDisconnect"]
FLOOD_PLAYER_LINK = addon_conf["floodPlayerLink"]

check_dir("/config/plugins/floodgate")

if not file_exists('/config/plugins/floodgate/config.yml'):
  log_norm("No Floodgate config.yml found, copying from default config...")
  shutil.copy(
    ROOT_DIR+"/default_config/floodgate.yml",
    ROOT_DIR+"/config/plugins/floodgate/config.yml")

flood_yaml = yaml.load(read_file("/config/plugins/floodgate/config.yml"))

for setting in FLOOD:
  log_finer(f"{setting}: {FLOOD[setting]}")
  flood_yaml[setting] = FLOOD[setting]

for setting in FLOOD_DISCONNECT:
  log_finer(f"{setting}: {FLOOD_DISCONNECT[setting]}")
  flood_yaml['disconnect'][setting] = FLOOD_DISCONNECT[setting]

for setting in FLOOD_PLAYER_LINK:
  log_finer(f"{setting}: {FLOOD_PLAYER_LINK[setting]}")
  flood_yaml['player-link'][setting] = FLOOD_PLAYER_LINK[setting]

flood_yaml['metrics']['uuid'] = UUID

with open(ROOT_DIR+"/config/plugins/floodgate/config.yml", "w") as file:
  yaml.dump(flood_yaml, file)
  log_fine("Updated Floodgate config.yml")

## ------------------------ ##

GEYSER_BEDROCK = addon_conf['geyserBedrock']
GEYSER_REMOTE = addon_conf['geyserRemote']
GEYSER = addon_conf['geyser']

check_dir("/config/plugins/Geyser-Velocity")

if not file_exists("/config/plugins/Geyser-Velocity/config.yml"):
  log_norm("No Geyser config.yml found, copying from default config...")
  shutil.copy(
    ROOT_DIR+"/default_config/geyser.yml",
    ROOT_DIR+"/config/plugins/Geyser-Velocity/config.yml")

geyser_yaml = yaml.load(read_file("/config/plugins/Geyser-Velocity/config.yml"))

geyser_yaml['metrics']['uuid'] = UUID
geyser_yaml['bedrock']['server-name'] = SERVER_NAME
geyser_yaml['max-players'] = MAX_PLAYERS
geyser_yaml['bedrock']['motd1'] = re.sub(r'<[^>]+>', '', addon_conf['motd'][0])
geyser_yaml['bedrock']['motd2'] = re.sub(r'<[^>]+>', '', addon_conf['motd'][1])

for setting in GEYSER_BEDROCK:
  log_finer(f"{setting}: {GEYSER_BEDROCK[setting]}")
  geyser_yaml['bedrock'][setting] = GEYSER_BEDROCK[setting]

for setting in GEYSER_REMOTE:
  log_finer(f"{setting}: {GEYSER_REMOTE[setting]}")
  geyser_yaml['remote'][setting] = GEYSER_REMOTE[setting]

for setting in GEYSER:
  log_finer(f"{setting}: {GEYSER[setting]}")
  geyser_yaml[setting] = GEYSER[setting]

with open(ROOT_DIR+"/config/plugins/Geyser-Velocity/config.yml", "w") as file:
  yaml.dump(geyser_yaml, file)
  log_fine("Updated Geyser config.yml")

## ----------------------------------- ##

check_dir("/config/plugins/viabackwards")
check_dir("/config/plugins/viarewind")

if not file_exists("/config/plugins/viabackwards/config.yml"):
  log_norm("No ViaBackwards config.yml found, copying from default config...")
  shutil.copy(
    ROOT_DIR+"/default_config/viabackwards.yml",
    ROOT_DIR+"/config/plugins/viabackwards/config.yml")

if not file_exists("/config/plugins/viarewind/config.yml"):
  log_norm("No ViaRewind config.yml found, copying from default config...")
  shutil.copy(
    ROOT_DIR+"/default_config/viarewind.yml",
    ROOT_DIR+"/config/plugins/viarewind/config.yml")
