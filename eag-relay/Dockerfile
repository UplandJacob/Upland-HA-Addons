ARG BUILD_FROM
FROM ${BUILD_FROM}

COPY start.sh /
COPY relays.txt /

# Uses /bin for compatibility purposes
# hadolint ignore=DL4005
RUN if [ ! -f /bin/sh ] && [ -f /usr/bin/sh ]; then ln -s /usr/bin/sh /bin/sh; fi && \
    if [ ! -f /bin/bash ] && [ -f /usr/bin/bash ]; then ln -s /usr/bin/bash /bin/bash; fi


RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    yq sudo curl default-jre unzip coturn

RUN curl --no-progress-meter \
    -H "Accept-Encoding: identity" \
    -H "Accept-Language: en" -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4.212 Safari/537.36" \
    -o /relay.zip \
    "https://git.eaglercraft.rip/eaglercraft/eaglercraft-1.8/raw/branch/main/sources/resources/relay_download.zip"

RUN unzip -n relay.zip
RUN sudo chmod 777 run.sh
RUN sudo chmod 777 start.sh

# entrypoint
CMD [ "/start.sh" ]




#ARG BUILD_ARCH
#ARG BUILD_DATE
#ARG BUILD_DESCRIPTION
#ARG BUILD_NAME
#ARG BUILD_REF
ARG REPO_URL
ARG VERSION
ARG PLATFORM
LABEL \
#    io.hass.name="${BUILD_NAME}" \
#    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${PLATFORM}" \
    io.hass.type="addon" \
    io.hass.version=${VERSION} \
    maintainer="UplandJacob (${REPO_URL})" \
#    org.opencontainers.image.title="${BUILD_NAME}" \
#    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="Home Assistant Add-ons" \
    org.opencontainers.image.authors="UplandJacob (https://github.com/uplandjacob)" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="${REPO_URL}" \
    org.opencontainers.image.source="${REPO_URL}" \
    org.opencontainers.image.documentation="${REPO_URL}/blob/main/README.md" \
#    org.opencontainers.image.created=${BUILD_DATE} \
#    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${VERSION}

