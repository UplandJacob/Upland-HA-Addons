#!/usr/bin/with-contenv bashio


echo ""
echo "Eaglercraft 1.5.2 LAN World Relay"
echo ""

local auto_restart="$1"
local debug_mode="$2"

bashio::log.green "autoRestart: $auto_restart"
bashio::log.green "debugMode: $debug_mode"
echo ""
exho ""

start() {
  if [ "$debug_mode" = true ]; then
    java -jar EaglerSPRelay.jar --debug
  else
    java -jar EaglerSPRelay.jar
  fi
}

if [ "$auto_restart" = true ]; then
  while true
    do
      start
      echo "restarting..."
    sleep 5
  done
else
  start
fi

echo "stopping..."
echo ""
echo ""
