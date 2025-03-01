ARG BUILD_FROM
ARG BUILD_ARCH

FROM debian:latest

RUN apt-cache depends --recurse --no-recommends --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances apt | grep "^\w" | sort -u
# RUN apt-cache depends --recurse apt
# RUN apt-cache rdepends --recurse --installed apt
RUN dpkg-query -L apt

RUN apt-cache depends --recurse --no-recommends --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances dpkg | grep "^\w" | sort -u
RUN dpkg-query -L dpkg


RUN apt-get update && apt-get upgrade -y && apt-get install -y gnupg wget

RUN apt-cache depends --recurse --no-recommends --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances wget | grep "^\w" | sort -u
RUN dpkg-query -L wget


FROM ${BUILD_FROM}

USER root


# we need /bin/sh
COPY --from=busybox:1.35.0-uclibc /bin/sh /bin/sh

COPY --from=0 /bin/bash /bin/bash

COPY --from=0 /bin/rm /bin/rm
COPY --from=0 /bin/xargs /bin/xargs
COPY --from=0 /bin/grep /bin/grep
COPY --from=0 /bin/uname /bin/uname
COPY --from=0 /bin/sleep /bin/sleep
COPY --from=0 /bin/chmod /bin/chmod
COPY --from=0 /bin/chown /bin/chown
COPY --from=0 /bin/mkdir /bin/mkdir

COPY --from=0 /usr/bin/dpkg /usr/bin/dpkg
COPY --from=0 /usr/bin/tar /usr/bin/tar
COPY --from=0 /usr/bin/diff /usr/bin/diff
COPY --from=0 /usr/bin/mktemp /usr/bin/mktemp
COPY --from=0 /usr/bin/chmod /usr/bin/chmod
COPY --from=0 /usr/bin/sed /usr/bin/sed
COPY --from=0 /usr/bin/touch /usr/bin/touch
COPY --from=0 /usr/bin/readlink /usr/bin/readlink
COPY --from=0 /usr/bin/sort /usr/bin/sort
COPY --from=0 /usr/bin/cp /usr/bin/cp
COPY --from=0 /usr/bin/mv /usr/bin/mv
COPY --from=0 /usr/bin/find /usr/bin/find
COPY --from=0 /usr/bin/awk /usr/bin/awk
COPY --from=0 /usr/bin/cat /usr/bin/cat
COPY --from=0 /usr/bin/cut /usr/bin/cut
COPY --from=0 /usr/bin/tr /usr/bin/tr
COPY --from=0 /usr/bin/comm /usr/bin/comm
COPY --from=0 /usr/bin/base64 /usr/bin/base64
COPY --from=0 /usr/bin/wget /usr/bin/wget
COPY --from=0 /usr/bin/dirmngr /usr/bin/dirmngr
COPY --from=0 /usr/bin/basename /usr/bin/basename
COPY --from=0 /usr/bin/getent /usr/bin/getent
COPY --from=0 /usr/bin/deb-systemd-helper /usr/bin/deb-systemd-helper

COPY --from=0 /usr/sbin/adduser /usr/sbin/adduser
COPY --from=0 /usr/sbin/ldconfig /usr/sbin/ldconfig
COPY --from=0 /usr/sbin/start-stop-daemon /usr/sbin/start-stop-daemon

COPY --from=0 /usr/bin/apt /usr/bin/apt
COPY --from=0 /usr/bin/apt-cache /usr/bin/apt-cache
COPY --from=0 /usr/bin/apt-cdrom /usr/bin/apt-cdrom
COPY --from=0 /usr/bin/apt-config /usr/bin/apt-config
COPY --from=0 /usr/bin/apt-get /usr/bin/apt-get
COPY --from=0 /usr/bin/apt-key /usr/bin/apt-key
COPY --from=0 /usr/bin/apt-mark /usr/bin/apt-mark
COPY --from=0 /usr/bin/gpgv /usr/bin/gpgv
COPY --from=0 /usr/bin/gpg /usr/bin/gpg

COPY --from=0 /usr/bin/dpkg-deb /usr/bin/dpkg-deb
COPY --from=0 /usr/bin/dpkg-divert /usr/bin/dpkg-divert
COPY --from=0 /usr/bin/dpkg-maintscript-helper /usr/bin/dpkg-maintscript-helper
COPY --from=0 /usr/bin/dpkg-query /usr/bin/dpkg-query
COPY --from=0 /usr/bin/dpkg-realpath /usr/bin/dpkg-realpath
COPY --from=0 /usr/bin/dpkg-split /usr/bin/dpkg-split
COPY --from=0 /usr/bin/dpkg-statoverride /usr/bin/dpkg-statoverride
COPY --from=0 /usr/bin/dpkg-trigger /usr/bin/dpkg-trigger
COPY --from=0 /usr/bin/update-alternatives /usr/bin/update-alternatives

COPY --from=0 /usr/lib /usr/lib
COPY --from=0 /usr/libexec/dpkg /usr/libexec/dpkg
# COPY --from=0 /usr/libexec/gpg /usr/libexec/gpg
COPY --from=0 /lib/x86_64-linux-gnu /lib/x86_64-linux-gnu
COPY --from=0 /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=0 /usr/share/dpkg /usr/share/dpkg
COPY --from=0 /usr/sbin/dpkg-fsys-usrunmess /usr/sbin/dpkg-fsys-usrunmess
COPY --from=0 /usr/sbin/dpkg-preconfigure /usr/sbin/dpkg-preconfigure


# COPY --from=0 /usr/lib/apt /usr/lib/apt
# COPY --from=0 /usr/lib/dpkg /usr/lib/dpkg
# COPY --from=0 /usr/lib/x86_64-linux-gnu/libapt-private.so.0.0.0 /usr/lib/x86_64-linux-gnu/libapt-private.so.0.0.0
# COPY --from=0 /usr/lib/x86_64-linux-gnu/libapt-private.so.0.0 /usr/lib/x86_64-linux-gnu/libapt-private.so.0.0
# COPY --from=0 /usr/lib/x86_64-linux-gnu/libapt-pkg.so.6.0 /usr/lib/x86_64-linux-gnu/libapt-pkg.so.6.0

COPY --from=0 /var/log/apt /var/log/apt
COPY --from=0 /var/cache/apt /var/cache/apt
COPY --from=0 /var/lib/apt /var/lib/apt
COPY --from=0 /var/lib/dpkg /var/lib/dpkg
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
RUN dpkg --configure -a
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 0E98404D386FA1D9 6ED0E7B82643E131 F8D2585B8783D481

RUN apt-get -f install

RUN apt-get reinstall -y apt dpkg gnupg gpgv libc6

RUN apt-cache depends apt | grep '[ |]Depends: [^<]' | cut -d: -f2 | tr -d ' ' | xargs apt-get --reinstall install -y

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    curl

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
