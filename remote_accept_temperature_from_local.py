# This is for the REMOTE PI
# Accept and parse a message from the local pi.
# This message contains the local Pi's desired temperature
# as read from the remote control. 

import socket
import sys

import logging
import logging.handlers

def init_logging():
    LOG_FILENAME = '/var/log/remote_accept_temperature.log'
    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s  %(message)s')
 
    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler( LOG_FILENAME, maxBytes=20000, backupCount=5)  
    handler.setFormatter(formatter)

    my_logger.addHandler(handler)

    my_logger.debug ('Start logging')
  
    return my_logger


my_logger = init_logging()

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
    
    if data[0] is 'R':
        # print 'Remote Required temperature: ' + data[1]
        #update the required temp file
        my_logger.debug ("desired temp = " + data[1])
        
        if int (data[1]) != 555:
            try:
                f = open ('./desired_temperature.txt','wt')
                f.write (data[1])
                f.close ()
            except IOError:
                my_logger.exception("Cant open file temperature.txt for writimg")
    else:
        my_logger.debug  ("Recived bad message from remote sensor " + temp_str)
        #my_logger.exception("Received bad message from remote sensor" + temp_str)
    if not data: 
        my_logger.debug  ('no data') 
                                                       
conn.close()
s.close()
