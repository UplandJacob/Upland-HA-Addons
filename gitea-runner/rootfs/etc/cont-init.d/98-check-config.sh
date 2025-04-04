#!/usr/bin/with-contenv bashio
bashio::log.info "checking for config.yaml..."
if [ ! -f /config/config.yaml ]; then
    bashio::log.info "generating config.yaml..."
    /usr/local/bin/act_runner generate-config > /config.yaml
fi