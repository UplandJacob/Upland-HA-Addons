#!/bin/bash

CONFIG_PATH=/config.yaml

NETWORK=$(yq '.options.network' $CONFIG_PATH)
ACCESS_TOKEN=$(yq '.options.access_token' $CONFIG_PATH)
REFRESH_TOKEN=$(yq '.options.refresh_token' $CONFIG_PATH)
LOGS=$(yq '.options.local_connection_logs' $CONFIG_PATH)


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

