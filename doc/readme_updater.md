# Interacting with the bootloader

Most of the interaction with the bootloader is with the sat_cli

```
yarn sat_cli --help
```

The most commonly used sat_cli programs will be ```verifyapp``` and ```reboot```

Use verifyapp to check the crc16 of the application image.
Reboot will select the image to boot, A, B, or G for application, bootloader, and golden image respectively

Interesting bootloader information can be found with
```
bootinfo
```
```
appinfo
```
```
uptime
```
```
imagetype
```
```
error
```

The sat_cli implements a ```help``` command to get a list of bootloader cli commands.

Use ```hello``` to be nice to the bootloader :)

# Using the updater

The updater is set by default to update the application image. The only option needed in the default configuration is the binary image to upload.
```
yarn sat_update -f <binary_file_name>.bin
```

During satellite operations sdr will need to be used. this can be specified with. This is no different from regular operations
```
-I sdr
```
Other options can be found with
```bash
yarn sat_update --help
```

# How to issue an update

## First step:
You must compile a version of the obc_software with bootloader support.

To do this, find the file ```hl_sys_link.cmd``` in ex2_obc_software. In the file are some commented definitions
```cmd
#define GOLDEN_IMAGE
//#define APPLICATION_IMAGE
//#define BOOTLOADER_PRESENT
```
Uncomment the definition for the image you are creating and uncomment the definition for bootloader present. Rebuild the project.
In the Debug/ folder will be a binary file, probably named ex2_obc_software.bin. This will be the file for the software update. 

## Second step:

If you are updating the application image the defaults may be used

First, run
```bash
yarn sat_update -f <binary_file_name>.bin [-I sdr]
```
Then, verify the application image by running
```bash
yarn sat_cli [-I sdr]
```
Within sat_cli, use
```bash
verifyapp
```
If successful, you may reboot in to the application image
```bash
reboot A
```

# But what if my update gets interrupted?

Not to worry! Simply rerun the ```yarn sat_update``` command with the parameter ```-r``` and the programs will negotiate a resume

# A note on golden images

Right now the bootloader probably doesn't work with the golden image. It is unknown if this will change in the future or if golden image support will be removed.