ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apt-get update && apt-get install -y jq bash sudo ha

COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

