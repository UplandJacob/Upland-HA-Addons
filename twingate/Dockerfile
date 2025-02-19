ARG BUILD_FROM
ARG BUILD_ARCH

FROM debian:latest

RUN apt-cache depends --recurse --no-recommends --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances apt | grep "^\w" | sort -u
# RUN apt-cache depends --recurse apt
# RUN apt-cache rdepends --recurse --installed apt
RUN dpkg-query -L apt

RUN apt-cache depends --recurse --no-recommends --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances dpkg | grep "^\w" | sort -u
RUN dpkg-query -L dpkg


# RUN apt-get update && apt-get upgrade -y && apt-get install -y wget curl



FROM ${BUILD_FROM}

# we need /bin/sh
COPY --from=busybox:1.35.0-uclibc /bin/sh /bin/sh
COPY --from=0 /usr/bin/apt /usr/bin/apt
COPY --from=0 /usr/bin/apt-cache /usr/bin/apt-cache
COPY --from=0 /usr/bin/apt-cdrom /usr/bin/apt-cdrom
COPY --from=0 /usr/bin/apt-config /usr/bin/apt-config
COPY --from=0 /usr/bin/apt-get /usr/bin/apt-get
COPY --from=0 /usr/bin/apt-key /usr/bin/apt-key
COPY --from=0 /usr/bin/apt-mark /usr/bin/apt-mark
COPY --from=0 /usr/lib /usr/lib
COPY --from=0 /lib/x86_64-linux-gnu /lib/x86_64-linux-gnu
COPY --from=0 /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=0 /usr/share/dpkg /usr/share/dpkg
# COPY --from=0 /usr/lib/apt /usr/lib/apt
# COPY --from=0 /usr/lib/dpkg /usr/lib/dpkg
# COPY --from=0 /usr/lib/x86_64-linux-gnu/libapt-private.so.0.0.0 /usr/lib/x86_64-linux-gnu/libapt-private.so.0.0.0
# COPY --from=0 /usr/lib/x86_64-linux-gnu/libapt-private.so.0.0 /usr/lib/x86_64-linux-gnu/libapt-private.so.0.0
# COPY --from=0 /usr/lib/x86_64-linux-gnu/libapt-pkg.so.6.0 /usr/lib/x86_64-linux-gnu/libapt-pkg.so.6.0

COPY --from=0 /var/lib/apt /var/lib/apt
COPY --from=0 /etc/apt /etc/apt

# Set S6 wait time
ENV S6_CMD_WAIT_FOR_SERVICES=1 \
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_SERVICES_GRACETIME=0

# Add rootfs
#COPY rootfs/ /

# Uses /bin for compatibility purposes
# hadolint ignore=DL4005
# RUN if [ ! -f /bin/sh ] && [ -f /usr/bin/sh ]; then ln -s /usr/bin/sh /bin/sh; fi && \
#     if [ ! -f /bin/bash ] && [ -f /usr/bin/bash ]; then ln -s /usr/bin/bash /bin/bash; fi

# RUN dpkg -i /tmp/apt.deb


# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    chmod curl

# Modules
ARG MODULES="00-banner.sh 00-global_var.sh"

# Automatic modules download
ADD "https://raw.githubusercontent.com/alexbelgium/hassio-addons/master/.templates/ha_automodules.sh" "/ha_automodules.sh"
RUN chmod 744 /ha_automodules.sh && /ha_automodules.sh "$MODULES" && rm /ha_automodules.sh

# Manual apps (NONE)
ENV PACKAGES=""
# Automatic apps & bashio
ADD "https://raw.githubusercontent.com/alexbelgium/hassio-addons/master/.templates/ha_autoapps.sh" "/ha_autoapps.sh"
RUN chmod 744 /ha_autoapps.sh && /ha_autoapps.sh "$PACKAGES" && rm /ha_autoapps.sh



# entrypoint
# CMD [ "/run.sh" ]

# Add entrypoint
ENV S6_STAGE2_HOOK=/ha_entrypoint.sh
ADD "https://raw.githubusercontent.com/alexbelgium/hassio-addons/master/.templates/ha_entrypoint.sh" "/ha_entrypoint.sh"

# Entrypoint modifications
ADD "https://raw.githubusercontent.com/alexbelgium/hassio-addons/master/.templates/ha_entrypoint_modif.sh" "/ha_entrypoint_modif.sh"
RUN chmod 777 /ha_entrypoint.sh /ha_entrypoint_modif.sh && /ha_entrypoint_modif.sh && rm /ha_entrypoint_modif.sh

ENTRYPOINT [ "/usr/bin/env" ]
CMD [ "/ha_entrypoint.sh" ]



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
