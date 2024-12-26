#!/usr/bin/with-contenv bashio

NETWORK=$(bashio::config 'network')
ACCESS_TOKEN=$(bashio::config 'access_token')
REFRESH_TOKEN=$(bashio::config 'refresh_token')
LOCAL_CONNECTION=$(bashio::config 'allow_local_connection')
LOGS=$(bashio::config 'local_connection_logs')

GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}"

echo "info entered:"
echo "network: ${NETWORK}"
echo "access_token: ${ACCESS_TOKEN}"
echo "refresh_token: ${REFRESH_TOKEN}"
echo "allow_local_connection: ${LOCAL_CONNECTION}"
echo "local_connection_logs: ${LOGS}"

echo -e "${NC}"

#ps -p 1 -o comm=

echo ""


CONFIG="/etc/twingate/connector.conf"

if [ -n "${NETWORK}" ]; then
  echo "TWINGATE_NETWORK=${NETWORK}" >> "${CONFIG}"
fi

if [ -n "${ACCESS_TOKEN}" ] && [ -n "${REFRESH_TOKEN}" ]; then
    { \
        echo "TWINGATE_ACCESS_TOKEN=${ACCESS_TOKEN}"; \
        echo "TWINGATE_REFRESH_TOKEN=${REFRESH_TOKEN}"; \
    } >> "${CONFIG}"
    if [ "${LOGS}" = true ]; then
        echo "TWINGATE_LOG_ANALYTICS=v2" >> "${CONFIG}"
    fi
    chmod 0600 "$CONFIG"
    systemctl enable --now twingate-connector
fi


echo ""
echo ""

