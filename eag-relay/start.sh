#!/usr/bin/with-contenv bashio

echo ""
echo ""

#get config
RELAY_CONFIG=$(bashio::config 'relayConfig')
RELAYS=$(bashio::config 'relays')

#set config file
config=$(echo "$RELAY_CONFIG" | jq -r 'to_entries | .[] | "\(.key): \(.value)"')
echo -e "[EaglerSPRelay]\nport: 6699\naddress: 0.0.0.0\n$config" > relayConfig.ini

echo "relayConfig.ini:"
cat relayConfig.ini
echo ""

#relays=$(echo "$RELAYS" | jq -r 'to_entries | .[] | "\(.key): \(.value)"')
echo -e "$RELAYS" > relays.txt

echo "relays.txt:"
cat relays.txt

echo ""
echo ""

#start turn/stun server
#turnserver --daemon --no-auth -n -V --syslog &

echo ""
echo ""

#start relay
./run.sh &

echo ""
echo ""
echo ""
echo ""

