# This is for the remote pi
# Process button press interrupts which
# allow the user to set a desired temperature.

import RPi.GPIO as GPIO


def read_desired_temperature_from_file():
    temp = '555'
    try:
        f = open ('./desired_temperature.txt','rt')
        temp = f.read ()
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

