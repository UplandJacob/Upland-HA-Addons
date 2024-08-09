ARG BUILD_FROM
FROM $BUILD_FROM

COPY install.sh /
RUN chmod a+x /install.sh
CMD [ "/install.sh" ]

COPY run.sh /
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]