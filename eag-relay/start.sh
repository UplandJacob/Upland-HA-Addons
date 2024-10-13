#!/usr/bin/with-contenv bashio

echo ""
echo ""

#get config
RELAY_CONFIG=$(bashio::config 'relayConfig')
#set config file

config=$(echo "$RELAY_CONFIG" | jq -r 'to_entries | .[] | "\(.key): \(.value)"')
echo -e "[EaglerSPRelay]\nport: 6969\naddress: 0.0.0.0\n$config" > relayConfig.ini

echo "relayConfig.ini:"
cat relayConfig.ini

echo ""
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
#echo "attaching to syslog..."
echo ""

turnserver --no-auth -n -V --syslog &

#sudo tail -f /var/log/syslog

