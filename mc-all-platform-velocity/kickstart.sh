#!/bin/bash

java -Xms1G -Xmx1G -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:MaxInlineLevel=15 -jar velocity.jar &
# Get the process ID (PID) of the last background command
pid=$!


duration=15

sleep $duration
kill $pid
