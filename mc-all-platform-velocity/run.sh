#!/usr/bin/with-contenv bashio
CONFIG_PATH=/data/options.json

logGreen() {
  echo -e "\033[32m$1\033[0m"
}
logLine() {
  echo -e ". \n"
}
getConfig() {
  jq --raw-output "$1" $CONFIG_PATH
}
logLine
logLine
#---------------------- velocity.toml -----------------------
#------- get config --------
TEST=$(getConfig '.rootConfig')
logGreen "TEST: "
echo -e "$TEST"
logLine
logLine


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
logLine
logGreen "velocity servers raw:"
echo -e "$VEL_SERVERS"
logLine
vel_servers_JSON=$(echo $VEL_SERVERS | sed 's/}/},/g' | sed '$ s/,$//' | awk '{print "[" $0 "]"}')
logGreen "velocity servers JSON:"
echo -e "$vel_servers_JSON"
logLine
vel_servers=""
vel_servers_length=$(echo "$vel_servers_JSON" | jq '. | length')
for (( i=0; i<$vel_servers_length; i++ )); do
  name=$(echo "$vel_servers_JSON" | jq -r ".[$i].name")
  addr=$(echo "$vel_servers_JSON" | jq -r ".[$i].address")
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
echo -e "config-version = \"2.7\"\nbind = \"0.0.0.0:25565\"\n$vel_root_config\n\n[servers]\n$vel_servers\n\ntry = [\n$vel_serv_ord\n]\n\n[forced-hosts]\n$vel_forced_hosts\n\n[advanced]\n$vel_advanced\n" > velocity.toml
logGreen "velocity.toml:"
cat velocity.toml
logLine
logLine

# --------------------------------- EAGLERCRAFT ----------------------------------------
#------- get config --------
EAG_CONFIG=$(getConfig 'eagConfig')
EAG_AUTH=$(getConfig 'eagAuth')
# ----------- plugins/eaglerxvelocity/settings.yml -----------
logGreen "eagConfig JSON:"
echo -e "$EAG_CONFIG"
logLine
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
logGreen "eagConfig:"
echo -e "$eag_config"
logLine
# -------   SAVE --------
echo -e "$eag_config" > plugins/eaglerxvelocity/settings.yml
logGreen "plugins/eaglerxvelocity/settings.yml:"
cat plugins/eaglerxvelocity/settings.yml
logLine
logLine

# ------------ plugins/eaglerxvelocity/authservice.yml ------------
logGreen "eagAuth JSON:"
echo -e "$EAG_AUTH"
logLine
eag_auth=$(echo "$EAG_AUTH" | jq -r 'to_entries | .[] | "\(.key): \(( if .value | type == "string" then "\"\(.value)\"\n" else "\(.value)\n" end ))"')
logGreen "eagAuth:"
echo -e "$eag_auth"
logLine
# ------  SAVE --------
echo -e "$eag_auth" > plugins/eaglerxvelocity/authservice.yml
logGreen "plugins/eaglerxvelocity/authservice.yml:"
cat plugins/eaglerxvelocity/authservice.yml
logLine
logLine


java -Xms1G -Xmx1G -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:MaxInlineLevel=15 -Deaglerxvelocity.stfu=true -jar velocity.jar
