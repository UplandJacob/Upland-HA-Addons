ARG BUILD_FROM
FROM ${BUILD_FROM}

ARG VELOCITY_VERS="3.4.0-SNAPSHOT"
ARG VELOCITY_BUILD="452"
ARG VIAVERSION_VERS="5.1.1"
ARG VIAREWIND_VERS="4.0.3"
ARG VIABACKWARDS_VERS="5.1.1"

COPY default_config default_config

COPY run.sh run.sh
COPY kickstart.sh kickstart.sh
RUN chmod +x run.sh
RUN chmod +x kickstart.sh
#COPY velocity.toml velocity.toml
RUN find . -maxdepth 1 -type f -exec chmod 777 {} \;

# Uses /bin for compatibility purposes
# hadolint ignore=DL4005
RUN if [ ! -f /bin/sh ] && [ -f /usr/bin/sh ]; then ln -s /usr/bin/sh /bin/sh; fi && \
    if [ ! -f /bin/bash ] && [ -f /usr/bin/bash ]; then ln -s /usr/bin/bash /bin/bash; fi

# RUN apt-get update && \
#     apt-get install --no-install-recommends -y \

#Velocity
RUN curl --no-progress-meter \
    -H "Accept-Encoding: identity" \
    -H "Accept-Language: en" -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4.212 Safari/537.36" \
    -o /velocity.jar \
    "https://api.papermc.io/v2/projects/velocity/versions/$VELOCITY_VERS/builds/$VELOCITY_BUILD/downloads/velocity-$VELOCITY_VERS-$VELOCITY_BUILD.jar"

### PLUGINS
RUN mkdir -p plugins

# for Eaglercraft
RUN cd plugins && curl --no-progress-meter \
    -H "Accept-Encoding: identity" \
    -H "Accept-Language: en" -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4.212 Safari/537.36" \
    -o EaglerXVelocity-Latest.jar \
    "https://git.eaglercraft.rip/eaglercraft/eaglercraft-1.8/raw/branch/main/gateway/EaglercraftXVelocity/EaglerXVelocity-Latest.jar"

# for old clients including Eaglercraft
RUN cd plugins && curl --no-progress-meter \
    -H "Accept-Encoding: identity" \
    -H "Accept-Language: en" -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4.212 Safari/537.36" \
    -o ViaVersion.jar \
    "https://hangarcdn.papermc.io/plugins/ViaVersion/ViaVersion/versions/$VIAVERSION_VERS/PAPER/ViaVersion-$VIAVERSION_VERS.jar"

RUN cd plugins && curl --no-progress-meter \
    -H "Accept-Encoding: identity" \
    -H "Accept-Language: en" -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4.212 Safari/537.36" \
    -o ViaRewind.jar \
    "https://hangarcdn.papermc.io/plugins/ViaVersion/ViaRewind/versions/$VIAREWIND_VERS/PAPER/ViaRewind-$VIAREWIND_VERS.jar"

RUN cd plugins && curl --no-progress-meter \
    -H "Accept-Encoding: identity" \
    -H "Accept-Language: en" -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4.212 Safari/537.36" \
    -o ViaBackwards.jar \
    "https://hangarcdn.papermc.io/plugins/ViaVersion/ViaBackwards/versions/$VIABACKWARDS_VERS/PAPER/ViaBackwards-$VIABACKWARDS_VERS.jar"

# for Bedrock
RUN cd plugins && curl --no-progress-meter \
    -H "Accept-Encoding: identity" \
    -H "Accept-Language: en" -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4.212 Safari/537.36" \
    -o Geyser.jar \
    "https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/velocity"

RUN cd plugins && curl --no-progress-meter \
    -H "Accept-Encoding: identity" \
    -H "Accept-Language: en" -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4.212 Safari/537.36" \
    -o Floodgate.jar \
    "https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/velocity"


RUN find . -maxdepth 1 -type f -exec chmod 777 {} \;

RUN ./kickstart.sh
# entrypoint
CMD [ "/run.sh" ]

ARG BUILD_ARCH
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
