#!/usr/bin/with-contenv bashio

logGreen() {
  echo -e "\033[32m$1\033[0m"
}
echo ""
echo ""
#-------- get config ------------
VEL_ROOT_CONFIG=$(bashio::config 'rootConfig')
VEL_SERVERS=$(bashio::config 'servers')
VEL_SERV_ATT_JOIN_ORD=$(bashio::config 'serverAttemptJoinOrder')
echo $VEL_SERV_ATT_JOIN_ORD
# main section
vel_root_config=$(echo "$VEL_ROOT_CONFIG" | jq -r 'to_entries | .[] | "\(.key) = \(.value)"')
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




echo -e "config-version = \"2.7\"\nbind = \"0.0.0.0:25565\"\n$vel_root_config\n[servers]\n$vel_servers\n\ntry = [\n" > velocity.toml
logGreen "velocity.toml:"
cat velocity.toml

# DEBUG_MODE=$(bashio::config 'debugMode')






java -Xms1G -Xmx1G -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:MaxInlineLevel=15 -Deaglerxvelocity.stfu=true -jar velocity.jar
