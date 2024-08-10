#!/usr/bin/with-contenv bashio

NETWORK=$(bashio::config 'network')
ACCESS_TOKEN=$(bashio::config 'access_token')
REFRESH_TOKEN=$(bashio::config 'refresh_token')
LOCAL_CONNECTION=$(bashio::config 'allow_local_connection')
LOGS=$(bashio::config 'local_connection_logs')

GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}info entered:"
echo "network: ${NETWORK}"
echo "access_token: ${ACCESS_TOKEN}"
echo "refresh_token: ${REFRESH_TOKEN}"
echo "allow_local_connection: ${LOCAL_CONNECTION}"
echo -e "local_connection_logs: ${LOGS}${NC}"


#curl "https://binaries.twingate.com/connector/setup.sh" | sudo \
sudo service \
  TWINGATE_ACCESS_TOKEN="${ACCESS_TOKEN}" \
  TWINGATE_REFRESH_TOKEN="${REFRESH_TOKEN}" \
  TWINGATE_LOG_ANALYTICS="v2" \
  TWINGATE_NETWORK="${NETWORK}" \
  TWINGATE_LABEL_DEPLOYED_BY="linux" bash

