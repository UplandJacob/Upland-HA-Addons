#!/usr/bin/with-contenv bashio

bashio::log.green "Starting app..."

#!/bin/bash
tmpfile=$(mktemp)

# Create a screen session named "velocity" and start the command
screen -dmS velocity bash -c 'java -Xms1G -Xmx1G -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:MaxInlineLevel=15 -jar /config/velocity.jar > '$tmpfile' 2>&1'

running=true

# Function to stop the process when the specific string is found in the log
filter() {
  while IFS= read -r line; do
    echo "$line"
    #if [[ "$line" == *"something to filter"* ]]; then
      # TODO - LOG FILTER
      # This is a long-term goal. I just want to have this here ready.
    #fi
    if  [[ "$running" == "false" ]]; then
      bashio::log.green "Stopping log tail..."
      break
    fi
  done
}
filter < <(tail -f $tmpfile)

# Wait for the process to finish
screen -S velocity -X quit
running=false
bashio::log.green "End detected"

