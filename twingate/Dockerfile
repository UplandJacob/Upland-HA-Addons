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
    sudo curl 

# pulumi
#RUN apt-get python3-venv python3-pip
#RUN curl -fsSL https://get.pulumi.com | sh
#RUN pip install twingate-connector
#RUN pulumi new
#would require some more

# helm
RUN curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null && \
    sudo apt-get install apt-transport-https --yes && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list && \
    sudo apt-get update && \
    sudo apt-get install helm
RUN helm repo add twingate https://twingate.github.io/helm-charts
#RUN helm upgrade --install twingate-connector twingate/connector -n default --set connector.network="test" --set connector.accessToken="" --set connector.refreshToken=""

# copy needed files and set executable 
COPY twingate-install.sh /twingate-install.sh
COPY run.sh /run.sh
RUN chmod a+x /run.sh /twingate-install.sh

# entrypoint
CMD [ "/run.sh" ]

