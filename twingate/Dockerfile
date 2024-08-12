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
    sudo curl git

# pulumi
#RUN apt-get python3-venv python3-pip
#RUN curl -fsSL https://get.pulumi.com | sh
#RUN pip install twingate-connector
#RUN pulumi new
#would require some more


# helm
RUN curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
RUN chmod 700 get_helm.sh
RUN ./get_helm.sh

RUN helm repo add twingate https://twingate.github.io/helm-charts
#RUN helm upgrade --install twingate-connector twingate/connector -n default --set connector.network="test" --set connector.accessToken="" --set connector.refreshToken=""


# copy needed files and set executable 
COPY twingate-install.sh /twingate-install.sh
COPY run.sh /run.sh
RUN chmod a+x /run.sh /twingate-install.sh

# entrypoint
CMD [ "/run.sh" ]

