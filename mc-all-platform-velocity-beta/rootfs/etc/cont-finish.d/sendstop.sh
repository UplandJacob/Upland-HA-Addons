#!/usr/bin/with-contenv bashio

bashio::log.green "Sending stop command to Velocity..."
screen -S velocity -X stuff "`echo -ne \"stop\r\"`"
bashio::log.info "Sent"

# Wait for the process to finish
screen -S velocity -X quit
bashio::log.green "Stopped"
