CC=gcc
CFLAGS=-I equipment_handler/include/ -I hardware_interface/include/
DEPS = equipment_handler/include/uhf_uart.h equipment_handler/include/i2c_dummy.h equipment_handler/include/uTransceiver.h hardware_interface/include/uhf.h
OBJ = hardware_interface/source/uhf.o equipment_handler/source/i2c_dummy.o equipment_handler/source/uTransceiver.o main.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

uhf_commands: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

.PHONY: clean

clean:
	rm -f *.o ./**/source/*.o uhf_commands