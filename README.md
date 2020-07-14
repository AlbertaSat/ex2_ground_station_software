## Build intructions

### If you like Docker, install docker, start it running in the backgrount, and run the following commands:
```
sudo docker build --tag ground_station:latest .
```
To build - on the first go, this will take a few minutes. You may have to run this after updating the code. Now run:

```
sudo docker run --rm -it --network=host ground_station:latest
```
To start the ground code!

# If you don't like docker:

* Dependencies:
    you must have cloned the [satelliteSim](https://github.com/AlbertaSat/SatelliteSim/) (or at least the [libcsp](https://github.com/AlbertaSat/SatelliteSim/) repo) and initialized the submodules

* Building libcsp:
    Go to libcsp root directory and configure the project as follows,
    ```./waf configure --with-os=posix --enable-rdp --enable-hmac --enable-xtea --with-loglevel=debug --enable-debug-timestamp --enable-python3-bindings --with-driver-usart=linux --enable-if-zmqhub --enable-examples```

    And then build csp,
    ```./waf build```

    NOTE: If your build fails due to socketcan calls, either try building with the ```--enable-can-socketcan``` option, or go comment out the 'pycsp_can_socketcan_init' function along with the line ```{"can_socketcan_init",  pycsp_can_socketcan_init,  METH_VARARGS, ""}``` from pycsp.c

    Note that this is built as a 64 bit program, and so you must remove the '-m32' CFLAG from the SatelliteSim makefile

* Now check that you have,
    a. a file called 'zmqproxy' in libcsp/build/. This executable will translate ZMQ requests to CSP on your local machine for development, and maybe for inter-ground station communication in the future.

    b. a file called libcsp_py3.so. This is the compiled version of libcsp/src/bindings/python/pycsp.c, and gives access to the CSP functions VIA a python class

* Running this ground groundStation code

    In the root directory of this project, run
    ```LD_LIBRARY_PATH=<relative_path_to_libcsp>/libcsp/build PYTHONPATH=<relative_path_to_libcsp>/libcsp/build python3 Src/groundStation.py -I zmq```

    NOTE: nothing will happen if either there is no xmqproxy running or if your CSP server is running!
