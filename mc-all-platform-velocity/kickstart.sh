#!/bin/bash
tmpfile=$(mktemp)

# Create a screen session named "minecraft" and start the command
screen -dmS velocity bash -c 'java -Xms1G -Xmx1G -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:MaxInlineLevel=15 -Deaglerxvelocity.stfu=true -jar velocity.jar > '$tmpfile' 2>&1'

# Function to stop the process when the specific string is found in the log
stop_when_string_logged() {
  while IFS= read -r line; do
    echo "- $line"
    if [[ "$line" == *"downloaded and loaded!"* ]]; then
      sleep 1
      # Send the "stop" command to the "minecraft" screen session
      screen -S velocity -X stuff "`echo -ne \"stop\r\"`"
      echo "Process stopped."
      break
    fi
  done
}
stop_when_string_logged < <(tail -f $tmpfile)

# Wait for the process to finish
screen -S velocity -X quit
# cleanup tmpfile
rm -f $tmpfile
