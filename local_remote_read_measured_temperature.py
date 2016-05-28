#!/usr/bin/env python

# Read the temperature from the temperature sensors and place this
# temperature in a file.

# This script is run in both the LOCAL PI and REMOTE PI.

from threading import Thread, Event
import Adafruit_DHT
import RPi.GPIO as GPIO

#import sys
import time
#import datetime 

import logging
import logging.handlers
 
#
ON = True
OFF = False


DEBUG_LEVEL_0 = 0 # Debug off
DEBUG_LEVEL_1 = 1
DEBUG_LEVEL_2 = 2
DEBUG_LEVEL_5 = 5
DEBUG_LEVEL_6 = 6



IN_MEASURE_TEMP_PIN = 4

DHT_22 = 22

# Functions to move date between threads using temporary  files.
# This mechanism may change

def init_logging():
    LOG_FILENAME = '/var/log/local_remote_read_measured_temperature.log'
    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s  %(message)s')
 
    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler( LOG_FILENAME, maxBytes=20000000, backupCount=5)  
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
    my_logger.debug ('Start logging')
    return my_logger 

def write_measured_temp_to_file (temp):

    try:
        f = open ('/tmp/measured_temperature.txt','wt')
        f.write ('{0:0.1f}'.format(temp))
        f.close ()
    except IOError:
        my_logger.warning ("Cant open file measured_temperature.txt for writing")
		

# Higher level functions to move the temperature data between threads. Currently
# Try using queues to move the data 


def update_measured_temp (temp):
    write_measured_temp_to_file (temp)


#---------------------------------------------------------------------------------

# Main thread:


my_logger = init_logging()

debug_level = DEBUG_LEVEL_0

# Read the temperature from the DHT22 temperature sensor.
    
while True:
    humidity, temperature = Adafruit_DHT.read(DHT_22,IN_MEASURE_TEMP_PIN )

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).  
    # If this happens try again!

    if humidity is not None and temperature is not None:
        my_logger.info (',{0:0.1f},{1:0.1f}'.format(temperature, humidity))
        update_measured_temp (temperature)
        time.sleep(10)
    else:
        my_logger.debug ('Failed to get reading. Try again!')
        time.sleep(2)
