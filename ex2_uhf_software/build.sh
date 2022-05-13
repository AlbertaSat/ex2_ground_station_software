#!/bin/bash
gcc -Iequipment_handler/include -Ihardware_interface/include -c -Wall -fpic equipment_handler/source/uTransceiver.c -o uTransceiver.o
gcc -Iequipment_handler/include -Ihardware_interface/include -c -Wall -fpic equipment_handler/source/gnuradio_interface.c -o gnuradio_interface.o
gcc -shared -o uTransceiver.so uTransceiver.o gnuradio_interface.o
rm gnuradio_interface.o
rm uTransceiver.o
