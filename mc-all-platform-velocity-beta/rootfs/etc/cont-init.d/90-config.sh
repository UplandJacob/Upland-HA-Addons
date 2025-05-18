#!/usr/bin/with-contenv bashio

bashio::log.info "Updating config and jars..."

python3 /etc/helpers/config.py
