# Twingate



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