# Installation Instructions

## If you like Docker...

First, ensure that Docker is installed and running in the background. Once that is done, run the following to build the image that we will be using:

```
docker build --tag ground_station:latest .
```

The image will take a few minutes to build on the first go so feel free to grab a coffee while you wait! Once the image is built, we can run a container off of it using:

```
docker run --rm -it --network=host ground_station:latest
```

You are now good to go, enjoy!

## If you don't like docker:

#### 1. You will need to first make sure you have yarn:
`sudo apt-get update`
`sudo apt-get install yarn -y`

#### 2. Install dependencies and run the ground station (may need to run with `sudo`):

`yarn build` (only need to run this once)

`yarn run:cli <options>`

e.g. `yarn run:cli -I uart -d /dev/ttyUSB0`

#### 3. Before and after development, the existing tests should be performed:

`yarn run:test_uhf <options>`

`yarn run:test_sband <options>`

#### Troubleshooting

On some systems, you may see something like:

`00h00m00s 0/0: : ERROR: [Errno 2] No such file or directory: 'build'`

If this occurs run the following command and then try step 2 again:

`bash install.sh`

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
