#!/usr/bin/with-contenv bashio

logGreen() {
  echo -e "\033[32m$1\033[0m"
}

#-------- get config ------------
VEL_ROOT_CONFIG=$(bashio::config 'rootConfig')
VEL_SERVERS=$(bashio::config 'servers')
VEL_SERV_ATT_JOIN_ORD=$(bashio::config 'serverAttemptJoinOrder')
# main section
vel_root_config=$(echo "$VEL_ROOT_CONFIG" | jq -r 'to_entries | .[] | "\(.key): \(.value)"')
# '[servers]' section
vel_servers_JSON=$(echo $VEL_SERVERS | sed 's/}/},/g' | sed '$ s/,$//' | awk '{print "[" $0 "]"}')
servers=""
servers_length=$(echo "$vel_servers_JSON" | jq '. | length')
for (( i=0; i<$servers_length; i++ )); do
  name=$(echo "$vel_servers_JSON" | jq -r ".[$i].name")
  addr=$(echo "$vel_servers_JSON" | jq -r ".[$i].address")
  relays+="$name = address=$addr\n"
  relays+="\n"
done


echo -e "config-version = \"2.7\"\nbind = \"0.0.0.0:25565\"\n$vel_root_config\n[servers]\n$servers" > velocity.toml
logGreen "velocity.toml:"
cat velocity.toml

# DEBUG_MODE=$(bashio::config 'debugMode')






java -Xms1G -Xmx1G -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:MaxInlineLevel=15 -Deaglerxvelocity.stfu=true -jar velocity.jar
