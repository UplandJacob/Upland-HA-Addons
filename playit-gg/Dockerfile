ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-debian:trixie-2025.12.0
FROM ${BUILD_FROM}
ARG BUILD_ARCH

WORKDIR /

COPY rootfs .

# Uses /bin for compatibility purposes
# hadolint ignore=DL4005
RUN if [ ! -f /bin/sh ] && [ -f /usr/bin/sh ]; then ln -s /usr/bin/sh /bin/sh; fi && \
    if [ ! -f /bin/bash ] && [ -f /usr/bin/bash ]; then ln -s /usr/bin/bash /bin/bash; fi

# renovate: datasource=github-tags depName=playit-cloud/playit-agent versioning=loose
ENV PLAYIT_AGENT_VERSION=v0.17.1

# hadolint ignore=DL3008
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update \
    && apt-get --no-install-recommends install -y curl \
    && [ "$BUILD_ARCH" = "aarch64" ] && ARCH="arm64" || ARCH="amd64" \
    && curl -SsL https://github.com/playit-cloud/playit-agent/releases/download/${PLAYIT_AGENT_VERSION}/playit_${ARCH}.deb -o ./playit_amd64.deb \
    && apt-get --no-install-recommends install -y ./playit_amd64.deb \
    && apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*

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
