#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json

NETWORK=$(bashio::config 'network')
ACCESS_TOKEN=$(bashio::config 'access_token')
REFRESH_TOKEN=$(bashio::config 'refresh_token')
LOGS=$(bashio::config 'local_connection_logs')

echo "info entered:"
echo "network: ${NETWORK}"
echo "access_token: ${ACCESS_TOKEN}"
echo "refresh_token: ${REFRESH_TOKEN}"
echo "log: ${LOGS}"


curl "https://binaries.twingate.com/connector/setup.sh" | sudo \
  TWINGATE_ACCESS_TOKEN="${ACCESS_TOKEN}" \
  TWINGATE_REFRESH_TOKEN="${REFRESH_TOKEN}" \
  TWINGATE_LOG_ANALYTICS="v2" \
  TWINGATE_NETWORK="${NETWORK}" \
  TWINGATE_LABEL_DEPLOYED_BY="linux" bash

