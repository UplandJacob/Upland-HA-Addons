# Twingate

## About
Deploy a twingate connector from Home Assistant.

## Install
1. Go to (twingate.com) and create an account and network.
2. Create a remote network and resource.
3. Create a connector, choose docker, generate tokens and input extra options. You will end up with something like this:

```
docker run -d 
  --env TWINGATE_NETWORK="somenetwork" 
  --env TWINGATE_ACCESS_TOKEN="someverylongtoken" 
  --env TWINGATE_REFRESH_TOKEN="somelesslongtoken"  
  --env TWINGATE_DNS="dnshostname"  
  --env TWINGATE_LABEL_HOSTNAME="`hostname`" 
  --env TWINGATE_LABEL_DEPLOYED_BY="docker" 
  --name "twingate-connector" 
  --network=host 
  --restart=unless-stopped 
  --pull=always 
  twingate/connector:1
```
