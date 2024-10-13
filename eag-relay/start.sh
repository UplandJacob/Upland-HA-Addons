#!/usr/bin/with-contenv bashio

echo:
echo:

#get config
RELAY_CONFIG=$(bashio::config 'relayConfig')
#set config file
echo -e "[EaglerSPRelay]\n$RELAY_CONFIG" > relayConfig.ini

echo "relayConfig.ini:"
cat relayConfig.ini

echo:
echo "relays.txt:"
cat relays.txt

echo:
echo:

#start turn/stun server
turnserver --daemon --no-auth -n
#start relay
./run.sh
