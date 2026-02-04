ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-debian:trixie-2025.12.2
FROM ${BUILD_FROM}
ARG BUILD_ARCH=amd64

# renovate: datasource=custom.vscode-cli depName=vscode-cli
ARG VSCODE_CLI_VERSION=1.109.0

WORKDIR /
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY rootfs .

# Uses /bin for compatibility purposes
# hadolint ignore=DL4005
RUN if [ ! -f /bin/sh ] && [ -f /usr/bin/sh ]; then ln -s /usr/bin/sh /bin/sh; fi && \
    if [ ! -f /bin/bash ] && [ -f /usr/bin/bash ]; then ln -s /usr/bin/bash /bin/bash; fi

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    curl=8.14.1-2+deb13u2 \
    tar=1.35+dfsg-3.1 \
    git=1:2.47.3-0+deb13u1 \
    openssh-client=1:10.0p1-7 && \
    [ "$BUILD_ARCH" = "aarch64" ] && ARCH="arm64" || ARCH="x64" && \
    curl -Lk https://update.code.visualstudio.com/${VSCODE_CLI_VERSION}/cli-linux-${ARCH}/stable -o vscode_cli.tar.gz && \
    tar -xf vscode_cli.tar.gz -C /bin && \
    apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*

# renovate: datasource=github-tags depName=docker/cli extractVersion=^v(?<version>.*)$
ENV DOCKER_VERSION=29.2.1
RUN curl -fsSL https://download.docker.com/linux/static/stable/x86_64/docker-$DOCKER_VERSION.tgz | tar zxvf - --strip 1 -C /usr/bin docker/docker

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

# Set environment variables for VS Code CLI
ENV VSCODE_CLI_USE_FILE_KEYCHAIN=true
ENV VSCODE_CLI_DATA_DIR=/config/.vscode
ENV VSCODE_AGENT_FOLDER=/config/.vscode-server


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
