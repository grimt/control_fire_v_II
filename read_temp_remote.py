
# Note this file is for the pi II - REMOTE PI
# Next: Read measured temperature in a different script, write it to a file
#       Read here from a file.

import sys
import Adafruit_DHT
import time
import socket   #for sockets
from Adafruit_7Segment import SevenSegment

import gc

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#setup i2c
segment = SevenSegment(address=0x70)



def read_desired_temperature_from_file():
    temp = '555'
    try:
        f = open ('./desired_temperature.txt','rt')
        temp = int(f.read ())
        f.close ()
    except IOError:
            print ("Cant open file desired_temperature.txt for reading")
    return temp

def write_desired_temperature_to_file(temperature):
    try:
        f = open ('./desired_temperature.txt', 'wt')
        f.write (str(temperature))
        f.close ()

    except IOError:
            print ("Cant open file temperature.txt for writing")


def pin_12_callback(channel):
        # White Button
        print ('Pressed button 12 White')
        desired_temperature = 19 
        write_desired_temperature_to_file(desired_temperature)
        #Send temperature to remote pi is done in the while loop below



def pin_18_callback(channel):
        # Green Button
        print ('Pressed button 18 Green')
        desired_temperature = 999 
        write_desired_temperature_to_file(desired_temperature)
        #Send temperature to remote pi is done in the while loop below

def pin_23_callback(channel):
        # Blue Button
        print ('pressed button 23 Blue')
        desired_temperature = read_desired_temperature_from_file()
        if desired_temperature > 0:
          desired_temperature = desired_temperature - 1
          write_desired_temperature_to_file(desired_temperature)
        # send temperature to remote pi is done in the while loop below.

def pin_24_callback(channel):
        # Yellow button
        print ('pressed button 24 Yellow')
        desired_temperature = read_desired_temperature_from_file()
        desired_temperature = desired_temperature + 1
        write_desired_temperature_to_file(desired_temperature)
        # send temperature to remote pi is done in the while loop below.

def pin_25_callback(channel):
        # Red button
        print ('pressed button 25 Red')
        desired_temperature = 0
        write_desired_temperature_to_file(desired_temperature)
        # send temperature to remote pi is done in the while loop below.       

def write_temp_to_led (temp):
  segment.writeDigit(0, int(temp / 10))     # Tens
  segment.writeDigit(1, int(temp % 10))          # Ones
  decimal = temp - int(temp)
  print str(decimal)
  decimal = decimal *10
  segment.writeDigit(3, int(decimal % 10))   # Tens
  # Toggle colon
  segment.setColon(1)              # Toggle colon at 1Hz 

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




port = 5000;


remote_ip = '192.168.1.151'

gc_count = 0
desired_temperature_changed = False

# First read the desired temperature from the file
last_desired_temperature_reading = int (read_desired_temperature_from_file())

while True:

    #create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()

    try:
        s.connect((remote_ip , port))
    except socket.error:
        print 'connection refused'
   
   
    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).  
    # If this happens try again!
    desired_temp = int(read_desired_temperature_from_file())
    if last_desired_temperature_reading != desired_temp:
        dtemp = "R:" + str(desired_temp) + ":"
        last_desired_temperature_reading = desired_temp
    else:
        dtemp = "R:" + "555" + ":"
        print 'Desired Temperature = ' + dtemp
        
# TO DO - Put the reading of the temperature in to its own task (separate file)
#         Read the measured temperature from a file.
    #humidity, temperature = Adafruit_DHT.read_retry(22, 4)
    humidity, temperature = Adafruit_DHT.read(22, 4)

    if humidity is not None and temperature is not None:
        rtemp = "M:" + "%.3f" % temperature
        write_temp_to_led(temperature)
    else:
        print "Failed to read temperature"
        rtemp = "M:" + "555"

    time.sleep(2)

    print 'Temperature = ' + rtemp

    temp = dtemp + rtemp
    
    print temp
    
    try :
        #Connect to remote server
        s.sendall(temp)
    except socket.error:
        #Send failed
        print 'Send failed'
    s.close()


        

# Suspect repeated allocation of socket may be chewing up memory so garbage collect
    if gc_count > 5:
        gc_count = 0
        gc.collect()
    else:
        gc_count += 1
    time.sleep(2)
