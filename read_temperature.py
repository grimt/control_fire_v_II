#!/usr/bin/env python

# modules to read from the flirc
from threading import Thread, Event
import Adafruit_DHT
import RPi.GPIO as GPIO

#import sys
import time
#import datetime 

import logging
import logging.handlers

LOG_FILENAME = '/var/log/control_fire.log'
 
# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s  %(message)s')
 
# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler( LOG_FILENAME, maxBytes=20000, backupCount=5)  
handler.setFormatter(formatter)

my_logger.addHandler(handler)

my_logger.debug ('Start logging')
#
ON = True
OFF = False


DEBUG_LEVEL_0 = 0 # Debug off
DEBUG_LEVEL_1 = 1
DEBUG_LEVEL_2 = 2
DEBUG_LEVEL_6 = 6



IN_MEASURE_TEMP_PIN = 4

DHT_22 = 22

# Functions to move date between threads using temporary  files.
# This mechanism may change


def read_measured_temp_from_file ():
    temp = my_fire.measured_temp_get() 
    try:
        f = open ('/tmp/measured_temperature.txt','rt')
        temp = f.read ()
        f.close ()
    except IOError:
        if my_fire.debug_level >=2:
    	    print ("Cant open file measured_temperature.txt for reading")
        my_logger.exception ("Cant open file measured_temperature.txt for reading")
 
    return temp


def write_measured_temp_to_file (temp):

    try:
        f = open ('/tmp/measured_temperature.txt','wt')
        f.write ('{0:0.1f}'.format(temp))
        f.close ()
    except IOError:
        if my_fire.debug_level >= 2:
            print ("Cant open file measured_temperature.txt for writing")
        my_logger.exception ("Cant open file measured_temperature.txt for writing")
		

# Higher level functions to move the temperature data between threads. Currently
# Try using queues to move the data 


def update_measured_temp (temp):
    write_measured_temp_to_file (temp)

def read_measured_temp():
    return read_measured_temp_from_file()


#---------------------------------------------------------------------------------

# Main thread:

# Init the hardware
init_GPIO ()

debug_level = DEBUG_LEVEL_6

# Read the temperature from the DHT22 temperature sensor.
    
while True:
    humidity, temperature = Adafruit_DHT.read(DHT_22,IN_MEASURE_TEMP_PIN )

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).  
    # If this happens try again!

    if humidity is not None and temperature is not None:
        if debug_level > 5:
            print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        #my_logger.info ('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        update_measured_temp (temperature)
        time.sleep(10)
    else:
        if debug_level > 5:
            print 'Failed to get reading. Try again!'
        #my_logger.info('Failed to read temp')
        time.sleep(2)
