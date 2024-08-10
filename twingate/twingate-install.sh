#!/bin/bash

set -e

CONFIG="/etc/twingate/connector.conf"
CONFIG_DIR=$(dirname "$CONFIG")

exit_no_changes () {
    echo "Canceling setup and exiting. No changes have been made."
    exit 1
}

usage () {
    echo "Usage: $0 [ -f ]"
    echo "            -f   (optional) force updating an existing configuration file"
    echo "                 A copy of the existing configuration file will be made"
    echo
    exit 1
}

while getopts "f" options; do
    case "$options" in
        f)
            FORCE=true
            ;;
        *)
            usage
            ;;
    esac
done

if [ -f "$CONFIG" ] && [ "$FORCE" != true ]; then
    echo "Config file \"${CONFIG}\" already exists"
    exit_no_changes
else
    install -d -m 0700 "$CONFIG_DIR"
    [ -f "$CONFIG" ] && mv "$CONFIG" "$CONFIG.$(date +%s)"
fi


echo "deb [trusted=true] https://packages.twingate.com/apt/ /" | tee /etc/apt/sources.list.d/twingate.list
apt-get update -yq
apt-get install -yq twingate-connector


if [ -n "${TWINGATE_NETWORK}" ]; then
  echo "TWINGATE_NETWORK=${TWINGATE_NETWORK}" >> "${CONFIG}"
elif [ -n "${TWINGATE_URL}" ]; then
  echo "TWINGATE_URL=${TWINGATE_URL}" >> "${CONFIG}"
fi

if [ -n "${TWINGATE_ACCESS_TOKEN}" ] && [ -n "${TWINGATE_REFRESH_TOKEN}" ]; then
    { \
        echo "TWINGATE_ACCESS_TOKEN=${TWINGATE_ACCESS_TOKEN}"; \
        echo "TWINGATE_REFRESH_TOKEN=${TWINGATE_REFRESH_TOKEN}"; \
    } >> "${CONFIG}"
    if [ -n "${TWINGATE_LOG_ANALYTICS}" ]; then
        echo "TWINGATE_LOG_ANALYTICS=${TWINGATE_LOG_ANALYTICS}" >> "${CONFIG}"
    fi
    chmod 0600 "$CONFIG"
    #systemctl enable --now twingate-connector
    #twingate-connector
fi
