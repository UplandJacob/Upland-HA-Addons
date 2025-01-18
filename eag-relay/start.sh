#!/usr/bin/with-contenv bashio

echo ""
echo ""

logGreen() {
  echo -e "\033[32m$1\033[0m"
}

#get config
RELAY_CONFIG=$(bashio::config 'relayConfig')
RELAYS=$(bashio::config 'relays')

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
logGreen "relays JSON unformatted:"
echo $RELAYS
echo ""

relayJSON=$(echo $RELAYS | sed 's/}/},/g' | sed '$ s/,$//' | awk '{print "[" $0 "]"}')

logGreen "relays JSON formatted:"
echo $relayJSON
echo ""
length=$(echo "$relayJSON" | jq '. | length')
relays=""
for (( i=0; i<$length; i++ )); do
  url=$(echo "$relayJSON" | jq -r ".[$i].url")
  user=$(echo "$relayJSON" | jq -r ".[$i].username // empty")
  cred=$(echo "$relayJSON" | jq -r ".[$i].credential // empty")
  
  if [ -n "$user" ] && [ -n "$cred" ]; then
    relays+="[PASSWD]\nurl=$url\nusername=$user\ncredential=$cred\n\n"
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


