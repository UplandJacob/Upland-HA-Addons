#!/usr/bin/with-contenv bashio

# simple functions
logGreen() {
  echo -e "\033[32m$1\033[0m"
}
logRed() {
  echo -e "\033[31m$1\033[0m"
}
logLine() {
  echo -e ". \n"
}
getConfig() {
  jq --raw-output "$1" /data/options.json
}

if [[ ! -f "/config/uuid.txt" ]]; then
  logGreen "No uuid.txt found, generating one..."
  uuid=$(uuidgen)
  echo "$uuid" > /config/uuid.txt
  logGreen "new server uuid: $uuid"
fi
UUID=$(</config/uuid.txt)

if [[ ! -f "/config/forwarding.secret.txt" ]]; then
  logGreen "No forwarding.secret.txt found, generating one..."
  secret=$(head -1 <(fold -w 10  <(tr -dc 'a-zA-Z0-9' < /dev/urandom)))
  echo "$secret" > /config/forwarding.secret.txt
  logGreen "new server forwarding secret: $secret"
fi

need_kick=false
need_kick_reason=()

################################################
logGreen "Generating config files..."
#---------------------- velocity.toml -----------------------
#------- get config --------
VEL_ROOT_CONFIG=$(getConfig '.rootConfig')
VEL_SERVERS=$(getConfig '.servers')
VEL_SERV_ATT_JOIN_ORD=$(getConfig '.serverAttemptJoinOrder')
VEL_FORCED_HOSTS=$(getConfig '.forcedHosts')
VEL_ADVANCED=$(getConfig '.advanced')
# main section -----------
logLine
logGreen "velocity rootConfig JSON:"
echo -e "$VEL_ROOT_CONFIG"
logLine
vel_root_config=$(echo "$VEL_ROOT_CONFIG" | jq -r 'to_entries | .[] | "\(.key) = \((if .value | type == "string" then "\"\(.value)\"" else .value end))"')
logGreen "velocity rootConfig formatted:"
echo -e "$vel_root_config"
logLine
# '[servers]' section --------------
logGreen "velocity servers JSON:"
echo -e "$VEL_SERVERS"
logLine
vel_servers=""
vel_servers_length=$(echo "$VEL_SERVERS" | jq '. | length')
for (( i=0; i<$vel_servers_length; i++ )); do
  name=$(echo "$VEL_SERVERS" | jq -r ".[$i].name")
  addr=$(echo "$VEL_SERVERS" | jq -r ".[$i].address")
  vel_servers+="$name = \"$addr\"\n"
  vel_servers+="\n"
done
logGreen "velocity servers formatted:"
echo -e "$vel_servers"
logLine
# try ------
logGreen "velocity serverAttemptJoinOrder JSON array:"
echo $VEL_SERV_ATT_JOIN_ORD
logLine
vel_serv_ord=""
vel_serv_ord_length=$(echo "$VEL_SERV_ATT_JOIN_ORD" | jq '. | length')
for (( i=0; i<$vel_serv_ord_length; i++ )); do
  name=$(echo "$VEL_SERV_ATT_JOIN_ORD" | jq -r ".[$i]")
  vel_serv_ord+="    \"$name\",\n"
done
logGreen "velocity serverAttemptJoinOrder formatted:"
echo -e "$vel_serv_ord"
logLine
# [forced-hosts] section --------------
logGreen "velocity forcedHosts JSON:"
echo -e "$VEL_FORCED_HOSTS"
logLine
vel_forced_hosts=""
vel_forced_hosts_length=$(echo "$VEL_FORCED_HOSTS" | jq '. | length')
for (( i=0; i<$vel_servers_length; i++ )); do
  host=$(echo "$VEL_FORCED_HOSTS" | jq -r ".[$i].hostname")
  servs=$(echo "$VEL_FORCED_HOSTS" | jq -r ".[$i].servNames")
  vel_forced_hosts+="\"$host\" = [\n"
  servs_len=$(echo "$servs" | jq '. | length')
  for (( j=0; j<$servs_len; j++ )); do
    name=$(echo "$servs" | jq -r ".[$j]")
    vel_forced_hosts+="    \"$name\",\n"
  done
  vel_forced_hosts+="]\n"
done
logGreen "velocity forcedHosts formatted:"
echo -e "$vel_forced_hosts"
logLine
# [advanced] section --------------
logGreen "velocity advanced JSON:"
echo $VEL_ADVANCED
logLine
vel_advanced=$(echo "$VEL_ADVANCED" | jq -r 'to_entries | .[] | "\(.key) = \((if .value | type == "string" then "\"\(.value)\"" else .value end))"')
logGreen "velocity advanced formatted:"
echo -e "$vel_advanced"
logLine
# -------    SAVE --------
echo -e "config-version = \"2.7\"\nbind = \"0.0.0.0:25565\"\nforwarding-secret-file = \"/config/forwarding.secret.txt\"\n$vel_root_config\n\n[servers]\n$vel_servers\n\ntry = [\n$vel_serv_ord\n]\n\n[forced-hosts]\n$vel_forced_hosts\n\n[advanced]\n$vel_advanced\n" > velocity.toml
logGreen "velocity.toml:"
cat velocity.toml
logLine
logLine

# --------------------------------- EAGLERCRAFT ----------------------------------------
#------- get config --------
EAG_CONFIG=$(getConfig '.eagConfig')
EAG_AUTH=$(getConfig '.eagAuth')
EAG_LISTENER=$(getConfig '.eagListener')
EAG_RELAYS=$(getConfig '.eagRelays')
# ----------- plugins/eaglerxvelocity/settings.yml -----------

eag_config=$(echo "$EAG_CONFIG" | jq -r '
  to_entries | .[] | "\(.key): \(
    if .value | type == "string" then
      (if .value | test("^\\$\\{.*\\}$") then
        .value
      else
        "\"\(.value)\""
      end)
    elif .value | type == "array" then
      (.value | map("\n  - \(.)") | join("\n"))
    elif .value | type == "object" then
      (.value | to_entries | map("\n  \(.key): \(.value)") | join("\n"))
    else
      .value
    end
  )" 
')

logLine
# -------   SAVE --------
echo -e "skin_cache_db_uri: jdbc:sqlite:/config/eaglercraft_skins_cache.db\n$eag_config" > plugins/eaglerxvelocity/settings.yml
logGreen "plugins/eaglerxvelocity/settings.yml:"
cat plugins/eaglerxvelocity/settings.yml
logLine

# ------------ plugins/eaglerxvelocity/authservice.yml ------------

eag_auth=$(echo "$EAG_AUTH" | jq -r 'to_entries | .[] | "\(.key): \(( if .value | type == "string" then "\"\(.value)\"\n" else "\(.value)\n" end ))"')

logLine
# ------  SAVE --------
echo -e "auth_db_uri: jdbc:sqlite:/config/eaglercraft_auths.db\n$eag_auth" > plugins/eaglerxvelocity/authservice.yml
logGreen "plugins/eaglerxvelocity/authservice.yml:"
cat plugins/eaglerxvelocity/authservice.yml

# ------------ plugins/eaglerxvelocity/listeners.yml ------------
if [[ ! -f "/config/eag_listeners.yml" ]]; then
  logGreen "no eag_listeners.yml file found. Copying from default.."
  cp /default_config/eag_listeners.yml /config/eag_listeners.yml
fi
logGreen "copying eag_listeners.yml from config..."
cp /config/eag_listeners.yml /plugins/eaglerxvelocity/listeners.yml

logGreen "eag listener JSON:"
echo -e "$EAG_LISTENER"
keys=$(echo "$EAG_LISTENER" | jq -r 'keys[]')

for key in $keys; do
  value=$(echo "$EAG_LISTENER" | jq -c --arg k "$key" '.[$k]')
  yq -iy ".listener_01.$key = $value" /plugins/eaglerxvelocity/listeners.yml
done

logGreen "/plugins/eaglerxvelocity/listeners.yml"
cat /plugins/eaglerxvelocity/listeners.yml
logLine
logLine

# ------------------- plugins/eaglerxvelocity/ice_servers.yml -----------
echo ""
logGreen "Eaglercraft ICE relay servers JSON:"
echo -e "$EAG_RELAYS"
echo ""

length=$(echo "$EAG_RELAYS" | jq '. | length')
relays="voice_servers_passwd:\n"
relays_no_cred="voice_servers_no_passwd:\n"
for (( i=0; i<$length; i++ )); do
  url=$(echo "$EAG_RELAYS" | jq -r ".[$i].url")
  user=$(echo "$EAG_RELAYS" | jq -r ".[$i].username // empty")
  pass=$(echo "$EAG_RELAYS" | jq -r ".[$i].password // empty")
  
  if [ -n "$user" ] && [ -n "$pass" ]; then
    relays+="  relay_$i:\n    url: '$url'\n    username: '$user'\n    password: '$pass'\n\n"
  else
    relays_no_cred+="   - '$url'\n"
  fi
  
done
echo -e "$relays_no_cred\n\n$relays" > plugins/eaglerxvelocity/ice_servers.yml
logGreen "Eagler ICE servers"
cat plugins/eaglerxvelocity/ice_servers.yml
#---------------------------------------- BEDROCK -----------------------------------
#------- get config --------
FLOOD_CONF=$(getConfig '.floodgate')
FLOOD_DISC=$(getConfig '.floodDisconnect')
FLOOD_PLAYER=$(getConfig '.floodPlayerLink')
GEYSER_BEDROCK=$(getConfig '.geyserBedrock')
GEYSER_REMOTE=$(getConfig '.geyserRemote')
GEYSER=$(getConfig '.geyser')
GEYSER_ADVANCED=$(getConfig '.geyserAdvanced')
# ------------ plugins/floodgate/config.yml ------------
logGreen "floodgate JSON:"
echo -e "$FLOOD_CONF"
flood_conf=$(echo "$FLOOD_CONF" | jq -r 'to_entries | .[] | "\(.key): \(( if .value | type == "string" then "\"\(.value)\"\n" else "\(.value)\n" end ))"')

logGreen "floodgate disconnect JSON:"
echo -e "$FLOOD_DISC"
flood_disc=$(echo "$FLOOD_DISC" | jq -r 'to_entries | .[] | "  \(.key): \(( if .value | type == "string" then "\"\(.value)\"\n" else "\(.value)\n" end ))"')

logGreen "floodgate player link JSON:"
echo -e "$FLOOD_PLAYER"
flood_player=$(echo "$FLOOD_PLAYER" | jq -r 'to_entries | .[] | "  \(.key): \(( if .value | type == "string" then "\"\(.value)\"\n" else "\(.value)\n" end ))"')

logLine
# ------  SAVE --------
echo -e "key-file-name: 'key.pem'\n\ndiaconnect:\n$flood_disc\n\nplayer-link:\n$flood_player\n\n$flood_conf\nmetrics:\n  enabled: false\n  uuid: $UUID\n\nconfig-version: 3" > plugins/floodgate/config.yml
logGreen "plugins/floodgate/config.yml"
cat plugins/floodgate/config.yml
# ------------ plugins/Geyser-Velocity/config.yml ------------
logGreen "geyser bedrock JSON:"
echo -e "$GEYSER_BEDROCK"
geyser_bedrock=$(echo "$GEYSER_BEDROCK" | jq -r 'to_entries | .[] | "  \(.key): \(( if .value | type == "string" then "\"\(.value)\"\n" else "\(.value)\n" end ))"')

logGreen "geyser remote JSON:"
echo -e "$GEYSER_REMOTE"
geyser_remote=$(echo "$GEYSER_REMOTE" | jq -r 'to_entries | .[] | "  \(.key): \(( if .value | type == "string" then "\"\(.value)\"\n" else "\(.value)\n" end ))"')

logGreen "geyser JSON:"
echo -e "$GEYSER"
geyser=$(echo "$GEYSER" | jq -r 'to_entries | .[] | "\(.key): \(( if .value | type == "string" then "\"\(.value)\"\n" else "\(.value)\n" end ))"')

logGreen "geyser advanced JSON:"
echo -e "$GEYSER_ADVANCED"
geyser_advanced=$(echo "$GEYSER_ADVANCED" | jq -r 'to_entries | .[] | "\(.key): \(( if .value | type == "string" then "\"\(.value)\"\n" else "\(.value)\n" end ))"')

logLine
# ------  SAVE --------
echo -e "bedrock:\n  port: 19132\n  clone-remote-port: false\n$geyser_bedrock\n\nremote:\n  address: auto\n  port: 25565\n$geyser_remote\n\nfloodgate-key-file: key.pem\n$geyser\n\nmetrics:\n  enabled: false\n  uuid: $UUID\n\n$geyser_advanced\n\nconfig-version: 4" > plugins/Geyser-Velocity/config.yml
logGreen "plugins/Geyser-Velocity/config.yml"
cat plugins/Geyser-Velocity/config.yml

#----- packs and extentions ------
if [[ ! -d "/config/geyser" ]]; then
  logGreen "creating 'geyser' folder..."
  mkdir /config/geyser
fi
if [[ ! -d "/config/geyser/packs" ]]; then
  logGreen "creating 'geyser/packs' folder..."
  mkdir /config/geyser/packs
fi
if [[ ! -d "/config/geyser/extensions" ]]; then
  logGreen "creating 'geyser/extensions' folder..."
  mkdir /config/geyser/extensions
fi
logGreen "copying Geyser packs..."
rsync -av --ignore-existing /config/geyser/packs/ /plugins/Geyser-Velocity/packs/
logGreen "copying Geyser extensions..."
rsync -av --ignore-existing /config/geyser/extensions/ /plugins/Geyser-Velocity/extensions/

# check for key.pem
if [[ ! -f "/config/geyser/key.pem" ]]; then
  logGreen "no key.pem file found. Will generate one."
  need_kick=true
  need_kick_reason+=("key.pem")
fi
# floodgate folder for DB jars and config
if [[ ! -d "/config/geyser/floodgate" ]]; then
  logGreen "creating 'geyser/floodgate' folder..."
  mkdir /config/geyser/floodgate
fi
# local linking
if [[ jq -r "$FLOOD_PLAYER.enable-own-linking" = true ]]; then
  if [[ jq -r "$FLOOD_PLAYER.type" = "mysql" ]]; then
    if [[ ! -f "/config/geyser/floodgate/floodgate-mysql-database.jar" ]]; then
      logRed "missing floodgate-mysql-database.jar for Floodgate DB type 'mysql'"
      exit 0
    fi
     if [[ ! -d "/config/geyser/floodgate/mysql" ]]; then
      mkdir /config/geyser/floodgate/mysql
    fi
    if [[ ! -f "/config/geyser/floodgate/mysql/mysql.yml" ]]; then
      need_kick=true
      need_kick_reason+=("floodgate/mysql.yml")
    fi
  elif [[ jq -r "$FLOOD_PLAYER.type" = "mongo" ]]; then
    if [[ ! -f "/config/geyser/floodgate/floodgate-mongo-database.jar" ]]; then
      logRed "missing floodgate-mongo-database.jar for Floodgate DB type 'mongo'"
      exit 0
    fi
    if [[ ! -d "/config/geyser/floodgate/mongo" ]]; then
      mkdir /config/geyser/floodgate/mongo
    fi
    if [[ ! -f "/config/geyser/floodgate/mongo/mongo.yml" ]]; then
      need_kick=true
      need_kick_reason+=("floodgate/mongo.yml")
    fi
  elif [[ jq -r "$FLOOD_PLAYER.type" = "sqlite" ]]; then
    if [[ ! -f "/config/geyser/floodgate/floodgate-sqlite-database.jar" ]]; then
      logRed "missing floodgate-sqlite-database.jar for Floodgate DB type 'sqlite'"
      exit 0
    fi
    ln -s /config/geyser/floodgate/linked-players.db /plugins/floodgate/linked-players.db
  fi
  
  rsync -av --ignore-existing /config/geyser/floodgate /plugins/floodgate
fi
#----------------------------------------- VIABACKWARDS --------------------------------
# ------------ plugins/viabackwards/config.yml ------------
if [[ ! -f "/config/viabackwards.yml" ]]; then
  logGreen "no viabackwards.yml file found. Copying from default.."
  cp /default_config/viabackwards.yml /config/viabackwards.yml
fi
logGreen "copying viabackwards.yml from config..."
cp /config/viabackwards.yml /plugins/viabackwards/config.yml

#----------------------------------------- VIAREWIND --------------------------------
# ------------ plugins/viarewind/config.yml ------------
# TODO


####### -------------------------- finalize -------------------------------------
logLine


if [[ "$need_kick" = true ]]; then
  logGreen "Temporarlily starting proxy for reason(s): $need_kick_reason"
  ./kickstart.sh "help for help!"
  if [[ "$need_kick_reason" =~ "key.pem" ]]; then
    logGreen "copying key.pem to config folder..."
    cp /plugins/floodgate/key.pem /config/geyser/key.pem
  fi
fi

logGreen "copying key.pem into plugin folders..."
cp /config/geyser/key.pem /plugins/Geyser-Velocity/key.pem
cp /config/geyser/key.pem /plugins/floodgate/key.pem




if [[ -f "/config/server-icon.png" ]]; then
  logGreen "server-icon.png found"
  cp /config/server-icon.png /server-icon.png
else
  logGreen "no server-icon.png found"
fi

RAM_ALLOCATE=$(getConfig '.allocatedRAM_MB')
logGreen "Allocated RAM: $RAM_ALLOCATE MB"
logLine
logGreen "Starting..............."
java -Xms${RAM_ALLOCATE}m -Xmx${RAM_ALLOCATE}m -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:MaxInlineLevel=15 -Deaglerxvelocity.stfu=true -jar velocity.jar
