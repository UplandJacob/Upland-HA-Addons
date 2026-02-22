ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-debian:trixie-2026.02.0
FROM ${BUILD_FROM}
ARG BUILD_ARCH=amd64

WORKDIR /
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY rootfs .

# Uses /bin for compatibility purposes
# hadolint ignore=DL4005
RUN if [ ! -f /bin/sh ] && [ -f /usr/bin/sh ]; then ln -s /usr/bin/sh /bin/sh; fi && \
    if [ ! -f /bin/bash ] && [ -f /usr/bin/bash ]; then ln -s /usr/bin/bash /bin/bash; fi

# Install packages
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    lsb-release=12.1-1 \
    gpg=2.4.7-21+deb13u1+b1 \
    curl=8.14.1-2+deb13u2 \
    tar=1.35+dfsg-3.1 && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://packages.redis.io/gpg | gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg && \
    chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list && \
    apt-get update && apt-get install --no-install-recommends -y \
    redis=6:8.6.0-1rl1~trixie1 && \
    apt-get remove -y lsb-release gpg && rm -rf /var/lib/apt/lists/*

ENV REDIS_EXPORTER_VERSION=v1.81.0
RUN [ "$BUILD_ARCH" = "aarch64" ] && ARCH="arm64" || ARCH="$BUILD_ARCH" && \
    curl -fsSL "https://github.com/oliver006/redis_exporter/releases/download/${REDIS_EXPORTER_VERSION}/redis_exporter-${REDIS_EXPORTER_VERSION}.linux-${ARCH}.tar.gz" \
        | tar zxvf - -C /usr/bin --strip-components=1 "redis_exporter-${REDIS_EXPORTER_VERSION}.linux-${ARCH}/redis_exporter" && \
    redis_exporter --version

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


#ARG BUILD_DATE
#ARG BUILD_REF
ARG BUILD_NAME
ARG BUILD_DESCRIPTION
ARG BUILD_REPO_NAME
ARG BUILD_SLUG
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
