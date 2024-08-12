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

docker run -d \
    --sysctl net.ipv4.ping_group_range="0 2147483647" \
    --env TWINGATE_NETWORK="${NETWORK}" \
    --env TWINGATE_ACCESS_TOKEN="${ACCESS_TOKEN}" \
    --env TWINGATE_REFRESH_TOKEN="${REFRESH_TOKEN}" \
    --env TWINGATE_LABEL_HOSTNAME="`hostname`" \
    --env TWINGATE_LABEL_DEPLOYED_BY="docker" \
    --name "twingate-connector" \
    --restart=unless-stopped \
    --pull=always \
    twingate/connector:1

#helm upgrade --install twingate-connector twingate/connector -n default \
#  --set connector.network="${NETWORK}" \
#  --set connector.accessToken="${ACCESS_TOKEN}" \
#  --set connector.refreshToken="${REFRESH_TOKEN}"


#curl "https://binaries.twingate.com/connector/setup.sh" | sudo \
#sudo /twingate-install.sh -f \
#  TWINGATE_ACCESS_TOKEN="${ACCESS_TOKEN}" \
#  TWINGATE_REFRESH_TOKEN="${REFRESH_TOKEN}" \
#  TWINGATE_LOG_ANALYTICS="v2" \
#  TWINGATE_NETWORK="${NETWORK}" \
#  TWINGATE_LABEL_DEPLOYED_BY="linux" bash


echo ""
echo ""

#sudo twingate-connector

