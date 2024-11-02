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

echo $RELAYS
relayJSON=$(echo $RELAYS | sed 's/}/},/g' | sed '$ s/,$//' | awk '{print "[" $0 "]"}')
echo $relayJSON

length=$(echo "$relayJSON" | jq '. | length')
echo "length: $length\n"
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

echo "relays.txt:"
cat relays.txt

echo ""
echo ""

echo ""
echo ""

#start relay (run.sh file is downloaded with relay)
./run.sh 

echo ""
echo ""

