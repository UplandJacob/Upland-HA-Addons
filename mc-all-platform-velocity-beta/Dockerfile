ARG BUILD_FROM=ghcr.io/uplandjacob/ha-base-debian-java-amd64:0.2.3
FROM ${BUILD_FROM}

WORKDIR /

COPY rootfs .
COPY default_config default_config
COPY requirements.txt requirements.txt
COPY config.yaml /default_config


# Uses /bin for compatibility purposes
# hadolint ignore=DL4005
RUN if [ ! -f /bin/sh ] && [ -f /usr/bin/sh ]; then ln -s /usr/bin/sh /bin/sh; fi && \
    if [ ! -f /bin/bash ] && [ -f /usr/bin/bash ]; then ln -s /usr/bin/bash /bin/bash; fi

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    tmux python3-full python3-pip && \
    apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --break-system-packages -r requirements.txt && \
    python3 -m pip install --no-cache-dir --break-system-packages --no-deps ruamel.yaml==0.19.0

# Modules
ARG MODULES="00-banner.sh"

# Automatic modules download
ADD "https://raw.githubusercontent.com/alexbelgium/hassio-addons/master/.templates/ha_automodules.sh" "/ha_automodules.sh"
RUN chmod 744 /ha_automodules.sh && /ha_automodules.sh "$MODULES" && rm /ha_automodules.sh

# Manual apps (NONE)
ENV PACKAGES=""
# Automatic apps & bashio
ADD "https://raw.githubusercontent.com/alexbelgium/hassio-addons/master/.templates/ha_autoapps.sh" "/ha_autoapps.sh"
RUN chmod 744 /ha_autoapps.sh && /ha_autoapps.sh "$PACKAGES" && rm /ha_autoapps.sh

# Add entrypoint
ENV S6_STAGE2_HOOK=/ha_entrypoint.sh
ADD "https://raw.githubusercontent.com/alexbelgium/hassio-addons/master/.templates/ha_entrypoint.sh" "/ha_entrypoint.sh"

# Entrypoint modifications
ADD "https://raw.githubusercontent.com/alexbelgium/hassio-addons/master/.templates/ha_entrypoint_modif.sh" "/ha_entrypoint_modif.sh"
RUN chmod 777 /ha_entrypoint.sh /ha_entrypoint_modif.sh && /ha_entrypoint_modif.sh && rm /ha_entrypoint_modif.sh

RUN rm /etc/cont-init.d/00-global_var.sh


ARG BUILD_ARCH
#ARG BUILD_DATE
#ARG BUILD_REF
ARG BUILD_NAME
ARG BUILD_SLUG
ARG BUILD_DESCRIPTION
ARG BUILD_REPO_NAME
ARG BUILD_AUTHOR
ARG BUILD_LICENSE
ARG BUILD_VERSION
LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="${BUILD_AUTHOR} (https://github.com/${BUILD_AUTHOR})" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="Home Assistant Add-ons" \
    org.opencontainers.image.authors="${BUILD_AUTHOR} (https://github.com/${BUILD_AUTHOR})" \
    org.opencontainers.image.licenses="${BUILD_LICENSE}" \
    org.opencontainers.image.url="https://github.com/${BUILD_AUTHOR}/${BUILD_REPO_NAME}" \
    org.opencontainers.image.source="https://github.com/${BUILD_AUTHOR}/${BUILD_REPO_NAME}/tree/main/${BUILD_SLUG}" \
    org.opencontainers.image.documentation="https://github.com/${BUILD_AUTHOR}/${BUILD_REPO_NAME}/blob/main/${BUILD_SLUG}/README.md" \
#    org.opencontainers.image.created=${BUILD_DATE} \
#    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}
