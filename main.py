#!/usr/bin/python
'''
    This is the main control script for the CC of CO RockSat 2021-2022 payload.

    Contributors:
	    Jillian Frimml
	    Skyler Puckett
        Konstantin Zaremski
    
    --- This product contains software from the previous payload written
        by Andrew Bruckbauer and Konstantin Zaremski for RockSat 2019 - 2021.
    
    Testing:
        The control program can be tested using the '--test' argument. Testing
        mode simulates a shutdown.
    
    Reset:
        The control program can be reset using the '--reset' argument.
        The reset argument clears any persisting save state so that operaiton
        can be tested as if running for the first time.
        $ python control.py --reset
        Flags can be supplied together (optional):    
        $ python control.py --reset --test
    
    Functionality:
        This program controls all payload functionality. All individual software
        subsystems for other experiments are integrated as modules that run in
        their own sub processes/threads. Timer events should be listened to within
        this file and not any of the other sub modules in case changes need to be 
        made to timing.
'''

# Import required modules
import time
import logging
from logging.handlers import RotatingFileHandler
import os
import multiprocessing as multiprocessing
import sys
import serial # used for telemetry

# Import system modules
import sensors
import fram
import armMotor
import telemetry_test_sensors


# Create a log folder if it does not exist yet
os.system('mkdir -p ./logs')
# Set up logging and log boot time
boottime = int(time.time())
rotatingFileHandler = RotatingFileHandler(
 	filename=f'logs/rocksat_payload_{str(boottime)}.log', 
  	mode='a',
  	maxBytes=20*1024*1024,
  	backupCount=2,
  	encoding='utf-8',
  	delay=0
)
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s.%(msecs)03d][%(module)7s][%(levelname)8s]\t%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[rotatingFileHandler])

# SET UP seerial RXD and TXD pins on Pi  8-N-1
# ser = serial.Serial(
#         port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
#         baudrate = 19200,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE,
#         bytesize=serial.EIGHTBITS,
#         timeout=1
# )
    
#formatter = logging.Formatter('[%(asctime)s.%(msecs)03d][%(module)7s][%(levelname)8s]\t%(message)s')

logger = logging.getLogger(__name__)

# Output all logs to console
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

logger.info(f'CC of CO payload finished booting at {boottime}')

# Entry point
if __name__ == '__main__':
    try:
        multiprocessing.set_start_method('fork')
        processQueue = multiprocessing.Queue()
        # Accept command line arguments
        
        # If no command line arguments are passed the script will assume that it is running in 
        arguments = sys.argv
        
        # Secondary experiment (radiation RAM)
        if ('--fram' in arguments or len(arguments) == 1):
            framExperimentThread = multiprocessing.Process(target=fram.main)
            framExperimentThread.start()

        # Tertiary experiment (sensors)
        if ('--sensors' in arguments or len(arguments) == 1):
            sensorThread = multiprocessing.Process(target=telemetry_test_sensors.main)
            sensorThread.start()

        # Arm Motor functions
        if ('--motor' in arguments or len(arguments) == 1):
            armMotor = multiprocessing.Process(target=armMotor.main)
            armMotor.start()
        # Read telemetry
        if ('--read' in arguments or len(arguments) == 1):
            telemetryRead = multiprocessing.Process(target=telemetry_read.main)
            telemetryRead.start()
        # Write Telemetry test
        if ('--read' in arguments or len(arguments) == 1):
            telemetryWrite = multiprocessing.Process(target=telemetry_test.main)
            telemetryWrite.start()
        # Prim
        #if framExperimentThread: framExperimentThread.join()
        #p1.terminate()
    except KeyboardInterrupt:
        print ('Caught KeyboardInterrupt exiting')
        
