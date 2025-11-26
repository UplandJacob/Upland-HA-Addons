#! /usr/bin/env python3
# config.py

import json
import logging
from colorlog import ColoredFormatter
import os
import random
import re
from typing import Any
import requests
import shutil
import string
import tomlkit
import uuid
from ruamel.yaml import YAML

ROOT_DIR = ''
CONF_DIR = ROOT_DIR + '/config'
SERV_DIR = CONF_DIR + '/server'
PLUG_DIR = SERV_DIR + '/plugins'
DEF_CONF = ROOT_DIR + '/default_config'

LOG_LEVEL = 2
log = logging.getLogger()
def set_log_level(level: int):
  global LOG_LEVEL
  LOG_LEVEL = level # pyright: ignore[reportConstantRedefinition]
  if level >= 4: log.setLevel(logging.DEBUG)
  elif level >= 2: log.setLevel(logging.INFO)
  elif level == 1: log.setLevel(logging.WARNING)
  else: log.setLevel(logging.ERROR)
set_log_level(2)

formatter = ColoredFormatter("%(log_color)s%(levelname)s: %(message)s", log_colors={
  "DEBUG":"white","INFO":"green","WARNING":"yellow","ERROR":"red","CRITICAL":"bold_red"
})
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

def check_dir(path: str):
  if not os.path.isdir(path):
    log.warning(f"Directory {path} does not exist, creating...")
    os.makedirs(path, exist_ok=True)

def file_exists(path: str) -> bool:
  log_debug_x(f"Checking if file {path} exists...")
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

def log_debug_x(msg: Any):
  if LOG_LEVEL >= 5: log.debug(msg)
def log_info_x(msg: Any):
  if LOG_LEVEL >= 3: log.info("\033[0m"+msg)


if not file_exists(ROOT_DIR+"/data/options.json"):
  log.warning("options.json file not found. Is this addon running outside of Home Assistant? Converting YAML to JSON...")
  ymlConf = yaml.load(read_file(DEF_CONF+"/config.yaml"))
  write_file_w(ROOT_DIR+"/data/options.json", json.dumps(ymlConf["options"], indent=2))

with open(ROOT_DIR+"/data/options.json", "r") as file:
  addon_conf = json.load(file)

set_log_level(addon_conf['logLevel'])


def minimsg_to_leg(minimessage: str):
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
    result = result.replace(f'<#{hex_color}>', "&b")
  # Handle gradients
  gradient_pattern = r'<gradient[^>]*>.*?</gradient>'
  result = re.sub(gradient_pattern, lambda m: "&b" + re.sub(r'<[^>]+>', '', m.group(0)), result)
  for mini, legacy in {**colors, **formats}.items():
    result = result.replace(mini, legacy)
  result = re.sub(r'<click[^>]*>.*?</click>', lambda m: re.sub(r'<[^>]+>', '', m.group(0)), result)
  result = re.sub(r'<hover[^>]*>.*?</hover>', lambda m: re.sub(r'<[^>]+>', '', m.group(0)), result)
  result = re.sub(r'<[^>]+>', '', result)
  return result

## ------------------ ##

check_dir(CONF_DIR+"/server")

if not file_exists(CONF_DIR+"/uuid.txt"):
  log.warning("No uuid.txt found, generating one...")
  new_uuid = str(uuid.uuid4())
  log_debug_x(f"Generated UUID: {new_uuid}")
  write_file_a(CONF_DIR+"/uuid.txt", new_uuid)
UUID = read_file(CONF_DIR+"/uuid.txt")
log.info(f"Server UUID: {UUID}")

if not file_exists(SERV_DIR+"/forwarding.secret.txt"):
  log.warning("No forwarding.secret.txt found, generating one...")
  new_secret = ''.join(random.choices(string.ascii_letters+string.digits, k=10))
  log_info_x(f"Generated forwarding secret: {new_secret}")
  write_file_a(SERV_DIR+"/forwarding.secret.txt", new_secret)

if not file_exists(CONF_DIR+"/plugins.yaml"):
  log.warning("No plugins.yaml found, copying from default config...")
  shutil.copy(DEF_CONF+"/plugins.yaml", CONF_DIR+"/plugins.yaml")

vers_data = yaml.load(read_file(CONF_DIR+"/plugins.yaml"))

# load default plugins.yaml to update the packaged_plugins section
vers_default = yaml.load(read_file(DEF_CONF+"/plugins.yaml"))
vers_data['packaged_plugins'] = vers_default['packaged_plugins']
vers_data['velocity'] = vers_default['velocity']


MAX_PLAYERS = addon_conf['max_players']
SERVER_NAME = addon_conf['server_name']

def parse_pl_holds(inp: str):
  inp = re.sub(r"{se?rv(er)?(_?na?me?)?}", SERVER_NAME, inp, flags=re.IGNORECASE)
  inp = re.sub(r"{max_?pl(a?ye?)?r?s}", str(MAX_PLAYERS), inp, flags=re.IGNORECASE)
  return inp

MOTD1 = parse_pl_holds(addon_conf['motd1'])
MOTD2 = parse_pl_holds(addon_conf['motd2'])

log_info_x(f"Max Players: {MAX_PLAYERS}")
log_info_x(f"Server Name: {SERVER_NAME}")
log_info_x(f"MOTD1: {MOTD1}")
log_info_x(f"MOTD2: {MOTD2}")

HAPROXY = addon_conf['haproxy']


## ----------------------------------- ##

VEL_ROOT_CONFIG = addon_conf['rootConfig']
VEL_SERVERS = addon_conf['servers']
VEL_SERV_ATT_JOIN_ORD = addon_conf['serverAttemptJoinOrder']
VEL_FORCED_HOSTS = addon_conf['forcedHosts']
VEL_ADVANCED = addon_conf['adv']

if not file_exists(SERV_DIR+"/velocity.toml"):
  log.warning("No velocity.toml found, copying from default config...")
  shutil.copy(DEF_CONF+"/velocity.toml", SERV_DIR+"/velocity.toml")

# Load the TOML file
vel_toml = tomlkit.parse(read_file(SERV_DIR+"/velocity.toml"))


for setting in VEL_ROOT_CONFIG:
  log.debug(f"{setting}: {VEL_ROOT_CONFIG[setting]}")
  vel_toml[setting] = VEL_ROOT_CONFIG[setting]

vel_toml['show-max-players'] = MAX_PLAYERS
vel_toml['motd'] = MOTD1+"\n"+MOTD2
vel_toml['haproxy-protocol'] = HAPROXY

vel_toml['servers'] = {}
for i in range(len(VEL_SERVERS)):
  server = VEL_SERVERS[i]['name']
  addr = VEL_SERVERS[i]['address']
  log.debug(f"{server}: {addr}")
  vel_toml['servers'][server] = addr

log.debug(f"try: {VEL_SERV_ATT_JOIN_ORD}")
vel_toml['servers']['try'] = VEL_SERV_ATT_JOIN_ORD

vel_toml['forced-hosts'] = {}
for i in range(len(VEL_FORCED_HOSTS)):
  host = VEL_FORCED_HOSTS[i]['hostname']
  serv_names = VEL_FORCED_HOSTS[i]['servNames']
  log.debug(f"{host}: {serv_names}")
  if host == 'null':
    log_info_x('Skipping null host')
    continue
  vel_toml['forced-hosts'][host] = serv_names

for setting in VEL_ADVANCED:
  log.debug(f"{setting}: {VEL_ADVANCED[setting]}")
  vel_toml['advanced'][setting] = VEL_ADVANCED[setting]

log_debug_x(vel_toml)

# Save the updated TOML file
write_file_w(SERV_DIR+"/velocity.toml", tomlkit.dumps(vel_toml))
log.info("Updated velocity.toml")

## ----------------------------------- ##

def plug_placeholders(txt: str, data: dict[str, str]) -> str:
  for placeholder in re.findall(r'\{(\w+)\}', txt):
    log.debug(f"Found placeholder: {placeholder}")
    txt = txt.replace(f"{{{placeholder}}}", str(data[placeholder]))
  return txt


def download_file(url: str, f_name: str, path: str=PLUG_DIR):
  log.info(f"Downloading {f_name} from {url}...")
  response = requests.get(url)
  if response.status_code == 200:
    with open(path+"/"+f_name, "wb") as file:
      file.write(response.content)
    log_info_x("File downloaded successfully!")
    return True
  else:
    log.warning("Failed to download the file.")
    return False

if vers_data['current_installed_urls'] is None: vers_data['current_installed_urls'] = {}
vel_url = plug_placeholders(vers_data['velocity']['url'], vers_data['velocity'])

# velocity download
if not file_exists(SERV_DIR+"/velocity.jar") or 'velocity' not in vers_data['current_installed_urls'] or vers_data['current_installed_urls']['velocity'] != vel_url:
  log.warning("Downloading Velocity...")
  if download_file(vel_url, 'velocity.jar', SERV_DIR):
    log_info_x("Velocity downloaded successfully!")
    vers_data['current_installed_urls']['velocity'] = vel_url
  else:
    log.error("Failed to download Velocity")
    exit(1)


check_dir(PLUG_DIR)
check_dir(PLUG_DIR+"/Geyser-Velocity/extensions")
check_dir(PLUG_DIR+"/Geyser-Velocity/packs")

all_plug_nms = []

def download_plugins(main_group: str, override_group: str = ''):
  log.info(f"Downloading plugins from '{main_group}' with overrides from '{override_group}'")
  if vers_data[main_group] is None: return

  plug_group = dict(vers_data[main_group])
  over_group = {} if override_group == '' or vers_data[override_group] is None else vers_data[override_group]
  for plugin in plug_group:
    log_info_x(f"Plugin: {plugin}")
    if plugin in all_plug_nms:
      log.error(f"Plugin name '{plugin}' already used. If you are trying to override a plugin's settings, use the override section.")
      continue
    all_plug_nms.append(plugin)
    plugin_data = plug_group[plugin]
    log_debug_x(f"Plugin data: {plugin_data}")

    over_data = {} if plugin not in over_group else over_group[plugin]
    log_debug_x(f"Override data: {over_data}")
    for key in over_data:
      log.debug(f"Overriding {key} with {over_data[key]}")
      plugin_data[key] = over_data[key]
    log.debug(f"Plugin data: {plugin_data}")
    if plugin_data is None: continue

    path = "/"
    if 'path' in plugin_data and plugin_data['path'] is not None:
      path = str(plugin_data['path'])
      if not path.startswith("/"): path = "/"+path
      if not path.endswith("/"): path += "/"
    log.debug(f"Path: {path}")

    f_nm = plug_placeholders(plugin_data['file'], plugin_data)
    full_jar_nm = PLUG_DIR+path+f_nm
    jar_present = file_exists(full_jar_nm)
    enabled = True if 'enabled' not in plugin_data else plugin_data['enabled']
    if not enabled:
      log.info(f"Plugin '{plugin}' is disabled, skipping...")
      if jar_present:
        log_info_x("Disabling existing jar...")
        os.rename(full_jar_nm, full_jar_nm+".disabled")
      continue
    if file_exists(full_jar_nm+".disabled"):
      log_info_x("Enabling existing jar...")
      os.rename(full_jar_nm+".disabled", full_jar_nm)
      jar_present = True

    url = plug_placeholders(plugin_data['url'], plugin_data)
    urls = vers_data['current_installed_urls']

    if plugin in urls and urls[plugin] == url and jar_present:
      log_info_x("Plugin up to date")
      continue
    if download_file(url, f_nm, PLUG_DIR+path):
      vers_data['current_installed_urls'][plugin] = url
      old_fl = vers_data['current_installed_files'].get(plugin, None)
      if old_fl is not None and old_fl != f_nm and file_exists(PLUG_DIR+path+old_fl):
        log_info_x(f"Removing old jar ('{old_fl}') for '{plugin}' because it is now '{f_nm}'")
        os.remove(PLUG_DIR+path+old_fl)
      vers_data['current_installed_files'][plugin] = f_nm
    else: 
      log.error(f"Failed to download plugin {plugin}")
      continue

if 'current_installed_urls' not in vers_data or vers_data['current_installed_urls'] is None: vers_data['current_installed_urls'] = {}
if 'current_installed_files' not in vers_data or vers_data['current_installed_files'] is None: vers_data['current_installed_files'] = {}

download_plugins('packaged_plugins', 'packaged_plugins_overrides')
download_plugins('custom_plugins')

with open(CONF_DIR+"/plugins.yaml", "w") as file:
  yaml.dump(vers_data, file)
  log.info("Updated plugins.yaml")

## ----------------------------------- ##

EAG_CONFIG = addon_conf['eagConfig']
EAG_SKIN = addon_conf['eagSkins']
EAG_VOICE = addon_conf['eagVoice']
EAG_UP_SERVICE = addon_conf['eagUpdateService']
EAG_UP_CHECKER = addon_conf['eagUpdateChecker']

check_dir(PLUG_DIR+"/eaglerxserver")
if not file_exists(PLUG_DIR+"/eaglerxserver/settings.toml"):
  log.warning("No EaglerXServer settings.toml found, copying from default config...")
  shutil.copy(DEF_CONF+"/eag_settings.toml", PLUG_DIR+"/eaglerxserver/settings.toml")

eag_toml = tomlkit.parse(read_file(PLUG_DIR+"/eaglerxserver/settings.toml"))

eag_toml['server_uuid'] = UUID
eag_toml['server_name'] = SERVER_NAME

for setting in EAG_CONFIG:
  log.debug(f"{setting}: {EAG_CONFIG[setting]}")
  eag_toml[setting] = EAG_CONFIG[setting]

for setting in EAG_SKIN:
  log.debug(f"{setting}: {EAG_SKIN[setting]}")
  eag_toml['skin_service'][setting] = EAG_SKIN[setting]

for setting in EAG_VOICE:
  log.debug(f"{setting}: {EAG_VOICE[setting]}")
  eag_toml['voice_service'][setting] = EAG_VOICE[setting]

for setting in EAG_UP_SERVICE:
  log.debug(f"{setting}: {EAG_UP_SERVICE[setting]}")
  eag_toml['update_service'][setting] = EAG_UP_SERVICE[setting]

for setting in EAG_UP_CHECKER:
  log.debug(f"{setting}: {EAG_UP_CHECKER[setting]}")
  eag_toml['update_checker'][setting] = EAG_UP_CHECKER[setting]


log_debug_x(eag_toml)
write_file_w(PLUG_DIR+"/eaglerxserver/settings.toml", tomlkit.dumps(eag_toml))
log.info("Updated EaglerXServer settings.toml")

# ------------------- #

EAG_LISTENER = addon_conf['eagListener']

if not file_exists(PLUG_DIR+"/eaglerxserver/listeners.toml"):
  log.warning("No EaglerXServer listeners.toml found, copying from default config...")
  shutil.copy(DEF_CONF+"/eag_listeners.toml", PLUG_DIR+"/eaglerxserver/listeners.toml")

eag_list_toml = tomlkit.parse(read_file(PLUG_DIR+"/eaglerxserver/listeners.toml"))
eag_motd = [minimsg_to_leg(MOTD1), minimsg_to_leg(MOTD2)]
log_info_x(f"EaglerXServer MOTD: {eag_motd}")
eag_list_toml['listener_list'][0]['server_motd'] = eag_motd # pyright: ignore[reportArgumentType]

for setting in EAG_LISTENER:
  log.debug(f"{setting}: {EAG_LISTENER[setting]}")
  eag_list_toml['listener_list'][0][setting] = EAG_LISTENER[setting] # pyright: ignore[reportArgumentType]

eag_list_toml['listener_list'][0]['dual_stack_haproxy_detection'] = HAPROXY # pyright: ignore[reportArgumentType]

log_debug_x(eag_list_toml)
write_file_w(PLUG_DIR+"/eaglerxserver/listeners.toml", tomlkit.dumps(eag_list_toml))
log.info("Updated EaglerXServer listeners.toml")

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
FLOOD_PLAYER_LINK = addon_conf["floodPlayerLink"]

check_dir(PLUG_DIR+"/floodgate")

if not file_exists(PLUG_DIR+"/floodgate/config.yml"):
  log.warning("No Floodgate config.yml found, copying from default config...")
  shutil.copy(DEF_CONF+"/floodgate.yml", PLUG_DIR+"/floodgate/config.yml")

flood_yaml = yaml.load(read_file(PLUG_DIR+"/floodgate/config.yml"))

for setting in FLOOD:
  log.debug(f"{setting}: {FLOOD[setting]}")
  flood_yaml[setting] = FLOOD[setting]

for setting in FLOOD_PLAYER_LINK:
  log.debug(f"{setting}: {FLOOD_PLAYER_LINK[setting]}")
  flood_yaml['player-link'][setting] = FLOOD_PLAYER_LINK[setting]

flood_yaml['metrics']['uuid'] = UUID

with open(PLUG_DIR+"/floodgate/config.yml", "w") as file:
  yaml.dump(flood_yaml, file)
  log.info("Updated Floodgate config.yml")

check_dir(PLUG_DIR+"/Geyser-Velocity")

if not file_exists(PLUG_DIR+"/floodgate/key.pem"):
  log.info("No Floodgate key.pem found, generating one...")
  key = os.urandom(16)
  with open(PLUG_DIR+"/floodgate/key.pem", "wb") as f:
    f.write(key)
  shutil.copy(PLUG_DIR+"/floodgate/key.pem", PLUG_DIR+"/Geyser-Velocity/key.pem")

if FLOOD_PLAYER_LINK['enable-own-linking']:
  log.info("Floodgate local player linking is enabled, checking database jar...")
  type = FLOOD_PLAYER_LINK['type']
  if not file_exists(PLUG_DIR+"/floodgate/"+FLOOD_DBS[type]['file']):
    log.warning("No Floodgate database jar found, downloading...")
    download_file(FLOOD_DBS[type]['url'], FLOOD_DBS[type]['file'], PLUG_DIR+"/floodgate")

## ------------------------ ##

GEYSER_BEDROCK = addon_conf['geyserBedrock']
GEYSER_JAVA = addon_conf['geyserJava']
GEYSER = addon_conf['geyser']

if not file_exists(PLUG_DIR+"/Geyser-Velocity/config.yml"):
  log.warning("No Geyser config.yml found, copying from default config...")
  shutil.copy(DEF_CONF+"/geyser.yml", PLUG_DIR+"/Geyser-Velocity/config.yml")

geyser_yaml = yaml.load(read_file(PLUG_DIR+"/Geyser-Velocity/config.yml"))

geyser_yaml['motd']['max-players'] = MAX_PLAYERS
geyser_yaml['motd']['primary-motd'] = re.sub(r'<[^>]+>', '', MOTD1)
geyser_yaml['motd']['secondary-motd'] = re.sub(r'<[^>]+>', '', MOTD2)

geyser_yaml['gameplay']['server-name'] = SERVER_NAME
geyser_yaml['java']['auth-type'] = addon_conf['geyserAuthType']
geyser_yaml['advanced']['java']['use-haproxy-protocol'] = HAPROXY

for setting in GEYSER_BEDROCK:
  log.debug(f"{setting}: {GEYSER_BEDROCK[setting]}")
  geyser_yaml['advanced']['bedrock'][setting] = GEYSER_BEDROCK[setting]

for setting in GEYSER_JAVA:
  log.debug(f"{setting}: {GEYSER_JAVA[setting]}")
  geyser_yaml['advanced']['java'][setting] = GEYSER_JAVA[setting]

for setting in GEYSER:
  log.debug(f"{setting}: {GEYSER[setting]}")
  geyser_yaml['gameplay'][setting] = GEYSER[setting]

with open(PLUG_DIR+"/Geyser-Velocity/config.yml", "w") as file:
  yaml.dump(geyser_yaml, file)
  log.info("Updated Geyser config.yml")

## ----------------------------------- ##

check_dir(PLUG_DIR+"/viabackwards")
check_dir(PLUG_DIR+"/viarewind")

if not file_exists(PLUG_DIR+"/viabackwards/config.yml"):
  log.warning("No ViaBackwards config.yml found, copying from default config...")
  shutil.copy(DEF_CONF+"/viabackwards.yml", PLUG_DIR+"/viabackwards/config.yml")

if not file_exists(PLUG_DIR+"/viarewind/config.yml"):
  log.warning("No ViaRewind config.yml found, copying from default config...")
  shutil.copy(DEF_CONF+"/viarewind.yml", PLUG_DIR+"/viarewind/config.yml")
