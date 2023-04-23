#!/bin/bash

# Get the current date and time in the format YYYYMMDDHH
DATE=$(TZ=UTC date +"%Y%m%d%H%M")

# Create a new file with the current date and time in the name
FILENAME="ScriptLogs/$DATE-utc.txt"

# Record terminal output to the new file
script $FILENAME

