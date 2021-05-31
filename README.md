## Build intructions

### If you like Docker, install docker, start it running in the backgrount, and run the following commands:
```
docker build --tag ground_station:latest .
```
To build - on the first go, this will take a few minutes. You may have to run this after updating the code. Now run:

```
docker run --rm -it --network=host ground_station:latest
```
To start the ground code!

# If you don't like docker:

* Dependencies:
    you must have cloned the [satelliteSim](https://github.com/AlbertaSat/SatelliteSim/) (or at least the [libcsp](https://github.com/AlbertaSat/SatelliteSim/) repo) and initialized the submodules

* Building libcsp:
    Go to libcsp root directory and configure the project as follows,
    ```./waf configure --with-os=posix --enable-rdp --enable-hmac --enable-xtea --enable-crc32 --with-loglevel=debug --enable-debug-timestamp --enable-python3-bindings --with-driver-usart=linux --enable-examples```

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

## The command language:

The ground station parses commands according to the following context free grammar described in BNF:

    <command> := <server name> "." <service name> "." <subservice name>
            <arguments>
    <arguments> := "" | "(" <argument list> ")"
    <argument list> := <argument value> | <argument value> "," <argument list>
    <argument value> := string | number
    <server name> := "OBC" | "EPS"
    <service name> := "ADCS" | "PAYLOAD" | "HOUSEKEEPING" | "SCHEDULING" | ...
    <subservice name> := "GET_FREQUENCY" | "GET_SPINRATE" | ...


Using this description, a parser has been constructed that will allow us to add new command structure objects which describe the valid combinations of services, subservices, and arguments, along with the return types in the TM response; the command structure objects also describe the mapping from the service and subservice names to the CSP ID and port numbers. Such a command description is shown for the housekeeping ‘parameter_report’ subservice.
'HOUSEKEEPING': {
    'port': 9,
    'subservice': {
        'PARAMETER_REPORT': {
            'subPort': 0,
            'inoutInfo': {
                'args': ['>B'],
                'returns': {
                    'err': '>b',
                    'structureID': '>B',
                    'temp': '>f4',
                }
            }
        }
    }
}
Code Snippet 5: Command structure object
Incoming TM responses are automatically parsed to the return types described in the command structure object. Note that all command responses shall have the first (signed) byte as the error code, which is ‘0’ upon success.


