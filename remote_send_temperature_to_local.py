
# Note this file is for the pi II - REMOTE PI

# Send the measured and desired temperatures from the remote
# pi to the local pi.

# Only send the desired temperature if it has changed from the last
# time the desired temperature was sent. This is because the desired
# temperature can also be set at the local pi from a remote control
# so we don't want to override. In other words the latest desired
# temperature to be set should be the one that counts regardless
# of where it came from.
#
# The measured temperature on the other hand should always come
# from the remote pi if its available.

# In either case, this is implemented by sending 555 if the
# desired temperature has not changed or the measured temperature
# is not available.

import sys
import Adafruit_DHT
import time
import socket   #for sockets
from Adafruit_7Segment import SevenSegment

import gc

import RPi.GPIO as GPIO

import logging
import logging.handlers

def init_logging:
    LOG_FILENAME = '/var/log/remote_send_temperature.log'
    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s  %(message)s')
 
    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler( LOG_FILENAME, maxBytes=20000, backupCount=5)  
    handler.setFormatter(formatter)

    my_logger.addHandler(handler)

    my_logger.debug ('Start logging')
    

def read_desired_temperature_from_file():
    temp = '555'
    try:
        f = open ('./desired_temperature.txt','rt')
        temp = f.read ()
        f.close ()
    except IOError:
            my_logger.exception ("Cant open file desired_temperature.txt for reading")
    return temp

def write_desired_temperature_to_file(temperature):
    try:
        f = open ('./desired_temperature.txt', 'wt')
        f.write (str(temperature))
        f.close ()

    except IOError:
            my_logger.exception ("Cant open file temperature.txt for writing")
            
def read_measured_temperature_from_file():
    temp = '555'
    try:
        f = open ('/tmp/measured_temperature.txt','rt')
        temp = f.read ()
        f.close ()
    except IOError:
        my_logger.exception ("Cant open file measured_temperature.txt for reading")
    return temp   


def write_temp_to_led (temp):
  segment.writeDigit(0, int(temp / 10))     # Tens
  segment.writeDigit(1, int(temp % 10))          # Ones
  decimal = temp - int(temp)
  decimal = decimal *10
  segment.writeDigit(3, int(decimal % 10))   # Tens
  # Toggle colon
  segment.setColon(1)              # Toggle colon at 1Hz 


init_logging ()

GPIO.setmode(GPIO.BCM)

#setup i2c
segment = SevenSegment(address=0x70)

port = 5000;

remote_ip = '192.168.1.151'

gc_count = 0
desired_temperature_changed = False

# First read the desired temperature from the file
# last_desired_temperature_reading = int (read_desired_temperature_from_file())

while True:

    #create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        my_logger.exception 'Failed to create socket'
        sys.exit()

    try:
        s.connect((remote_ip , port))
    except socket.error:
        my_logger.exception 'connection refused'
   
   
    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).  
    # If this happens try again!
    # desired_temp = int(read_desired_temperature_from_file())
    # if last_desired_temperature_reading != desired_temp:
    #     dtemp = "R:" + str(desired_temp) + ":"
    #   last_desired_temperature_reading = desired_temp
    # else:
    # Desired temperature is being sent straight from the button press.
    dtemp = "R:" + "555" + ":"
        
#   Read the measured temperature from a file.
    temperature = float (read_measured_temperature_from_file())

    rtemp = "M:" + "%.3f" % temperature
    write_temp_to_led(temperature)

    time.sleep(2)


    temp = dtemp + rtemp
    
    try :
        #Connect to remote server
        s.sendall(temp)
    except socket.error:
        #Send failed
        my_logger.exception ('Send failed')
    s.close()


        

# Suspect repeated allocation of socket may be chewing up memory so garbage collect
    if gc_count > 5:
        gc_count = 0
        gc.collect()
    else:
        gc_count += 1
    time.sleep(2)
