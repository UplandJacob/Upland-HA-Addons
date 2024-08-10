#!/usr/bin/env bashio

NETWORK=$(bashio::config 'network')
ACCESS_TOKEN=$(bashio::config 'access_token')
REFRESH_TOKEN=$(bashio::config 'refresh_token')

echo "info entered:"
echo "network: $NETWORK"
echo "access_token: $ACCESS_TOKEN"
echo "refresh_token: $REFRESH_TOKEN"


curl "https://binaries.twingate.com/connector/setup.sh" | sudo \
  TWINGATE_ACCESS_TOKEN="" \ 
  TWINGATE_REFRESH_TOKEN="" \ 
  TWINGATE_LOG_ANALYTICS="v2" \
  TWINGATE_NETWORK="feilhouse" \
  TWINGATE_LABEL_DEPLOYED_BY="linux" bash

