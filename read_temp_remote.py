
# Note this file is for the pi II

import sys
import Adafruit_DHT
import time
import socket   #for sockets

import gc

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


def read_desired_temperature_from_file():
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


def pin_18_callback(channel):
        print ('Pressed button 18')
	desired_temperature = read_desired_temperature_from_file()
	desired_temperature = desired_temperature + 1
	write_desired_temperature_to_file(desired_temperature)
	#Send temperature to remote pi

def pin_23_callback(channel):
        print ('pressed button 23')
	desired_temperature = read_desired_temperature_from_file()
	desired_temperature = desired_temperature - 1
	write_desired_temperature_to_file(desired_temperature)
        # send temperature to remote pi

GPIO.setup (18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect (18, GPIO.FALLING, callback=pin_18_callback, bouncetime=1000)


GPIO.setup (23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect (23, GPIO.FALLING, callback=pin_23_callback, bouncetime=1000)


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

    #humidity, temperature = Adafruit_DHT.read_retry(22, 4)
    humidity, temperature = Adafruit_DHT.read(22, 4)
   
   
    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).  
    # If this happens try again!
  
    if humidity is not None and temperature is not None:
        temp = "M:" + "%.3f" % temperature
        print 'Temperature = ' + temp
        try :

            #Connect to remote server
            s.sendall(temp)
        except socket.error:
            #Send failed
            print 'Send failed'
    else:
        print 'Failed to get reading. Try again!'

    desired_temp = int(read_desired_temperature_from_file())
    if last_desired_temperature_reading != desired_temp:
        temp = "R:" + str(desired_temp)

        print 'Desired Temperature = ' + temp
        try :

            #Connect to remote server
            s.sendall(temp)
        except socket.error:
            #Send failed
            print 'Send failed'
        last_desired_temperature_reading = desired_temp
    s.close()

# Suspect repeated allocation of socket may be chewing up memory so garbace collect
    if gc_count > 5:
        gc_count = 0
        gc.collect()
    else:
        gc_count += 1
    time.sleep(2)
