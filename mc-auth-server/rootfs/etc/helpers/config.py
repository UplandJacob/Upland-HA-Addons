#! /usr/bin/env python3
# config.py

import logging
from colorlog import ColoredFormatter

import requests
import os, shutil
from os.path import join as j_pth
import re, uuid

import json
from ruamel.yaml import YAML

from typing import Any


ROOT_DIR = '/'
CONF_DIR = j_pth(ROOT_DIR, 'config')
SERV_DIR = j_pth(CONF_DIR, 'server')
PLUG_DIR = j_pth(SERV_DIR, 'plugins')
DEF_CONF = j_pth(ROOT_DIR, 'default_config')

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

def read_file(path: str) -> str:
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

OPT_FILE = j_pth(ROOT_DIR, "data/options.json")
if not file_exists(OPT_FILE):
  log.warning("options.json file not found. Is this addon running outside of Home Assistant? Converting YAML to JSON...")
  ymlConf = yaml.load(read_file(j_pth(DEF_CONF, "config.yaml")))
  write_file_w(OPT_FILE, json.dumps(ymlConf["options"], indent=2))

with open(OPT_FILE, "r") as file:
  addon_conf = json.load(file)

set_log_level(addon_conf['logLevel'])

## ------------------ ##

check_dir(SERV_DIR)
UUID_FILE = j_pth(CONF_DIR, "uuid.txt")
if not file_exists(UUID_FILE):
  log.warning("No uuid.txt found, generating one...")
  new_uuid = str(uuid.uuid4())
  log_debug_x(f"Generated UUID: {new_uuid}")
  write_file_a(UUID_FILE, new_uuid)
UUID = read_file(UUID_FILE)
log.info(f"Server UUID: {UUID}")

PLUG_FILE = j_pth(CONF_DIR, "plugins.yaml")
DEF_PLUG_FILE = j_pth(DEF_CONF, "plugins.yaml")
if not file_exists(PLUG_FILE):
  log.warning("No plugins.yaml found, copying from default config...")
  shutil.copy(DEF_PLUG_FILE, PLUG_FILE)

vers_data = yaml.load(read_file(PLUG_FILE))

# load default plugins.yaml to update the packaged_plugins section
vers_default = yaml.load(read_file(DEF_PLUG_FILE))
vers_data['packaged_plugins'] = vers_default['packaged_plugins']
vers_data['server'] = vers_default['server']


MAX_PLAYERS = addon_conf['max_players']
SERVER_NAME = addon_conf['server_name']

def parse_pl_holds(inp: str) -> str:
  inp = re.sub(r"{se?rv(er)?(_?na?me?)?}", SERVER_NAME, inp, flags=re.IGNORECASE)
  inp = re.sub(r"{max_?pl(a?ye?)?r?s}", str(MAX_PLAYERS), inp, flags=re.IGNORECASE)
  return inp

MOTD1 = parse_pl_holds(addon_conf['motd1'])
MOTD2 = parse_pl_holds(addon_conf['motd2'])

log_info_x(f"Max Players: {MAX_PLAYERS}")
log_info_x(f"Server Name: {SERVER_NAME}")
log_info_x(f"MOTD1: {MOTD1}")
log_info_x(f"MOTD2: {MOTD2}")

EULA_FILE = j_pth(SERV_DIR, "eula.txt")
if not file_exists(EULA_FILE):
  shutil.copy(j_pth(DEF_CONF, "eula.txt"), EULA_FILE)

EULA = addon_conf['eula']
log_info_x(f"EULA: {EULA}")
if not EULA:
  log.error("You must accept the EULA to run the server!") 
with open(EULA_FILE, "r") as file:
  lines = file.readlines()
lines[2] = f"eula={EULA}\n"
with open(EULA_FILE, "w") as file:
  file.writelines(lines)
log.info("Updated eula.txt")

## ----------------------------------- ##
SERV_PROP_FILE = j_pth(SERV_DIR, "server.properties")
if not file_exists(SERV_PROP_FILE):
  log.warning("server.properties not found, copying from default_config...")
  shutil.copy(j_pth(DEF_CONF, "server.properties"), SERV_PROP_FILE)

SERV_SET = addon_conf["server"]
SERV_SET["max-players"] = MAX_PLAYERS
SERV_SET["motd"] = '"'+MOTD1+"\\n"+MOTD2+'"'
SERV_SET["server-name"] = SERVER_NAME

with open(SERV_PROP_FILE, "r") as file:
  serv_props = file.readlines()

for i, line in enumerate(serv_props):
  stripped_line = line.strip()
  if "=" not in stripped_line or stripped_line.startswith("#"): continue # Ignore comments
  log_debug_x(stripped_line)
  key = stripped_line.split("=", 1)[0]
  log_debug_x(key)
  if key in SERV_SET:
    serv_props[i] = f"{key}={SERV_SET[key]}\n"

with open(SERV_PROP_FILE, "w") as file:
    file.writelines(serv_props)

## ----------------------------------- ##

check_dir(PLUG_DIR)

def plug_placeholders(txt: str, data: dict[str, str]) -> str:
  for placeholder in re.findall(r'\{(\w+)\}', txt):
    log.debug(f"Found placeholder: {placeholder}")
    txt = txt.replace(f"{{{placeholder}}}", str(data[placeholder]))
  return txt


def download_file(url: str, f_name: str, path: str = PLUG_DIR):
  log.info(f"Downloading {f_name} from {url}...")
  response = requests.get(url)
  if response.status_code == 200:
    with open(j_pth(path, f_name), "wb") as file:
      file.write(response.content)
    log_info_x("File downloaded successfully!")
    return True
  else:
    log.warning("Failed to download the file.")
    return False

if vers_data['current_installed_urls'] is None: vers_data['current_installed_urls'] = {}
serv_url = plug_placeholders(vers_data['server']['url'], vers_data['server'])

# server download
if not file_exists(j_pth(SERV_DIR, "server.jar")) or 'server' not in vers_data['current_installed_urls'] or vers_data['current_installed_urls']['server'] != serv_url:
  log.warning("Downloading server...")
  if download_file(serv_url, 'server.jar', SERV_DIR):
    log_info_x("Server downloaded successfully!")
    vers_data['current_installed_urls']['server'] = serv_url
  else:
    log.error("Failed to download server")
    exit(1)

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

    path = ""
    if 'path' in plugin_data and plugin_data['path'] is not None:
      path = str(plugin_data['path'])
    log.debug(f"Path: {path}")

    f_nm = plug_placeholders(plugin_data['file'], plugin_data)
    full_jar_nm = j_pth(PLUG_DIR, path, f_nm)
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
    if download_file(url, f_nm, j_pth(PLUG_DIR, path)):
      vers_data['current_installed_urls'][plugin] = url
      old_fl = vers_data['current_installed_files'].get(plugin, None)
      if old_fl is not None and old_fl != f_nm and file_exists(j_pth(PLUG_DIR, path, old_fl)):
        log_info_x(f"Removing old jar ('{old_fl}') for '{plugin}' because it is now '{f_nm}'")
        os.remove(j_pth(PLUG_DIR, path, old_fl))
      vers_data['current_installed_files'][plugin] = f_nm
    else: 
      log.error(f"Failed to download plugin {plugin}")
      continue

## ----------------------------------- ##

SPIGOT_FILE = j_pth(SERV_DIR, "spigot.yml")
if not file_exists(SPIGOT_FILE):
  log.warning("spigot.yml doesn't exist. Copying from default_config...")
  shutil.copy(j_pth(DEF_CONF, "spigot.yml"), SPIGOT_FILE)

check_dir(j_pth(SERV_DIR, "config"))
PAPER_FILE = j_pth(SERV_DIR, "config/paper-global.yml")
if not file_exists(PAPER_FILE):
  log.warning("paper-global.yml doesn't exist. Copying from default_config...")
  shutil.copy(DEF_CONF+"/paper-global.yml", PAPER_FILE)

check_dir(j_pth(PLUG_DIR, "BungeeGuard"))
BUNGEE_GUARD_FILE = j_pth(PLUG_DIR, "BungeeGuard/config.yaml")
if not file_exists(BUNGEE_GUARD_FILE):
  log.warning("Bungeeguard config.yml doesn't exist. Copying from default_config...")
  shutil.copy(j_pth(DEF_CONF, "bungeeguard.yml"), BUNGEE_GUARD_FILE)

spigot_yaml = yaml.load(read_file(SPIGOT_FILE))
paper_yaml = yaml.load(read_file(PAPER_FILE))
bungee_guard = yaml.load(read_file(BUNGEE_GUARD_FILE))

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

with open(SPIGOT_FILE, "w") as file:
  yaml.dump(spigot_yaml, file)
  log.info("Updated spigot.yml")

with open(PAPER_FILE, "w") as file:
  yaml.dump(paper_yaml, file)
  log.info("Updated config/paper-global.yml")

with open(BUNGEE_GUARD_FILE, "w") as file:
  yaml.dump(bungee_guard, file)
  log.info("Updated BungeeGuard config.yml")

if 'current_installed_urls' not in vers_data or vers_data['current_installed_urls'] is None: vers_data['current_installed_urls'] = {}
if 'current_installed_files' not in vers_data or vers_data['current_installed_files'] is None: vers_data['current_installed_files'] = {}

download_plugins('packaged_plugins', 'packaged_plugins_overrides')
download_plugins('custom_plugins')

with open(PLUG_FILE, "w") as file:
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

check_dir(j_pth(PLUG_DIR, "floodgate"))
FLOOD_FILE = j_pth(PLUG_DIR, "floodgate/config.yml")
if not file_exists(FLOOD_FILE):
  log.warning("No Floodgate config.yml found, copying from default config...")
  shutil.copy(j_pth(DEF_CONF, "floodgate.yml"), FLOOD_FILE)

flood_yaml = yaml.load(read_file(FLOOD_FILE))

for setting in FLOOD:
  log.debug(f"{setting}: {FLOOD[setting]}")
  flood_yaml[setting] = FLOOD[setting]

for setting in FLOOD_PLAYER_LINK:
  log.debug(f"{setting}: {FLOOD_PLAYER_LINK[setting]}")
  flood_yaml['player-link'][setting] = FLOOD_PLAYER_LINK[setting]

flood_yaml['metrics']['uuid'] = UUID

with open(FLOOD_FILE, "w") as file:
  yaml.dump(flood_yaml, file)
  log.info("Updated Floodgate config.yml")

# if not file_exists(j_pth(PLUG_DIR, "floodgate/key.pem")):
#   log.info("No Floodgate key.pem found, generating one...")
#   key = os.urandom(16)
#   with open(j_pth(PLUG_DIR, "floodgate/key.pem"), "wb") as f:
#     f.write(key)
#   shutil.copy(j_pth(PLUG_DIR, "floodgate/key.pem"), PLUG_DIR+"/Geyser-Velocity/key.pem")

if FLOOD_PLAYER_LINK['enable-own-linking']:
  log.info("Floodgate local player linking is enabled, checking database jar...")
  type = FLOOD_PLAYER_LINK['type']
  if not file_exists(j_pth(PLUG_DIR, "floodgate", FLOOD_DBS[type]['file'])):
    log.warning("No Floodgate database jar found, downloading...")
    download_file(FLOOD_DBS[type]['url'], FLOOD_DBS[type]['file'], j_pth(PLUG_DIR, "floodgate"))

## ----------------------------------- ##

check_dir(j_pth(PLUG_DIR, "ViaVersion"))
check_dir(j_pth(PLUG_DIR, "ViaBackwards"))
check_dir(j_pth(PLUG_DIR, "ViaRewind"))

if not file_exists(j_pth(PLUG_DIR, "ViaVersion/config.yml")):
  log.warning("No ViaVersion config.yml found, copying from default config...")
  shutil.copy(j_pth(DEF_CONF, "viaversion.yml"), j_pth(PLUG_DIR, "ViaVersion/config.yml"))

if not file_exists(j_pth(PLUG_DIR, "ViaBackwards/config.yml")):
  log.warning("No ViaBackwards config.yml found, copying from default config...")
  shutil.copy(j_pth(DEF_CONF, "viabackwards.yml"), j_pth(PLUG_DIR, "ViaBackwards/config.yml"))

if not file_exists(j_pth(PLUG_DIR, "ViaRewind/config.yml")):
  log.warning("No ViaRewind config.yml found, copying from default config...")
  shutil.copy(j_pth(DEF_CONF, "viarewind.yml"), j_pth(PLUG_DIR, "ViaRewind/config.yml"))
