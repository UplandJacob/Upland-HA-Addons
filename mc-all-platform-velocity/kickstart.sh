#!/bin/bash

java -Xms1G -Xmx1G -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:MaxInlineLevel=15 -Deaglerxvelocity.stfu=true -jar velocity.jar > log.txt 2>&1 &
# Get process ID of last background cmd
pid=$!

# Function to stop the process when the specific string is found in the log
stop_when_string_logged() {
  while IFS= read -r line; do
    echo "RUNNING: $line"
    if [[ "$line" == *"downloaded and loaded!"* ]]; then
      sleep 2
      kill $pid
      echo "Process stopped."
      break
    fi
  done
}

stop_when_string_logged < <(tail -f log.txt)

wait $pid

rm /plugins/floodgate/key.pem