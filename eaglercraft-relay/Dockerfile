ARG BUILD_FROM
FROM ${BUILD_FROM}

# Add rootfs
#COPY rootfs/ /

# Uses /bin for compatibility purposes
# hadolint ignore=DL4005
RUN if [ ! -f /bin/sh ] && [ -f /usr/bin/sh ]; then ln -s /usr/bin/sh /bin/sh; fi && \
    if [ ! -f /bin/bash ] && [ -f /usr/bin/bash ]; then ln -s /usr/bin/bash /bin/bash; fi


RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    sudo curl default-jre

RUN curl --no-progress-meter \
    -H "Accept-Encoding: identity" \
    -H "Accept-Language: en" -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4.212 Safari/537.36" \
    -o /relay.zip \
    "https://git.eaglercraft.rip/eaglercraft/eaglercraft-1.8/raw/branch/main/sources/resources/relay_download.zip"


#more to add


# entrypoint
CMD [ "/run.sh" ]