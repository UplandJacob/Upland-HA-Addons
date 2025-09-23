#!/usr/bin/with-contenv bashio
bashio::log.info "Checking for .runner..."
if [ ! -f /config/.runner ]; then
    bashio::log.info "Registering..."
    if [ $GITEA_RUNNER_REGISTRATION_TOKEN = '' ]; then
        bashio::log.fatal "GITEA_RUNNER_REGISTRATION_TOKEN is not set!"
        exit 1
    fi
    /usr/local/bin/act_runner register --instance $GITEA_INSTANCE_URL --token $GITEA_RUNNER_REGISTRATION_TOKEN --name $GITEA_RUNNER_NAME --labels $GITEA_RUNNER_LABELS
fi