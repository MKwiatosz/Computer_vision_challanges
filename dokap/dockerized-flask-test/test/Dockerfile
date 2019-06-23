FROM alpine:3.7
RUN apk add --no-cache curl bash
COPY app_test.sh /var/
WORKDIR /var/
ENTRYPOINT [ "bash" ]
CMD ["app_test.sh"]