#!/usr/bin/with-contenv bashio

echo ""
echo ""

logGreen() {
  echo -e "\033[32m$1\033[0m"
}
getConfig() {
  jq --raw-output "$1" /data/options.json
}

#get config
RELAY_CONFIG=$(getConfig '.relayConfig')
RELAYS=$(getConfig '.relays')

AUTO_RESTART=$(bashio::config 'autoRestart')
DEBUG_MODE=$(bashio::config 'debugMode')

logGreen "relayConfig JSON:"
echo $RELAY_CONFIG
echo ""

config=$(echo "$RELAY_CONFIG" | jq -r 'to_entries | .[] | "\(.key): \(.value)"')
echo -e "[EaglerSPRelay]\nport: 6699\naddress: 0.0.0.0\n$config" > relayConfig.ini

echo ""
logGreen "relayConfig.ini:"
cat relayConfig.ini
echo ""

echo ""
logGreen "relays JSON:"
echo $RELAYS
echo ""

length=$(echo "$RELAYS" | jq '. | length')
relays=""
for (( i=0; i<$length; i++ )); do
  url=$(echo "$RELAYS" | jq -r ".[$i].url")
  user=$(echo "$RELAYS" | jq -r ".[$i].username // empty")
  pass=$(echo "$RELAYS" | jq -r ".[$i].password // empty")
  
  if [ -n "$user" ] && [ -n "$pass" ]; then
    relays+="[PASSWD]\nurl=$url\nusername=$user\npassword=$pass\n\n"
  else
    relays+="[NO_PASSWD]\nurl=$url\n\n"
  fi
  relays+="\n"
done
echo -e "$relays" > relays.txt
logGreen "relays.txt:"
cat relays.txt

echo ""
echo ""
logGreen "Starting Eaglercraft relay..."
echo ""

#start relay
./run.sh $AUTO_RESTART $DEBUG_MODE


