# Skyler Puckett
# Initial Testing for Telemetry code
# Instructions to set up PI for serial communication
# https://pimylifeup.com/raspberry-pi-serial/
# serial library/documentation
# https://pyserial.readthedocs.io/en/latest/tools.html

#!/usr/bin/env python
import time
import serial

ser = serial.Serial(
        port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
counter = 0
print("serial initialed")

while 1:
        string = "Write counter" + str(counter)
        ser.write(string.encode('utf-8'))
        print("serial loop: " + str(counter))
        time.sleep(1)
        counter += 1
