#!/usr/bin/with-contenv bashio
bashio::log.info "Checking for config.yaml..."
if [ ! -f /config/config.yaml ]; then
    bashio::log.info "Generating config.yaml..."
    /usr/local/bin/act_runner generate-config > /config/config.yaml
    yq -i -y '.runner.file = "/config/.runner"' /config/config.yaml
fi
