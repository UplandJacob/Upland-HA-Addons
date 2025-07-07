#! /usr/bin/env python3
# config.py

import json
import logging
from colorlog import ColoredFormatter
import os
import random
import re
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
with open(ROOT_DIR+"/data/options.json", "r") as file:
  addon_conf = json.load(file)

LOG_LEVEL = addon_conf['logLevel']
log = logging.getLogger()
if LOG_LEVEL >= 4: log.setLevel(logging.DEBUG)
elif LOG_LEVEL >= 2: log.setLevel(logging.INFO)
elif LOG_LEVEL == 1: log.setLevel(logging.WARNING)
else: log.setLevel(logging.ERROR)

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

def file_exists(path):
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

def log_debug_x(msg: str):
  if LOG_LEVEL >= 5: log.debug(msg)
def log_info_x(msg: str):
  if LOG_LEVEL >= 3: log.info("\033[0m"+msg)

## ------------------ ##

check_dir(CONF_DIR+"/server")

if not file_exists(CONF_DIR+"/uuid.txt"):
  log.warning("No uuid.txt found, generating one...")
  new_uuid = str(uuid.uuid4())
  log_debug_x(f"Generated UUID: {new_uuid}")
  write_file_a(CONF_DIR+"/uuid.txt", new_uuid)
UUID = read_file(CONF_DIR+"/uuid.txt")
log.info(f"Server UUID: {UUID}")

if not file_exists(CONF_DIR+"/plugins.yaml"):
  log.warning("No plugins.yaml found, copying from default config...")
  shutil.copy(DEF_CONF+"/plugins.yaml", CONF_DIR+"/plugins.yaml")

vers_data = yaml.load(read_file(CONF_DIR+"/plugins.yaml"))

# load default plugins.yaml to update the packaged_plugins section
vers_default = yaml.load(read_file(DEF_CONF+"/plugins.yaml"))
vers_data['packaged_plugins'] = vers_default['packaged_plugins']
vers_data['server'] = vers_default['server']


MAX_PLAYERS = addon_conf['max_players']
SERVER_NAME = addon_conf['server_name']

def parse_pl_holds(inp):
  inp = re.sub(r"{se?rv(er)?(_?na?me?)?}", SERVER_NAME, inp, flags=re.IGNORECASE)
  inp = re.sub(r"{max_?pl(a?ye?)?r?s}", str(MAX_PLAYERS), inp, flags=re.IGNORECASE)
  return inp

MOTD1 = parse_pl_holds(addon_conf['motd1'])
MOTD2 = parse_pl_holds(addon_conf['motd2'])

log_info_x(f"Max Players: {MAX_PLAYERS}")
log_info_x(f"Server Name: {SERVER_NAME}")
log_info_x(f"MOTD1: {MOTD1}")
log_info_x(f"MOTD2: {MOTD2}")

if not file_exists(SERV_DIR+"/eula.txt"):
  shutil.copy(DEF_CONF+"/eula.txt", SERV_DIR+"/eula.txt")


EULA = addon_conf['eula']
log_info_x(f"EULA: {EULA}")
if not EULA:
  log.error("You must accept the EULA to run the server!") 
with open(SERV_DIR+"/eula.txt", "r") as file:
  lines = file.readlines()
lines[2] = f"eula={EULA}\n"
with open(SERV_DIR+"/eula.txt", "w") as file:
  file.writelines(lines)
log.info("Updated eula.txt")

## ----------------------------------- ##

if not file_exists(SERV_DIR+"/server.properties"):
  log.warning("server.properties not found, copying from default_config...")
  shutil.copy(DEF_CONF+"/server.properties", SERV_DIR+"/server.properties")

if not file_exists(SERV_DIR+"/spigot.yml"):
  log.warning("spigot.yml not found. Copying from default_config...")
  shutil.copy(DEF_CONF+"/spigot.yml", SERV_DIR+"/spigot.yml")

SERV_SET = addon_conf["server"]
SERV_SET["max-players"] = MAX_PLAYERS
SERV_SET["motd"] = '"'+MOTD1+"\\n"+MOTD2+'"'
SERV_SET["server-name"] = SERVER_NAME

with open(SERV_DIR+"/server.properties", "r") as file:
  serv_props = file.readlines()

for i, line in enumerate(serv_props):
  stripped_line = line.strip()
  if "=" not in stripped_line or stripped_line.startswith("#"): continue # Ignore comments
  log_debug_x(stripped_line)
  key = stripped_line.split("=", 1)[0]
  log_debug_x(key)
  if key in SERV_SET:
    serv_props[i] = f"{key}={SERV_SET[key]}\n"

with open(SERV_DIR+"/server.properties", "w") as file:
    file.writelines(serv_props)

## ----------------------------------- ##

check_dir(PLUG_DIR)

def plug_placeholders(txt: str, data: dict) -> str:
  for placeholder in re.findall(r'\{(\w+)\}', txt):
    log.debug(f"Found placeholder: {placeholder}")
    txt = txt.replace(f"{{{placeholder}}}", str(data[placeholder]))
  return txt


def download_file(url: str, f_name: str, path=PLUG_DIR):
  log.info(f"Downloading {f_name} from {url}...")
  response = requests.get(url)
  if not path.endswith("/"): path += "/"
  if response.status_code == 200:
    with open(path+f_name, "wb") as file:
      file.write(response.content)
    log_info_x("File downloaded successfully!")
    return True
  else:
    log.warning("Failed to download the file.")
    return False

# server download
if not file_exists(SERV_DIR+"/server.jar"):
  log.warning("No server.jar found, downloading...")
  download_file(plug_placeholders(vers_data['server']['url'], vers_data['server']), 'server.jar', SERV_DIR)

def download_plugins(main_group: str, override_group: str):
  log.info(f"Downloading plugins from '{main_group}' with overrides from '{override_group}'")
  if vers_data[main_group] is None: return

  plug_group = dict(vers_data[main_group])
  over_group = {} if override_group == '' or vers_data[override_group] is None else vers_data[override_group]
  for plugin in plug_group:
    log_info_x(f"Plugin: {plugin}")
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
      path = plugin_data['path']
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
    if vers_data['current_installed_urls'] is None: vers_data['current_installed_urls'] = {}
    urls = vers_data['current_installed_urls']

    if plugin in urls and urls[plugin] == url and jar_present:
      log_info_x("Plugin up to date")
      continue
    if download_file(url, f_nm, PLUG_DIR+path): vers_data['current_installed_urls'][plugin] = url

download_plugins('packaged_plugins', 'packaged_plugins_overrides')
download_plugins('custom_plugins', '')

## ----------------------------------- ##

if not file_exists(SERV_DIR+"/spigot.yml"):
  log.warning("spigot.yml doesn't exist. Copying from default_config...")
  shutil.copy(DEF_CONF+"/spigot.yml", SERV_DIR+"/spigot.yml")

check_dir(SERV_DIR+"/config")
if not file_exists(SERV_DIR+"/config/paper-global.yml"):
  log.warning("paper-global.yml doesn't exist. Copying from default_config...")
  shutil.copy(DEF_CONF+"/paper-global.yml", SERV_DIR+"/config/paper-global.yml")

check_dir(PLUG_DIR+"/BungeeGuard")
if not file_exists(PLUG_DIR+"/BungeeGuard/config.yml"):
  log.warning("Bungeeguard config.yml doesn't exist. Copying from default_config...")
  shutil.copy(DEF_CONF+"/bungeeguard.yml", PLUG_DIR+"/BungeeGuard/config.yml")

spigot_yaml = yaml.load(read_file(SERV_DIR+"/spigot.yml"))
paper_yaml = yaml.load(read_file(SERV_DIR+"/config/paper-global.yml"))
bungee_guard = yaml.load(read_file(PLUG_DIR+"/BungeeGuard/config.yml"))

FOR_EN = addon_conf["enableForward"]; BUNGUARD = addon_conf["useBungeeGuard"]; BUNCORD = addon_conf["bungeecordMode"]
proxy_set_bungee = "using BungeeCord mode NOT RECOMMENDED-NOT SECURE" if not BUNCORD else "Velocity mode"
proxy_set_guard = "enabled" if BUNGUARD else f"disabled-NOT recommended - {proxy_set_bungee}"
log_info_x("Forwarding disabled" if not FOR_EN else f"Forwarding enabled -- BungeeGuard: {proxy_set_guard}")

if vers_data["packaged_plugins_overrides"] is None: vers_data["packaged_plugins_overrides"] = {}
if "bungeeguard" not in vers_data["packaged_plugins_overrides"]: vers_data["packaged_plugins_overrides"]["bungeeguard"] = {}

vers_data["packaged_plugins_overrides"]["bungeeguard"]["enabled"] = FOR_EN and BUNGUARD
spigot_yaml["settings"]["bungeecord"] = FOR_EN and (BUNGUARD or BUNCORD)
paper_yaml["proxies"]["velocity"]["enabled"] = FOR_EN and not BUNGUARD and not BUNCORD

paper_yaml["proxies"]["bungee-cord"]["online-mode"] = addon_conf["proxyOnlineMode"]
paper_yaml["proxies"]["velocity"]["online-mode"] = addon_conf["proxyOnlineMode"]
paper_yaml["proxies"]["velocity"]["secret"] = addon_conf["forwardingSecret"]
bungee_guard["allowed-tokens"][0] = addon_conf["forwardingSecret"]

with open(SERV_DIR+"/spigot.yml", "w") as file:
  yaml.dump(spigot_yaml, file)
  log.info("Updated spigot.yml")

with open(SERV_DIR+"/config/paper-global.yml", "w") as file:
  yaml.dump(paper_yaml, file)
  log.info("Updated config/paper-global.yml")

with open(PLUG_DIR+"/BungeeGuard/config.yml", "w") as file:
  yaml.dump(bungee_guard, file)
  log.info("Updated BungeeGuard config.yml")


with open(CONF_DIR+"/plugins.yaml", "w") as file:
  yaml.dump(vers_data, file)
  log.info("Updated plugins.yaml")

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

# if not file_exists(PLUG_DIR+"/floodgate/key.pem"):
#   log.info("No Floodgate key.pem found, generating one...")
#   key = os.urandom(16)
#   with open(PLUG_DIR+"/floodgate/key.pem", "wb") as f:
#     f.write(key)
#   shutil.copy(PLUG_DIR+"/floodgate/key.pem", PLUG_DIR+"/Geyser-Velocity/key.pem")

if FLOOD_PLAYER_LINK['enable-own-linking']:
  log.info("Floodgate local player linking is enabled, checking database jar...")
  type = FLOOD_PLAYER_LINK['type']
  if not file_exists(PLUG_DIR+"/floodgate/"+FLOOD_DBS[type]['file']):
    log.warning("No Floodgate database jar found, downloading...")
    download_file(FLOOD_DBS[type]['url'], FLOOD_DBS[type]['file'], PLUG_DIR+"/floodgate")

## ------------------------ ##



## ----------------------------------- ##

check_dir(PLUG_DIR+"/viaversion")
check_dir(PLUG_DIR+"/viabackwards")
check_dir(PLUG_DIR+"/viarewind")

if not file_exists(PLUG_DIR+"/viaversion/config.yml"):
  log.warning("No ViaVersion config.yml found, copying from default config...")
  shutil.copy(DEF_CONF+"/viaversion.yml", PLUG_DIR+"/viaversion/config.yml")

if not file_exists(PLUG_DIR+"/viabackwards/config.yml"):
  log.warning("No ViaBackwards config.yml found, copying from default config...")
  shutil.copy(DEF_CONF+"/viabackwards.yml", PLUG_DIR+"/viabackwards/config.yml")

if not file_exists(PLUG_DIR+"/viarewind/config.yml"):
  log.warning("No ViaRewind config.yml found, copying from default config...")
  shutil.copy(DEF_CONF+"/viarewind.yml", PLUG_DIR+"/viarewind/config.yml")
