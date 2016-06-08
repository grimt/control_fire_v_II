# This is for the REMOTE PI
# Accept and parse a message from the local pi.
# This message contains the local Pi's desired temperature
# as read from the remote control. 

import socket
import sys

import logging
import logging.handlers
from Adafruit_7Segment import SevenSegment
from Adafruit_LEDBackpack import LEDBackpack

def init_logging():
    LOG_FILENAME = '/var/log/remote_accept_temperature.log'
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

def write_temp_to_7segment (temp):
  segment = SevenSegment(address=0x71) 
  hundreds = int (temp / 100)
  if (hundreds > 0):
      segment.writeDigit(1, hundreds)            # Hundreds
  temp = temp - (hundreds * 100)
  segment.writeDigit(3, int(temp / 10))      # tens
  segment.writeDigit(4, int(temp % 10))      # ones


my_logger = init_logging()

#setup i2c
segment = SevenSegment(address=0x71)
led = LEDBackpack(0x71)

HOST = '192.168.1.161'
PORT = 5000 # Arbitrary non-privileged port
  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print 'Socket created'
   
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    my_logger.exception ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
                    
my_logger.debug ('Socket bind complete')
            
s.listen(10)
                      
#now keep talking with the client
while 1:
#wait to accept a connection - blocking call
    conn, addr = s.accept()
    
    temp_str = conn.recv(1024)
    data = temp_str.split(':')

    try:    
        if data[0] is 'R':
            # print 'Remote Required temperature: ' + data[1]
            #update the required temp file
            my_logger.debug ("desired temp = " + data[1])
        
            if int (data[1]) != 555:
                try:
                    f = open ('./desired_temperature.txt','wt')
                    f.write (data[1])
                    write_temp_to_7segment (int(data[1]))
                    f.close ()
                except IOError:
                    my_logger.exception("Cant open file temperature.txt for writimg")
        else:
            my_logger.info  ("Recived bad message from remote sensor " + temp_str)
    except:
        my_logger.info ("Bad data: " + temp_str)

    if not data: 
        my_logger.info  ('no data') 
                                                       
conn.close()
s.close()
