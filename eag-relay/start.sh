#!/usr/bin/with-contenv bashio

echo ""
echo ""

#get config
RELAY_CONFIG=$(bashio::config 'relayConfig')
RELAYS=$(bashio::config 'relays')

bashio::log.green "relayConfig JSON:"
echo $RELAY_CONFIG
echo ""

config=$(echo "$RELAY_CONFIG" | jq -r 'to_entries | .[] | "\(.key): \(.value)"')
echo -e "[EaglerSPRelay]\nport: 6699\naddress: 0.0.0.0\n$config" > relayConfig.ini

echo ""
bashio::log.green "relayConfig.ini:"
cat relayConfig.ini
echo ""

echo ""
echo -e "\033[32mrelays JSON unformatted:\033[0m"
echo $RELAYS
echo ""

relayJSON=$(echo $RELAYS | sed 's/}/},/g' | sed '$ s/,$//' | awk '{print "[" $0 "]"}')

bashio::log.green "relays JSON formatted:"
echo $relayJSON
echo ""

length=$(echo "$relayJSON" | jq '. | length')

relays=""
for (( i=0; i<$length; i++ )); do
  type=$(echo "$relayJSON" | jq -r ".[$i].type")
  url=$(echo "$relayJSON" | jq -r ".[$i].url")
  user=$(echo "$relayJSON" | jq -r ".[$i].username // empty")
  cred=$(echo "$relayJSON" | jq -r ".[$i].credential // empty")

  relays+="[$type]\nurl=$url\n"
  [ -n "$user" ] && relays+="username=$user\n"
  [ -n "$cred" ] && relays+="credential=$cred\n"
  relays+="\n"
done

echo -e "$relays" > relays.txt

bashio::log.green "relays.txt:"
cat relays.txt

echo ""
echo ""
bashio::log.green "Starting Eaglercraft relay..."
echo ""

#start relay (run.sh file is downloaded with relay)
./run.sh 


