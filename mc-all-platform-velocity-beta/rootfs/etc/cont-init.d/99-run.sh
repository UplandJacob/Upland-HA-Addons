#!/usr/bin/with-contenv bashio

getConfig() {
  jq --raw-output "$1" /data/options.json
}

bashio::log.green "Starting app..."

cd /config/server
tmpfile=$(mktemp)

RAM_ALLOCATE=$(getConfig '.allocatedRAM')
RAM_MAX=$(getConfig '.maxRAM')
bashio::log.green "Allocated RAM: $RAM_ALLOCATE MB"
bashio::log.green "Max RAM: $RAM_MAX MB"

# Create a screen session named "velocity" and start the command
screen -dmS velocity bash -c "java -Xms${RAM_ALLOCATE}M -Xmx${RAM_MAX}M -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:MaxInlineLevel=15 -jar velocity.jar > $tmpfile 2>&1"

running=true


tail -f $tmpfile | while IFS= read -r line; do
  if [[ "$line" != *"ERROR]: SLF4J:"* ]]; then
    echo "$line"
  fi
  if [[ "$running" == "false" ]]; then
    bashio::log.green "Stopping log tail..."
    break
  fi
done &


# Wait for the process to finish
screen -S velocity -X quit
running=false
bashio::log.green "End detected"
