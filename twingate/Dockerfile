ARG BUILD_FROM
ARG BUILD_ARCH
# hadolint ignore=DL3007
FROM debian:latest as deb
#RUN apt-cache depends --recurse --no-recommends --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances apt | grep "^\w" | sort -u
#RUN dpkg-query -L apt
RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y gnupg wget
#########################################################################
FROM ${BUILD_FROM}
# hadolint ignore=DL3002
USER root
SHELL ["/bin/bash", "-c"]

# we need /bin/sh
COPY --from=busybox:1.35.0-uclibc /bin/sh /bin/sh
# and /bin/bash
COPY --from=deb /bin/bash /bin/bash

COPY --from=deb /bin/rm /bin/rm
COPY --from=deb /bin/xargs /bin/xargs
COPY --from=deb /bin/grep /bin/grep
COPY --from=deb /bin/uname /bin/uname
COPY --from=deb /bin/sleep /bin/sleep
COPY --from=deb /bin/chmod /bin/chmod
COPY --from=deb /bin/chown /bin/chown
COPY --from=deb /bin/mkdir /bin/mkdir
COPY --from=deb /bin/head /bin/head

COPY --from=deb /usr/bin/env /usr/bin/env
COPY --from=deb /usr/bin/dpkg /usr/bin/dpkg
COPY --from=deb /usr/bin/tar /usr/bin/tar
COPY --from=deb /usr/bin/diff /usr/bin/diff
COPY --from=deb /usr/bin/mktemp /usr/bin/mktemp
COPY --from=deb /usr/bin/chmod /usr/bin/chmod
COPY --from=deb /usr/bin/sed /usr/bin/sed
COPY --from=deb /usr/bin/touch /usr/bin/touch
COPY --from=deb /usr/bin/readlink /usr/bin/readlink
COPY --from=deb /usr/bin/sort /usr/bin/sort
COPY --from=deb /usr/bin/cp /usr/bin/cp
COPY --from=deb /usr/bin/mv /usr/bin/mv
COPY --from=deb /usr/bin/find /usr/bin/find
COPY --from=deb /usr/bin/awk /usr/bin/awk
COPY --from=deb /usr/bin/cat /usr/bin/cat
COPY --from=deb /usr/bin/cut /usr/bin/cut
COPY --from=deb /usr/bin/tr /usr/bin/tr
COPY --from=deb /usr/bin/comm /usr/bin/comm
COPY --from=deb /usr/bin/base64 /usr/bin/base64
COPY --from=deb /usr/bin/wget /usr/bin/wget
COPY --from=deb /usr/bin/dirmngr /usr/bin/dirmngr
COPY --from=deb /usr/bin/basename /usr/bin/basename
COPY --from=deb /usr/bin/getent /usr/bin/getent
COPY --from=deb /usr/bin/deb-systemd-helper /usr/bin/deb-systemd-helper

COPY --from=deb /usr/sbin/adduser /usr/sbin/adduser
COPY --from=deb /usr/sbin/ldconfig /usr/sbin/ldconfig
COPY --from=deb /usr/sbin/start-stop-daemon /usr/sbin/start-stop-daemon

COPY --from=deb /usr/bin/apt /usr/bin/apt
COPY --from=deb /usr/bin/apt-cache /usr/bin/apt-cache
COPY --from=deb /usr/bin/apt-cdrom /usr/bin/apt-cdrom
COPY --from=deb /usr/bin/apt-config /usr/bin/apt-config
COPY --from=deb /usr/bin/apt-get /usr/bin/apt-get
COPY --from=deb /usr/bin/apt-key /usr/bin/apt-key
COPY --from=deb /usr/bin/apt-mark /usr/bin/apt-mark
COPY --from=deb /usr/bin/gpgv /usr/bin/gpgv
COPY --from=deb /usr/bin/gpg /usr/bin/gpg

COPY --from=deb /usr/bin/dpkg-deb /usr/bin/dpkg-deb
COPY --from=deb /usr/bin/dpkg-divert /usr/bin/dpkg-divert
COPY --from=deb /usr/bin/dpkg-maintscript-helper /usr/bin/dpkg-maintscript-helper
COPY --from=deb /usr/bin/dpkg-query /usr/bin/dpkg-query
COPY --from=deb /usr/bin/dpkg-realpath /usr/bin/dpkg-realpath
COPY --from=deb /usr/bin/dpkg-split /usr/bin/dpkg-split
COPY --from=deb /usr/bin/dpkg-statoverride /usr/bin/dpkg-statoverride
COPY --from=deb /usr/bin/dpkg-trigger /usr/bin/dpkg-trigger
COPY --from=deb /usr/bin/update-alternatives /usr/bin/update-alternatives

COPY --from=deb /usr/lib /usr/lib
COPY --from=deb /usr/libexec/dpkg /usr/libexec/dpkg
# COPY --from=deb /usr/lib/apt /usr/lib/apt
# COPY --from=deb /usr/lib/dpkg /usr/lib/dpkg

COPY --from=deb /lib/x86_64-linux-gnu /lib/x86_64-linux-gnu
COPY --from=deb /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=deb /usr/share/dpkg /usr/share/dpkg
COPY --from=deb /usr/sbin/dpkg-fsys-usrunmess /usr/sbin/dpkg-fsys-usrunmess
COPY --from=deb /usr/sbin/dpkg-preconfigure /usr/sbin/dpkg-preconfigure

COPY --from=deb /var/log/apt /var/log/apt
COPY --from=deb /var/cache/apt /var/cache/apt
COPY --from=deb /var/lib/apt /var/lib/apt
COPY --from=deb /var/lib/dpkg /var/lib/dpkg
COPY --from=deb /etc/apt /etc/apt

# Set S6 wait time
ENV S6_CMD_WAIT_FOR_SERVICES=1 \
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_SERVICES_GRACETIME=0

# Add rootfs
#COPY rootfs/ /

# Uses /bin for compatibility purposes
# hadolint ignore=DL4005
RUN if [ ! -f /bin/sh ] && [ -f /usr/bin/sh ]; then ln -s /usr/bin/sh /bin/sh; fi && \
    if [ ! -f /bin/bash ] && [ -f /usr/bin/bash ]; then ln -s /usr/bin/bash /bin/bash; fi
# hadolint ignore=DL3008
RUN dpkg --configure -a && \
    apt-get -f install --no-install-recommends -y && \
    apt-get reinstall -y apt dpkg gnupg gpgv libc6 && \
    apt-cache depends apt | grep '[ |]Depends: [^<]' | cut -d: -f2 | tr -d ' ' | xargs apt-get --reinstall install -y

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    curl micro gzip xz-utils tar && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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
