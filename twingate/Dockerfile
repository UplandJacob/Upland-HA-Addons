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
    sudo python3-venv python3-pip

# pulumi
RUN curl -fsSL https://get.pulumi.com | sh
RUN pip install twingate-connector
RUN pulumi new




# copy needed files and set executable 
#COPY twingate-install.sh /twingate-install.sh
COPY run.sh /run.sh
RUN chmod a+x /run.sh

# entrypoint
CMD [ "/run.sh" ]

