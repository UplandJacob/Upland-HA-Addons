#!/bin/bash

java -Xms1G -Xmx1G -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:MaxInlineLevel=15 -jar velocity.jar &
# Get the process ID (PID) of the last background command
pid=$!

# Function to stop the process when the specific string is found in the log
stop_when_string_logged() {
  while IFS= read -r line; do
    echo "$line"
    if [[ "$line" == *"Run /geyser help for help!"* ]]; then
      kill $pid
      echo "Process stopped."
      break
    fi
  done
}



#duration=7

#sleep $duration
#kill $pid


stop_when_string_logged < <(tail -f nohup.out)

wait $pid

rm /plugins/floodgate/key.pem