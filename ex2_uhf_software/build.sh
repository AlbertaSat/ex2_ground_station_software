#!/bin/bash
gcc -c -Wall -Werror -fpic /equipment_handler/source/uTransceiver.c uTransceiver.o
gcc -shared -o uTransceiver.so uTransceiver.o
