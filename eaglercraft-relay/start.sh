#!/usr/bin/with-contenv bashio

RELAY_CONFIG=$(bashio::config 'relayConfig')

echo -e "[EaglerSPRelay]\n$RELAY_CONFIG" > relayConfig.ini

turnserver --daemon --no-auth -n

./run.sh