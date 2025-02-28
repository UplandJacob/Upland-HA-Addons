#!/usr/bin/with-contenv bashio

logGreen() {
  echo -e "\033[32m$1\033[0m"
}

echo ""
echo "Eaglercraft 1.5.2 LAN World Relay"
echo "Relay version: 1.4"
echo "From https://git.eaglercraft.rip/eaglercraft/eaglercraft-1.8/src/branch/main/sp-relay/SharedWorldRelay"
echo ""

auto_restart="$1"
debug_mode="$2"

logGreen "autoRestart: $auto_restart"
logGreen "debugMode: $debug_mode"
echo ""
echo ""

start() {
  if [ "$debug_mode" = true ]; then
    java -jar EaglerSPRelay.jar --debug
  else
    java -jar EaglerSPRelay.jar
  fi
}

if [ "$auto_restart" = true ]; then
  echo "Auto restart enabled"
  while true
    do
      start
      logGreen "restarting..."
    sleep 5
  done
else
  echo "Auto restart disabled"
  start
fi

echo "stopping..."
echo ""
echo ""