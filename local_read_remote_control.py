#!/usr/bin/env python

# Read input from remote control representing the
# desired temperature. Put this desired temperature
# in to a file.
#
# This is for the LOCAL PI.
#
# The remote in the filename refers to remote control

# modules to read from the flirc
from evdev import InputDevice, categorize, ecodes
#from threading import Thread, Event
from Queue import Queue
#import Adafruit_DHT
import RPi.GPIO as GPIO
from threading import Thread, Event

import time

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

# Key definitions
REMOTE_KEY_NONE = 0
REMOTE_KEY_RED = 2
REMOTE_KEY_GREEN = 3
REMOTE_KEY_YELLOW = 4
REMOTE_KEY_BLUE = 5 

# GPIO PINs
OUT_DESIRED_TEMP_GREEN_LED = 25
OUT_DESIRED_TEMP_YELLOW_LED = 21
OUT_DESIRED_TEMP_BLUE_LED = 22


def init_GPIO():
    GPIO.setwarnings(False)
    GPIO.setmode (GPIO.BCM)

    GPIO.setup (OUT_DESIRED_TEMP_GREEN_LED, GPIO.OUT)
    GPIO.setup (OUT_DESIRED_TEMP_YELLOW_LED, GPIO.OUT)
    GPIO.setup (OUT_DESIRED_TEMP_BLUE_LED, GPIO.OUT)


# Right now we are passing data between threads by writing to a file.
# This may change in the future. These abstractions allow for the
# data communication  method to change.


def switch_on_desired_temp_led (key):
    # First set all the desired temp LEDs to off
    GPIO.output (OUT_DESIRED_TEMP_GREEN_LED, False)
    GPIO.output (OUT_DESIRED_TEMP_YELLOW_LED, False)
    GPIO.output (OUT_DESIRED_TEMP_BLUE_LED, False)

    if key == REMOTE_KEY_GREEN:
       GPIO.output (OUT_DESIRED_TEMP_GREEN_LED, True) 
    elif key == REMOTE_KEY_YELLOW:
        GPIO.output (OUT_DESIRED_TEMP_YELLOW_LED, True)
    elif key == REMOTE_KEY_BLUE:
        GPIO.output (OUT_DESIRED_TEMP_BLUE_LED, True)


# Functions to move date between threads using temporary  files.
# This mechanism may change


def read_desired_temp_from_file():
    temp = 0
    try:
        f = open ('/tmp/desired_temperature.txt','rt')
        temp = f.read ()
        f.close ()
    except IOError:
        if debug_level >=DEBUG_LEVEL_2:
            print ("Cant open file desired_temperature.txt for reading")
        my_logger.exception("Cant open file desired_temperature.txt for reading")

    return temp

def write_desired_temp_to_file (key):
   
    if key == REMOTE_KEY_RED:
        # The red remote button toggles the fire off/on irrespective of
        # temperature. This is represented in the file by:
        # on = 999
        # off = 0
        # To Toggle the temperature we must first read it from the file.
        desired_temperature = 0
        temp = read_desired_temp ()
        desired_temperature = int (temp)
        if desired_temperature == 0:
            desired_temperature = 999
        elif desired_temperature > 0:
            desired_temperature = 0
    
    elif key == REMOTE_KEY_GREEN:
        desired_temperature = 19
    elif key == REMOTE_KEY_YELLOW:
        desired_temperature = 20
    elif key == REMOTE_KEY_BLUE:
        desired_temperature = 21
    elif key == REMOTE_KEY_NONE:
        desired_temperature = 0

    try:
        f = open ('/tmp/desired_temperature.txt','wt')
        f.write (str (desired_temperature))
        f.close ()
    except IOError:
        if debug_level >= DEBUG_LEVEL_2:
    	    print ("Cant open file temperature.txt for writing")
        my_logger.exception ("Cant open file desired_temperature.txt for writing")

def update_desired_temp (key_press):
    switch_on_desired_temp_led (key_press)
    write_desired_temp_to_file (key_press)
    # remote_read_q.put(key_press)

def read_desired_temp():
    return (read_desired_temp_from_file ())
    #return (read_remote_q.get())

#---------------------------------------------------------------------------------


# Init the hardware
init_GPIO ()


update_desired_temp (REMOTE_KEY_NONE)

debug_level = DEBUG_LEVEL_6 

dev = InputDevice ('/dev/input/event0')
if debug_level >= 5:
    print (dev)
for event in dev.read_loop():
    #
    # type should always be 1 for a keypress
    # code is the numeric value of the key that has been pressed
    # value 0 = key up, 1 = key down, 2 = key hold

    if event.type == ecodes.EV_KEY:
        if debug_level >= 5:
            print (categorize(event))
            print ( 'type: ' + str (event.type) + ' code: ' + str (event.code) + ' value ' + str (event.value))
        if event.value == 0:  # key up
            if event.code == REMOTE_KEY_RED or event.code == REMOTE_KEY_GREEN or event.code == REMOTE_KEY_YELLOW or event.code == REMOTE_KEY_BLUE:
                update_desired_temp (event.code) 
                time.sleep(1)

