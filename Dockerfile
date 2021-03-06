### EGEOFFREY ###

### define base image
ARG SDK_VERSION
ARG ARCHITECTURE
FROM egeoffrey/egeoffrey-sdk-raspbian:${SDK_VERSION}-${ARCHITECTURE}

### install module's dependencies
RUN apt-get update && apt-get install -y rtl-sdr librtlsdr-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install rtl_433 (https://github.com/merbanan/rtl_433)
ENV RTL_433_VERSION=18.05
RUN wget https://github.com/merbanan/rtl_433/archive/$RTL_433_VERSION.zip \
  && unzip $RTL_433_VERSION.zip \
  && rm -f $RTL_433_VERSION.zip \
  && cd rtl_433-$RTL_433_VERSION/ \
  && mkdir build \
  && cd build \
  && cmake ../ \
  && make \
  && make install \
  && make clean

### copy files into the image
COPY . $WORKDIR
