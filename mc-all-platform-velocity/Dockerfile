ARG BUILD_FROM
FROM ${BUILD_FROM}

ENV VELOCITY_VERS="3.4.0-SNAPSHOT"
ENV VELOCITY_BUILD="487"
ENV EAGLER_COMMIT_ID="b0a2739fe126dd8440b380449af9a2117754e59c"
ENV VIAVERSION_VERS="5.3.2"
ENV VIABACKWARDS_VERS="5.3.2"
ENV VIAREWIND_VERS="4.0.7"
ENV GEYSER_VERS="2.7.0"
ENV GEYSER_BUILD="820"
ENV FLOOD_VERS="2.2.4"
ENV FLOOD_BUILD="116"

WORKDIR /

COPY default_config default_config

COPY run.sh run.sh
COPY kickstart.sh kickstart.sh
RUN chmod +x run.sh && chmod +x kickstart.sh && \
    find . -maxdepth 1 -type f -exec chmod 777 {} \;

# Uses /bin for compatibility purposes
# hadolint ignore=DL4005
RUN if [ ! -f /bin/sh ] && [ -f /usr/bin/sh ]; then ln -s /usr/bin/sh /bin/sh; fi && \
    if [ ! -f /bin/bash ] && [ -f /usr/bin/bash ]; then ln -s /usr/bin/bash /bin/bash; fi

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    rsync screen uuid-runtime && \
    apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*

#Velocity
RUN curl --no-progress-meter -H "Accept-Encoding: identity" -H "Accept-Language: en" -L \
    -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4.212 Safari/537.36" \
    -o /velocity.jar "https://api.papermc.io/v2/projects/velocity/versions/$VELOCITY_VERS/builds/$VELOCITY_BUILD/downloads/velocity-$VELOCITY_VERS-$VELOCITY_BUILD.jar"

### PLUGINS
WORKDIR /plugins

# for Eaglercraft
ADD "https://gitea.uplandustries.com/uplandustries/eaglercraft-1.8/raw/commit/$EAGLER_COMMIT_ID/gateway/EaglercraftXVelocity/EaglerXVelocity-Latest.jar" EaglerXVelocity.jar

# for older and newer clients (compared to backend servers) including Eaglercraft
ADD "https://hangarcdn.papermc.io/plugins/ViaVersion/ViaVersion/versions/$VIAVERSION_VERS/PAPER/ViaVersion-$VIAVERSION_VERS.jar" ViaVersion.jar
ADD "https://hangarcdn.papermc.io/plugins/ViaVersion/ViaRewind/versions/$VIAREWIND_VERS/PAPER/ViaRewind-$VIAREWIND_VERS.jar" ViaRewind.jar
ADD "https://hangarcdn.papermc.io/plugins/ViaVersion/ViaBackwards/versions/$VIABACKWARDS_VERS/PAPER/ViaBackwards-$VIABACKWARDS_VERS.jar" ViaBackwards.jar

# for Bedrock
ADD "https://download.geysermc.org/v2/projects/geyser/versions/$GEYSER_VERS/builds/$GEYSER_BUILD/downloads/velocity" Geyser.jar
ADD "https://download.geysermc.org/v2/projects/floodgate/versions/$FLOOD_VERS/builds/$FLOOD_BUILD/downloads/velocity" Floodgate.jar

WORKDIR /

RUN find . -maxdepth 1 -type f -exec chmod 777 {} \;

# kickstart and make sure there are no extra files
RUN ./kickstart.sh "downloaded and loaded!" && \
    rm /plugins/floodgate/key.pem && \
    rm eaglercraft_auths.db && \
    rm eaglercraft_skins_cache.db

# entrypoint
CMD [ "/run.sh" ]

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
