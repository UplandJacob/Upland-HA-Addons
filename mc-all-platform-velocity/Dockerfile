ARG BUILD_FROM
FROM ${BUILD_FROM}

ARG VELOCITY_VERS="3.4.0-SNAPSHOT"
ARG VELOCITY_BUILD="450"

ARG VIAVERSION_VERS="5.1.1"
ARG VIAREWIND_VERS="4.0.3"
ARG VIABACKWARDS_VERS="5.1.1"
	

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
#     yq curl default-jre 

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
