#!/usr/bin/with-contenv bashio
CONFIG_PATH=/data/options.json

logGreen() {
  echo -e "\033[32m$1\033[0m"
}
echo ""
echo ""
#-------- get config ------------
VEL_ROOT_CONFIG=$(bashio::config 'rootConfig')
VEL_SERVERS=$(bashio::config 'servers')
VEL_SERV_ATT_JOIN_ORD=$(jq --raw-output '.serverAttemptJoinOrder' $CONFIG_PATH)
echo $VEL_SERV_ATT_JOIN_ORD
# main section
echo ""
echo $VEL_ROOT_CONFIG
echo ""
# vel_root_config=$(echo "$VEL_ROOT_CONFIG" | jq -r 'to_entries | .[] | "\(.key) = \(.value)"')
vel_root_config=$(echo "$VEL_ROOT_CONFIG" | jq -r 'to_entries | .[] | "\(.key) = \((if .value | type == "string" then "\"\(.value)\"" else .value end))"')
echo $vel_root_config
echo ""
# '[servers]' section
echo ""
echo $VEL_SERVERS
vel_servers_JSON=$(echo $VEL_SERVERS | sed 's/}/},/g' | sed '$ s/,$//' | awk '{print "[" $0 "]"}')
echo $vel_servers_JSON
vel_servers=""
vel_servers_length=$(echo "$vel_servers_JSON" | jq '. | length')
for (( i=0; i<$vel_servers_length; i++ )); do
  name=$(echo "$vel_servers_JSON" | jq -r ".[$i].name")
  addr=$(echo "$vel_servers_JSON" | jq -r ".[$i].address")
  vel_servers+="$name = \"$addr\"\n"
  vel_servers+="\n"
done
echo $vel_servers

vel_serv_ord=""
vel_serv_ord_length=$(echo "$VEL_SERV_ATT_JOIN_ORD" | jq '. | length')
for (( i=0; i<$vel_serv_ord_length; i++ )); do
  name=$(echo "$VEL_SERV_ATT_JOIN_ORD" | jq -r ".[$i]")
  vel_serv_ord+="    \"$name\",\n"
done
echo $vel_serv_ord

echo -e "config-version = \"2.7\"\nbind = \"0.0.0.0:25565\"\n$vel_root_config\n[servers]\n$vel_servers\n\ntry = [\n$vel_serv_ord\n]\n" > velocity.toml
logGreen "velocity.toml:"
cat velocity.toml

# DEBUG_MODE=$(bashio::config 'debugMode')






java -Xms1G -Xmx1G -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:MaxInlineLevel=15 -Deaglerxvelocity.stfu=true -jar velocity.jar
