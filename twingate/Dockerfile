ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apt-get update && apt-get install -y jq bash

COPY config.conf /etc/twingate/config.conf
COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

