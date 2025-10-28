#!/usr/bin/with-contenv bashio

bashio::log.info "Starting app..."

/usr/local/bin/act_runner --config /config/config.yaml daemon