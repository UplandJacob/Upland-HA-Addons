#!/usr/bin/with-contenv bashio

logGreen() {
  echo -e "\033[32m$1\033[0m"
}

echo ""
echo "Eaglercraft 1.5.2 LAN World Relay"
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
