#!/bin/bash
tmpfile=$(mktemp)

java -Xms1G -Xmx1G -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:MaxInlineLevel=15 -Deaglerxvelocity.stfu=true -jar velocity.jar > $tmpfile 2>&1 &
# Get process ID of last background cmd
pid=$!

# Function to stop the process when the specific string is found in the log
stop_when_string_logged() {
  while IFS= read -r line; do
    echo "- $line"
    if [[ "$line" == *"downloaded and loaded!"* ]]; then
      sleep 1
      #kill $pid
      echo -ne "stop\r" > /proc/$pid/fd/0
      echo "Process stopped."
      break
    fi
  done
}

stop_when_string_logged < <(tail -f $tmpfile)

wait $pid

rm /plugins/floodgate/key.pem