#!/usr/bin/with-contenv bashio
bashio::log.info "Checking for .runner..."
if [ ! -f /config/.runner ]; then
    bashio::log.info "Registering..."
    if [ $GITEA_RUNNER_REGISTRATION_TOKEN = '' ]; then
        bashio::log.fatal "GITEA_RUNNER_REGISTRATION_TOKEN is not set."
        exit 1
    fi
    if [ $GITEA_INSTANCE_URL = '' ]; then
        bashio::log.fatal "GITEA_INSTANCE_URL is not set."
        exit 1
    fi
    if [ $GITEA_RUNNER_NAME = '' ]; then
        bashio::log.fatal "GITEA_RUNNER_NAME is not set."
        exit 1
    fi
    extra_args=""
    if [[ ! -z ${GITEA_RUNNER_LABELS+x} ]]; then
        extra_args="--labels $GITEA_RUNNER_LABELS"
    else
        bashio::log.warning "GITEA_RUNNER_LABELS is not set."
    fi
    /usr/local/bin/act_runner --config /config/config.yaml register --instance $GITEA_INSTANCE_URL --token $GITEA_RUNNER_REGISTRATION_TOKEN --name $GITEA_RUNNER_NAME $extra_args
fi