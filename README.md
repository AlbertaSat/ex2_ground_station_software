# Installation Instructions

## Prerequisites

If you're installing for the first time on a given machine, run `bash install.sh` before continuing.

Also, you will need to make sure that you have yarn.

```
sudo apt-get update
sudo apt-get install yarn -y
```

## Basic Functionality

Step 1: install dependencies and run the ground station (may need to run with `sudo`).

```
yarn install_dependencies
yarn csp:clone
yarn build
yarn cli <options>
```

e.g. `yarn cli -I uart -d /dev/ttyUSB0`

Step 2: before and after development, the existing tests should be run:

```
yarn test_uhf <options>
yarn test_sband <options>
```

## Using This Repository with a UHF SDR

If using this repository for FlatSat testing or deployment, follow these slightly different instructions. Hardware setup steps are excluded.

Step 1: Follow [Ground Station Software Setup Guide](https://docs.google.com/document/d/1-BGoCOlOCisQk08cB9kHaWAGk-gdsx6xPlfZvo5EFBs/edit). Run the GNURadio flow graph you will be using for testing or operations.

Step 2: install dependencies and run the ground station (may need to run with `sudo`).

```
yarn install_dependencies
yarn csp:clone
yarn build:gnuradio
yarn cli -I SDR -u
```

## Command Documentation
Documentation for supported ground station commands can be found in [CommandDocs.txt](https://github.com/AlbertaSat/ex2_ground_station_software/blob/update-readme/CommandDocs.txt).

## The Command Language

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

```
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
```

#### Code Snippet 5: Command structure object
Incoming TM responses are automatically parsed to the return types described in the command structure object. Note that all command responses shall have the first (signed) byte as the error code, which is ‘0’ upon success.

## Docker Installation Method (deprecated and unstable)

First, ensure that Docker is installed and running in the background. Once that is done, run the following to build the image that we will be using:

```
docker build --tag ground_station:latest .
```

The image will take a few minutes to build on the first go so feel free to grab a coffee while you wait! Once the image is built, we can run a container off of it using:

```
docker run --rm -it --network=host ground_station:latest
```

You are now good to go, enjoy!
