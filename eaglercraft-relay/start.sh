#!/usr/bin/with-contenv bashio
#get config
RELAY_CONFIG=$(bashio::config 'relayConfig')
#set config file
echo -e "[EaglerSPRelay]\n$RELAY_CONFIG" > relayConfig.ini
#start turn/stun server
turnserver --daemon --no-auth -n
#start relay
./run.sh