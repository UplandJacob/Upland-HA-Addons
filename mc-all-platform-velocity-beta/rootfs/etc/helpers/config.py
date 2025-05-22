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

ROOT_DIR = '.'
CONF_DIR = ROOT_DIR + '/config'
SERV_DIR = CONF_DIR + '/server'
PLUG_DIR = SERV_DIR + '/plugins'
DEF_CONF = ROOT_DIR + '/default_config'
with open(ROOT_DIR+"/data/options.json", "r") as file:
  addon_conf = json.load(file)

LOG_LEVEL = addon_conf['logLevel']

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("CONF")

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

def check_dir(path: str):
  if not os.path.isdir(path):
    log_warn(f"Directory {path} does not exist, creating...")
    os.makedirs(path, exist_ok=True)

def file_exists(path):
  log_finest(f"Checking if file {path} exists...")
  return os.path.isfile(path)

def read_file(path: str):
  with open(path, 'r', encoding='utf-8') as file:
    return file.read()
def write_file_a(path: str, to_write: str):
  with open(path, 'a', encoding='utf-8') as file:
    return file.write(to_write)
def write_file_w(path: str, to_write: str):
  with open(path, 'w', encoding='utf-8') as file:
    return file.write(to_write)

def log_finest(msg: str):
  if LOG_LEVEL >= 5: log.info(msg)
def log_finer(msg: str):
  if LOG_LEVEL >= 4: log.info(msg)
def log_fine(msg: str):
  if LOG_LEVEL >= 3: log.info(msg)
def log_norm(msg: str):
  if LOG_LEVEL >= 2: log.info("\033[32m"+msg+"\033[0m")
def log_warn(msg: str):
  if LOG_LEVEL >= 1: log.warning("\033[33m"+msg+"\033[0m")
  

def minimsg_to_leg(minimessage):
    colors = {
        "<black>": "&0", "<dark_blue>": "&1", "<dark_green>": "&2", "<dark_aqua>": "&3", "<dark_red>": "&4", "<dark_purple>": "&5",
        "<gold>": "&6", "<gray>": "&7", "<dark_gray>": "&8", "<blue>": "&9", "<green>": "&a", "<aqua>": "&b",
        "<red>": "&c", "<light_purple>": "&d", "<yellow>": "&e", "<white>": "&f", "<reset>": "&r"
    }
    formats = {
        "<obfuscated>": "&k", "<obf>": "&k", "<bold>": "&l", "<b>": "&l", "<strikethrough>": "&m", "<st>": "&m",
        "<underline>": "&n", "<u>": "&n", "<italic>": "&o", "<i>": "&o"
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

## ------------------ ##

check_dir(CONF_DIR+"/server")

if not file_exists(CONF_DIR+"/uuid.txt"):
  log_warn("No uuid.txt found, generating one...")
  new_uuid = str(uuid.uuid4())
  log_finest(f"Generated UUID: {new_uuid}")
  write_file_a(CONF_DIR+"/uuid.txt", new_uuid)
UUID = read_file(CONF_DIR+"/uuid.txt")
log_norm(f"Server UUID: {UUID}")

if not file_exists(SERV_DIR+"/forwarding.secret.txt"):
  log_warn("No forwarding.secret.txt found, generating one...")
  new_secret = ''.join(random.choices(string.ascii_letters+string.digits, k=10))
  log_fine(f"Generated forwarding secret: {new_secret}")
  write_file_a(SERV_DIR+"/forwarding.secret.txt", new_secret)

###########

if not file_exists(CONF_DIR+"/versions.yaml"):
  log_warn("No versions.yaml found, copying from default config...")
  shutil.copy(DEF_CONF+"/versions.yaml", CONF_DIR+"/versions.yaml")

vers_data = yaml.load(read_file(CONF_DIR+"/versions.yaml"))

# load default versions.yaml to update the packaged_plugins section
vers_default = yaml.load(read_file(DEF_CONF+"/versions.yaml"))
vers_data['packaged_plugins'] = vers_default['packaged_plugins']
vers_data['velocity'] = vers_default['velocity']


MAX_PLAYERS = addon_conf['max_players']
SERVER_NAME = addon_conf['server_name']

def parse_pl_holds(inp):
  inp = re.sub(r"{se?rv(er)?(_?na?me?)?}", SERVER_NAME, inp, flags=re.IGNORECASE)
  inp = re.sub(r"{max_?pl(a?ye?)?r?s}", str(MAX_PLAYERS), inp, flags=re.IGNORECASE)
  return inp

MOTD1 = parse_pl_holds(addon_conf['motd1'])
MOTD2 = parse_pl_holds(addon_conf['motd2'])

log_fine(f"Max Players: {MAX_PLAYERS}")
log_fine(f"Server Name: {SERVER_NAME}")
log_fine(f"MOTD1: {MOTD1}")
log_fine(f"MOTD2: {MOTD2}")


## ----------------------------------- ##

VEL_ROOT_CONFIG = addon_conf['rootConfig']
VEL_SERVERS = addon_conf['servers']
VEL_SERV_ATT_JOIN_ORD = addon_conf['serverAttemptJoinOrder']
VEL_FORCED_HOSTS = addon_conf['forcedHosts']
VEL_ADVANCED = addon_conf['adv']

if not file_exists(SERV_DIR+"/velocity.toml"):
  log_warn("No velocity.toml found, copying from default config...")
  shutil.copy(DEF_CONF+"/velocity.toml", SERV_DIR+"/velocity.toml")

# Load the TOML file
vel_toml = tomlkit.parse(read_file(SERV_DIR+"/velocity.toml"))


for setting in VEL_ROOT_CONFIG:
  log_finer(f"{setting}: {VEL_ROOT_CONFIG[setting]}")
  vel_toml[setting] = VEL_ROOT_CONFIG[setting]

vel_toml['show-max-players'] = MAX_PLAYERS
vel_toml['motd'] = MOTD1+"\n"+MOTD2

vel_toml['servers'] = {}
for i in range(len(VEL_SERVERS)):
  server = VEL_SERVERS[i]['name']
  addr = VEL_SERVERS[i]['address']
  log_finer(f"{server}: {addr}")
  vel_toml['servers'][server] = addr

log_finer(f"try: {VEL_SERV_ATT_JOIN_ORD}")
vel_toml['servers']['try'] = VEL_SERV_ATT_JOIN_ORD

vel_toml['forced-hosts'] = {}
for i in range(len(VEL_FORCED_HOSTS)):
  host = VEL_FORCED_HOSTS[i]['hostname']
  serv_names = VEL_FORCED_HOSTS[i]['servNames']
  log_finer(f"{host}: {serv_names}")
  if host == 'null':
    log_fine('Skipping null host')
    continue
  vel_toml['forced-hosts'][host] = serv_names

for setting in VEL_ADVANCED:
  log_finer(f"{setting}: {VEL_ADVANCED[setting]}")
  vel_toml['advanced'][setting] = VEL_ADVANCED[setting]

log_finest(vel_toml)

# Save the updated TOML file
write_file_w(SERV_DIR+"/velocity.toml", tomlkit.dumps(vel_toml))
log_norm("Updated velocity.toml")

## ----------------------------------- ##

def plug_placeholders(txt: str, data: dict) -> str:
  for placeholder in re.findall(r'\{(\w+)\}', txt):
    log_finer(f"Found placeholder: {placeholder}")
    txt = txt.replace(f"{{{placeholder}}}", str(data[placeholder]))
  return txt


def download_file(url: str, f_name: str, path=PLUG_DIR):
  log_norm(f"Downloading {f_name} from {url}...")
  response = requests.get(url)
  if response.status_code == 200:
    with open(path+"/"+f_name, "wb") as file:
      file.write(response.content)
    log_fine("File downloaded successfully!")
    return True
  else:
    log_warn("Failed to download the file.")
    return False

# velocity download
if not file_exists(SERV_DIR+"/velocity.jar"):
  log_warn("No velocity.jar found, downloading...")
  download_file(plug_placeholders(vers_data['velocity']['url'], vers_data['velocity']), 'velocity.jar', SERV_DIR)

check_dir(PLUG_DIR)
check_dir(PLUG_DIR+"/Geyser-Velocity/extensions")
check_dir(PLUG_DIR+"/Geyser-Velocity/packs")

def download_plugins(main_group: str, override_group: str):
  log_norm(f"Downloading plugins from '{main_group}' with overrides from '{override_group}'")
  if vers_data[main_group] is None: return
  for plugin in vers_data[main_group]:
    log_finer(f"Plugin: {plugin}")
    plugin_data = dict(vers_data[main_group][plugin])
    log_finest(f"Plugin data: {plugin_data}")

    over_group = vers_data[override_group] if override_group != '' else {}
    over_data = {} if over_group is None or plugin not in over_group else over_group[plugin]
    log_finest(f"Override data: {over_data}")

    for key in over_data:
      log_finer(f"Overriding {key} with {over_data[key]}")
      plugin_data[key] = over_data[key]
    log_finer(f"Plugin data: {plugin_data}")

    if plugin_data is None: continue
    elif 'enabled' in plugin_data: enabled = plugin_data['enabled']
    else: enabled = True
    if not enabled:
      log_norm(f"Plugin '{plugin}' is disabled, skipping...")
      continue

    path = "/"
    if 'path' in plugin_data and plugin_data['path'] is not None:
      path = plugin_data['path']
      if not path.startswith("/"): path = "/"+path
      if not path.endswith("/"): path += "/"
    log_finer(f"Path: {path}")

    url = plug_placeholders(plugin_data['url'], plugin_data)
    if vers_data['current_installed_urls'] is None: vers_data['current_installed_urls'] = {}
    urls = vers_data['current_installed_urls']
    f_nm = plug_placeholders(plugin_data['file'], plugin_data)

    if plugin not in urls or urls[plugin] != url or not file_exists(PLUG_DIR+path+f_nm):
      if download_file(url, f_nm, PLUG_DIR+path): vers_data['current_installed_urls'][plugin] = url

download_plugins('packaged_plugins', 'packaged_plugins_overrides')
download_plugins('custom_plugins', '')

with open(CONF_DIR+"/versions.yaml", "w") as file:
  yaml.dump(vers_data, file)
  log_norm("Updated versions.yaml")

## ----------------------------------- ##

EAG_CONFIG = addon_conf['eagConfig']
EAG_SKIN = addon_conf['eagSkins']
EAG_VOICE = addon_conf['eagVoice']
EAG_UP_SERVICE = addon_conf['eagUpdateService']
EAG_UP_CHECKER = addon_conf['eagUpdateChecker']

check_dir(PLUG_DIR+"/eaglerxserver")
if not file_exists(PLUG_DIR+"/eaglerxserver/settings.toml"):
  log_warn("No EaglerXServer settings.toml found, copying from default config...")
  shutil.copy(DEF_CONF+"/eag_settings.toml", PLUG_DIR+"/eaglerxserver/settings.toml")

eag_toml = tomlkit.parse(read_file(PLUG_DIR+"/eaglerxserver/settings.toml"))

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
write_file_w(PLUG_DIR+"/eaglerxserver/settings.toml", tomlkit.dumps(eag_toml))
log_norm("Updated EaglerXServer settings.toml")

# ------------------- #

EAG_LISTENER = addon_conf['eagListener']

if not file_exists(PLUG_DIR+"/eaglerxserver/listeners.toml"):
  log_warn("No EaglerXServer listeners.toml found, copying from default config...")
  shutil.copy(DEF_CONF+"/eag_listeners.toml", PLUG_DIR+"/eaglerxserver/listeners.toml")

eag_list_toml = tomlkit.parse(read_file(PLUG_DIR+"/eaglerxserver/listeners.toml"))
eag_motd = [minimsg_to_leg(MOTD1), minimsg_to_leg(MOTD2)]
log_fine(f"EaglerXServer MOTD: {eag_motd}")
eag_list_toml['listener_list'][0]['server_motd'] = eag_motd

for setting in EAG_LISTENER:
  log_finer(f"{setting}: {EAG_LISTENER[setting]}")
  eag_list_toml['listener_list'][0][setting] = EAG_LISTENER[setting]


log_finest(eag_list_toml)
write_file_w(PLUG_DIR+"/eaglerxserver/listeners.toml", tomlkit.dumps(eag_list_toml))
log_norm("Updated EaglerXServer listeners.toml")

## ----------------------------------- ##

FLOOD_DBS = {
  'sqlite': {
    "url": "https://ci.opencollab.dev/job/GeyserMC/job/Floodgate/job/fix-weird-via-issue/lastSuccessfulBuild/artifact/database/sqlite/build/libs/floodgate-sqlite-database.jar",
    "file": "floodgate-sqlite-database.jar"
  },
  'mysql': {
    "url": "https://ci.opencollab.dev/job/GeyserMC/job/Floodgate/job/fix-weird-via-issue/lastSuccessfulBuild/artifact/database/mysql/build/libs/floodgate-mysql-database.jar",
    "file": "floodgate-mysql-database.jar"
  },
  'mongo': {
    "url": "https://ci.opencollab.dev/job/GeyserMC/job/Floodgate/job/fix-weird-via-issue/lastSuccessfulBuild/artifact/database/mongo/build/libs/floodgate-mongo-database.jar",
    "file": "floodgate-mongo-database.jar"
  }
}


FLOOD = addon_conf["floodgate"]
FLOOD_DISCONNECT = addon_conf["floodDisconnect"]
FLOOD_PLAYER_LINK = addon_conf["floodPlayerLink"]

check_dir(PLUG_DIR+"/floodgate")

if not file_exists(PLUG_DIR+"/floodgate/config.yml"):
  log_warn("No Floodgate config.yml found, copying from default config...")
  shutil.copy(DEF_CONF+"/floodgate.yml", PLUG_DIR+"/floodgate/config.yml")

flood_yaml = yaml.load(read_file(PLUG_DIR+"/floodgate/config.yml"))

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

with open(PLUG_DIR+"/floodgate/config.yml", "w") as file:
  yaml.dump(flood_yaml, file)
  log_norm("Updated Floodgate config.yml")

check_dir(PLUG_DIR+"/Geyser-Velocity")

if not file_exists(PLUG_DIR+"/floodgate/key.pem"):
  log_norm("No Floodgate key.pem found, generating one...")
  key = os.urandom(16)
  with open(PLUG_DIR+"/floodgate/key.pem", "wb") as f:
    f.write(key)
  shutil.copy(PLUG_DIR+"/floodgate/key.pem", PLUG_DIR+"/Geyser-Velocity/key.pem")

if FLOOD_PLAYER_LINK['enable-own-linking']:
  log_norm("Floodgate local player linking is enabled, checking database jar...")
  type = FLOOD_PLAYER_LINK['type']
  if not file_exists(PLUG_DIR+"/floodgate/"+FLOOD_DBS[type]['file']):
    log_warn("No Floodgate database jar found, downloading...")
    download_file(FLOOD_DBS[type]['url'], FLOOD_DBS[type]['file'], PLUG_DIR+"/floodgate")

## ------------------------ ##

GEYSER_BEDROCK = addon_conf['geyserBedrock']
GEYSER_REMOTE = addon_conf['geyserRemote']
GEYSER = addon_conf['geyser']

if not file_exists(PLUG_DIR+"/Geyser-Velocity/config.yml"):
  log_warn("No Geyser config.yml found, copying from default config...")
  shutil.copy(DEF_CONF+"/geyser.yml", PLUG_DIR+"/Geyser-Velocity/config.yml")

geyser_yaml = yaml.load(read_file(PLUG_DIR+"/Geyser-Velocity/config.yml"))

geyser_yaml['metrics']['uuid'] = UUID
geyser_yaml['max-players'] = MAX_PLAYERS
geyser_yaml['bedrock']['server-name'] = SERVER_NAME
geyser_yaml['bedrock']['motd1'] = re.sub(r'<[^>]+>', '', MOTD1)
geyser_yaml['bedrock']['motd2'] = re.sub(r'<[^>]+>', '', MOTD2)

for setting in GEYSER_BEDROCK:
  log_finer(f"{setting}: {GEYSER_BEDROCK[setting]}")
  geyser_yaml['bedrock'][setting] = GEYSER_BEDROCK[setting]

for setting in GEYSER_REMOTE:
  log_finer(f"{setting}: {GEYSER_REMOTE[setting]}")
  geyser_yaml['remote'][setting] = GEYSER_REMOTE[setting]

for setting in GEYSER:
  log_finer(f"{setting}: {GEYSER[setting]}")
  geyser_yaml[setting] = GEYSER[setting]

with open(PLUG_DIR+"/Geyser-Velocity/config.yml", "w") as file:
  yaml.dump(geyser_yaml, file)
  log_norm("Updated Geyser config.yml")

## ----------------------------------- ##

check_dir(PLUG_DIR+"/viabackwards")
check_dir(PLUG_DIR+"/viarewind")

if not file_exists(PLUG_DIR+"/viabackwards/config.yml"):
  log_warn("No ViaBackwards config.yml found, copying from default config...")
  shutil.copy(DEF_CONF+"/viabackwards.yml", PLUG_DIR+"/viabackwards/config.yml")

if not file_exists(PLUG_DIR+"/viarewind/config.yml"):
  log_warn("No ViaRewind config.yml found, copying from default config...")
  shutil.copy(DEF_CONF+"/viarewind.yml", PLUG_DIR+"/viarewind/config.yml")
