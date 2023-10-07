Note: this repository uses yarn for run and build scripts. Scripts can be created and modified within package.json.

# Installation Instructions

## Prerequisites

If you're installing for the first time on a given machine, run the following before continuing:
```
bash install.sh
```

Also, you will need to make sure that you have yarn.

```
sudo npm install --global yarn
```

## Basic Functionality

Step 1: Install dependencies and run the ground station.

```
yarn install_dependencies
yarn csp:clone
```

Step 2: Build the ground station. For isolated backend software testing, run:
```
yarn build
```
Or if you intend to run the ground station with the Software Defined Radio (SDR):
```
yarn build:gnuradio
```
Step 3: Run the existing tests, before and after development:

```
yarn test_uhf <options>
yarn test_sband <options>
```

## Using This Repository with a UHF SDR

If using this repository with the satellites or the flatsat, follow these instructions. Hardware setup steps are excluded.

Step 4: Install conda (if not already present) by following the [conda installation instructions](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#installing-conda-on-a-system-that-has-other-python-installations-or-packages). 
We use a conda environment to run GNURadio, because there are additional GNURadio dependencies (out-of-tree modules) that we use in the ground station.

Step 5: Set up the AlbertaSat GNURadio Ground Station, which uses [radioconda](https://github.com/ryanvolz/radioconda). 
This will install our environment and all blocks needed, so there is no need to manually install other dependencies.
```
conda create -n radioconda -c conda-forge -c ryanvolz --only-deps radioconda
conda activate radioconda
conda install --file https://github.com/ryanvolz/radioconda/releases/download/2023.07.26/radioconda-win-64.lock
gnuradio-companion
```

This should open GNURadio 3.10.7. Open and run the relevant flow graph for your application in `libcsp/ex2_sdr/gnuradio/uhf/` or  `libcsp/ex2_sdr/gnuradio/sband/`. Note: the first time this is run on a new machine, gnuradio will prompt you to run uhd_images_downloader.py from the proper directory path.  

Step 6: Install Gpredict on your machine, if it's not already present. This is only necessary when tracking a satellite that is in orbit. If you want to run the ground station without doppler correction, you will likely need to disable the Gpredic doppler

```
sudo apt install gpredict
gpredict
```

In Gpredict preferences, set your ground station location. Also, set TLE auto-update to daily, and have "If TLEs are too old:" set to "Perform automatic update in the background." Create a new module in the "File" tab with the satellites of interest selected.

Finally, you can run the relevant ground station application (e.g. cli, sat_cli, ftp) using yarn, making sure to use the correct arguments for what you're doing.

```
yarn cli -I sdr -u -s EX2
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

## Example Commands for Operators

Action: Open command line interface for Ex-Alta 2. Encryption key files are local to ground station.
```
yarn cli -u -s EX2 --hkeyfile test_key.dat --xkeyfile test_key.dat
```

Action: Upload local file tosat.txt to YukonSat, in adcs directory. Encryption key files are local to ground station.
```
yarn ftp -p tosat.txt -o adcs/onsat.txt -u --hkeyfile test_key.dat --xkeyfile test_key.dat -s YKS
```

Action: Open sat_cli terminal interface for AuroraSat.
```
yarn sat_cli -I sdr -u -s ARS --hkeyfile test_key.dat --xkeyfile test_key.dat
```
Action: Resume firmware update already in progress to Ex-Alta 2.
```
yarn sat_update -I sdr -u -f Exalta2.bin -r -s EX2
```

You are now good to go, enjoy!
