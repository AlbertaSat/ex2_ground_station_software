Note: this repository uses yarn for run and build scripts. Scripts can be created and modified within package.json.

# Installation Instructions

## Prerequisites

If you're installing for the first time on a given machine, run `bash install.sh` before continuing.

Also, you will need to make sure that you have yarn.

```
sudo npm install --global yarn
```

## Basic Functionality

Step 1: install dependencies and run the ground station. In order to run as a user process your user may need to be in the `dialout` group

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

Step 1: Check if you have conda installed by running `conda`. If not installed, follow the [conda installation instructions](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#installing-conda-on-a-system-that-has-other-python-installations-or-packages).

Step 2: Set up GNURadio

```
conda create -n gnuradio-3.9.4
conda activate gnuradio-3.9.4
conda config --env --add channels conda-forge
conda config --env --set channel_priority strict
conda install gnuradio python=3.9.4
sudo apt install liblog4cpp5v5 liblog4cpp5-dev
conda install -c conda-forge gnuradio-satellites
sudo apt install libuhd-dev uhd-host
git clone https://github.com/AlbertaSat/ex2_sdr
```

Step 3: Install dependencies and build the ground station.

```
yarn install_dependencies
yarn csp:clone
yarn uhf:clone
yarn build:gnuradio
```

Step 4: Run the ground station. This must be done every new session.
```
conda activate gnuradio-3.9.4
gnuradio-companion
```
In GNURadio, open and run the relevant flow graph for your application in `ex2_sdr/gnuradio/uhf/` or  `ex2_sdr/gnuradio/sband/`. Note: the first time this is run on a new machine, gnuradio will prompt you to run uhd_images_downloader.py from the proper directory path. Do that, and then try running the flow graph again. Next, you can run the relevant ground station application (e.g. cli, sat_cli, ftp) using yarn, making sure to use the correct arguments for what you're doing.
```
yarn cli -I sdr -u
```
Step 5: Gpredict install. This is only necessary when tracking a satellite that is in orbit.

```
sudo apt install gpredict
gpredict
```
In Gpredict preferences, set your ground station location. Also, set TLE auto-update to daily, and have "If TLEs are too old:" set to "Perform automatic update in the background." Create a new module in the "File" tab with the satellites of interest selected.

Step 6: Doppler shift correction install. This is only necessary when tracking a satellite that is in orbit. Ensure gnuradio-companion is closed before proceeding.

```
sudo apt install doxygen
git clone https://github.com/gruffen/gr-gpredict-doppler-3.8.git
cd gr-gpredict-doppler-3.8
rm -r build
```
Follow all of the readme instructions in [gr-gpredict-doppler](https://github.com/wnagele/gr-gpredict-doppler), including "Setting up Gpredict". Gpredict can be started using the `gpredict` command. Type the following command (or manually copy over the .yml file).
```
cp ex2_sdr_install_path/gnuradio/utils/gpredict_doppler_doppler.block.yml /home/josh/miniconda3/envs/gnuradio-3.9.4/share/gnuradio/grc
```
Step 7: Run the ground station with doppler. This must be done every new session when talking to an in-orbit satellite.
Like Step 4, activate the gnuradio environment, open GNURadio, and open Gpredict. Open Gpredict's Radio Control and set the target uplink and downlink frequencies to 437.875000 MHz. Set the target to the satellite you want to track. Set the Device to GNURadio. Set the Cycle field to 100 msec. Select Track and Engage. In GNURadio, open and run the relevant flow graph for your application in `ex2_sdr/gnuradio/uhf/` or  `ex2_sdr/gnuradio/sband/`, ensuring that the file name has "doppler" in it. Next, you can run the relevant ground station application (e.g. cli, sat_cli, ftp) using yarn, making sure to use the correct arguments for what you're doing.

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

