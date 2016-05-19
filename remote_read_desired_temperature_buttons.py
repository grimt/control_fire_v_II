# This is for the remote pi
# Process button press interrupts which
# allow the user to set a desired temperature.

import RPi.GPIO as GPIO
import socket 
import time
import logging
import logging.handlers

def init_logging():
    LOG_FILENAME = '/var/log/remote_read_desired_temp.log'
    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s  %(message)s')
 
    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler( LOG_FILENAME, maxBytes=20000, backupCount=5)  
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
    my_logger.debug ('Start logging')
    return my_logger


def send_desired_temperature_to_local (temp):
    port = 5000;
    remote_ip = '192.168.1.151'
    
    #create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        my_logger.exception ('Failed to create socket')
        sys.exit()

    try:
        s.connect((remote_ip , port))
    except socket.error:
        my_logger.exception ('connection refused')
        
    dtemp = "R:" + temp + ":" + "M:" + "555"

    try :
        #Connect to remote server
        s.sendall(dtemp)
    except socket.error:
        #Send failed
        my_logger.exception ('Send failed')
    s.close()

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

def pin_12_callback(channel):
        # White Button
        desired_temperature = 19 
        write_desired_temperature_to_file(desired_temperature)
        send_desired_temperature_to_local (str (desired_temperature))



def pin_18_callback(channel):
        # Green Button
        desired_temperature = 999 
        write_desired_temperature_to_file(desired_temperature)
        send_desired_temperature_to_local (str (desired_temperature))

def pin_23_callback(channel):
        # Blue Button
        desired_temperature = int(read_desired_temperature_from_file())
        print "Desired " + str (desired_temperature)
        if desired_temperature > 0:
          desired_temperature = desired_temperature - 1
          write_desired_temperature_to_file(str(desired_temperature))
          send_desired_temperature_to_local (str (desired_temperature))

def pin_24_callback(channel):
        # Yellow button
        desired_temperature = int(read_desired_temperature_from_file())
        desired_temperature = desired_temperature + 1
        write_desired_temperature_to_file(str(desired_temperature))
        send_desired_temperature_to_local (str (desired_temperature))

def pin_25_callback(channel):
        # Red button
        desired_temperature = 0
        write_desired_temperature_to_file(str(desired_temperature))
        send_desired_temperature_to_local (str (desired_temperature))



my_logger = init_logging()

GPIO.setmode(GPIO.BCM)

GPIO.setup (12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect (12, GPIO.FALLING, callback=pin_12_callback, bouncetime=1000)



GPIO.setup (18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect (18, GPIO.FALLING, callback=pin_18_callback, bouncetime=1000)


GPIO.setup (23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect (23, GPIO.FALLING, callback=pin_23_callback, bouncetime=1000)

GPIO.setup (24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect (24, GPIO.FALLING, callback=pin_24_callback, bouncetime=1000)

GPIO.setup (25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect (25, GPIO.FALLING, callback=pin_25_callback, bouncetime=1000)


while True:
    #don't do much
    #balls_variable = 1
    time.sleep(2)
