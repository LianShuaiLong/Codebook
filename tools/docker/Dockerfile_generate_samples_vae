FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-devel-dalle

LABEL maintainer="l1091545654@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i "s#archive.ubuntu.com#mirrors.aliyun.com#g" /etc/apt/sources.list && \
    sed -i "s#security.ubuntu.com#mirrors.aliyun.com#g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libsm6 \
        python-opencv \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip --no-cache-dir install requests tornado

ADD ./ /root/
RUN chmod +x /root/start_service.sh
EXPOSE 80

WORKDIR /root
#ENTRYPOINT ./start_service.sh

