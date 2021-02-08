FROM ubuntu:latest

WORKDIR /
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install wget -y
RUN apt-get install gcc-multilib g++-multilib -y
RUN apt install git -y
RUN apt-get install libsocketcan-dev -y

# install python
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && pip3 install numpy

# install zmq
RUN wget https://github.com/zeromq/libzmq/releases/download/v4.2.2/zeromq-4.2.2.tar.gz
RUN tar xvzf zeromq-4.2.2.tar.gz
RUN apt-get install -y libtool pkg-config build-essential autoconf automake uuid-dev
WORKDIR /zeromq-4.2.2
RUN ./autogen.sh
RUN ./configure
RUN make && make install
RUN apt-get install libzmq5 -y

WORKDIR /home/
RUN git clone https://github.com/albertasat/libcsp.git
WORKDIR /home/libcsp/
RUN git checkout upstream

RUN python3 waf configure --with-os=posix --enable-can-socketcan --enable-rdp --enable-hmac --enable-xtea --with-loglevel=debug --enable-debug-timestamp --enable-python3-bindings --with-driver-usart=linux --enable-if-zmqhub --enable-examples
RUN python3 waf build

WORKDIR /home/gs
COPY . .
CMD LD_LIBRARY_PATH=../libcsp/build PYTHONPATH=../libcsp/build python3 src/cli.py -I fifo

# FROM ubuntu:latest

# WORKDIR /
# ARG DEBIAN_FRONTEND=noninteractive
# RUN apt-get update
# RUN apt-get install build-essential -y
# RUN apt-get install wget -y
# RUN apt-get install gcc-multilib g++-multilib -y
# RUN apt install git -y
# RUN apt-get install libsocketcan-dev -y

# # install python
# RUN apt-get update \
#   && apt-get install -y python3-pip python3-dev \
#   && cd /usr/local/bin \
#   && ln -s /usr/bin/python3 python \
#   && pip3 install --upgrade pip \
#   && pip3 install numpy

# # install zmq
# RUN wget https://github.com/zeromq/libzmq/releases/download/v4.2.2/zeromq-4.2.2.tar.gz
# RUN tar xvzf zeromq-4.2.2.tar.gz
# RUN apt-get install -y libtool pkg-config build-essential autoconf automake uuid-dev
# WORKDIR /zeromq-4.2.2
# RUN ./autogen.sh
# RUN ./configure
# RUN make && make install
# RUN apt-get install libzmq5 -y

# # install libcsp
# WORKDIR /home/
# RUN git clone https://github.com/AlbertaSat/libcsp.git
# WORKDIR /home/libcsp/
# RUN git checkout upstream
# RUN python3 waf configure --with-os=posix --enable-can-socketcan --enable-rdp --enable-hmac --enable-xtea --with-loglevel=debug --enable-debug-timestamp --enable-python3-bindings --with-driver-usart=linux --enable-if-zmqhub --enable-examples
# RUN python3 waf build

# # install SatelliteSim
# WORKDIR /home/
# RUN git clone https://github.com/AlbertaSat/SatelliteSim.git
# WORKDIR /home/SatelliteSim
# # TODO: change this if we ever move away form the 64 bit branch:
# RUN git checkout 64bit
# RUN git submodule init
# RUN git submodule update
# WORKDIR /home/SatelliteSim/libcsp/
# RUN cp -r /home/libcsp/** .

# # Make FIFO files
# WORKDIR /datavolume1
# RUN mkfifo ground_to_sat sat_to_ground

# # Install services repo
# WORKDIR /home/
# RUN git clone https://github.com/AlbertaSat/ex2_services.git
# WORKDIR /home/ex2_services/
# RUN git checkout fifo

# WORKDIR /home/ex2_command_handling_demo/
# RUN cp -r /home/ex2_services/** .
# RUN ls
# RUN gcc ex2_demo_software/*.c Platform/demo/*.c Platform/demo/hal/*.c Services/*.c -c -D SYSTEM_APP_ID=_DEMO_APP_ID_ -I . -I ex2_demo_software/ -I Platform/demo -I Platform/demo/hal -I Services/ -I ../upsat-ecss-services/services/ -I ../SatelliteSim/Source/include/ -I ../SatelliteSim/Project/ -I ../libcsp/include/ -I ../SatelliteSim/Source/portable/GCC/POSIX/ -I ../libcsp/build/include/ -lpthread -std=c99 -lrt && ar -rsc client_server.a *.o

# WORKDIR /home/SatelliteSim
# RUN make clean && make all

# WORKDIR /home/gs
# COPY . .
# CMD /home/SatelliteSim/SatelliteSim & LD_LIBRARY_PATH=../libcsp/build PYTHONPATH=../libcsp/build python3 src/groundstation.py -I zmq
