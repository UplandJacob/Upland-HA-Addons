#!/bin/bash
java -jar velocity.jar &
# Get the process ID (PID) of the last background command
pid=$!


duration=60

sleep $duration
kill $pid
