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

#### 1. You will need to first make sure you have yarn:
`sudo apt-get update`
`sudo apt-get install yarn -y`

#### 2. Run install dependencies and run the ground station (may need to run with `sudo`):
`yarn build` (only need to run this once)

`yarn run:cli <options>`

e.g. `yarn run:cli -I uart -d /dev/ttyUSB0`

#### Troubleshooting

On some systems, you may see something like this:
```
00h00m00s 0/0: : ERROR: [Errno 2] No such file or directory: 'build'
```

In this case, you shold run the following command:

`bash install.sh`

Now try step 2 again.

Before and after development, the existing tests should be performed:

`yarn run:test_uhf`

`yarn run:test_sband`

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
`'HOUSEKEEPING': {
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
}`
Code Snippet 5: Command structure object
Incoming TM responses are automatically parsed to the return types described in the command structure object. Note that all command responses shall have the first (signed) byte as the error code, which is ‘0’ upon success.
