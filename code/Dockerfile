# Uses the Debian Bullseye image as the base for the container.
FROM debian:bullseye
# apt from prompting for user input during package installs.
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    git \
    subversion \
    pkg-config \
    libedit-dev \
    uuid-dev \
    libjansson-dev \
    libxml2-dev \
    libssl-dev \
    libsqlite3-dev \
    libncurses5-dev \
    libnewt-dev \
    libcurl4-openssl-dev \
    libspeex-dev \
    libspeexdsp-dev \
    libvorbis-dev \
    libopus-dev \
    libogg-dev \
    libsrtp2-dev \
    libtool \
    autoconf \
    automake \
    unzip

  WORKDIR /usr/src

  RUN wget http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-20-current.tar.gz \
  && tar xvfz asterisk-20-current.tar.gz \
  && cd asterisk-20.* \
  && contrib/scripts/get_mp3_source.sh \
  && ./configure --with-jansson-bundled \
  && make menuselect.makeopts \
  && menuselect/menuselect --enable chan_pjsip --enable res_http_websocket menuselect.makeopts \
  && make -j$(nproc) \
  && make install \
  && make samples \
  && make config

#COPY configs/ /etc/asterisk/

COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 5060/udp 5060/tcp 8088/tcp 10000-20000/udp

CMD ["/run.sh"]

