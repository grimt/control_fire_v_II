# This is for the LOCAL PI
# Accept and parse a message from the remote pi.
# This message contains the remote Pi's desired temperature
# as read from the push buttons and the measured temperature
# For both measured and desired, a temperature of 555 means ignore.

import socket
import sys

import logging
import logging.handlers
 
HOST = '192.168.1.151'   # Symbolic name meaning all available interfaces
PORT = 5000 # Arbitrary non-privileged port
 
 
def init_logging():
    LOG_FILENAME = '/var/log/local_accept_temp.log'
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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print 'Socket created'
   
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    my_logger.debug('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
                    
my_logger.debug ('Socket bind complete')
            
s.listen(10)
# print 'Socket now listening'
                      
#now keep talking with the client
while 1:
#wait to accept a connection - blocking call
    conn, addr = s.accept()
    # print 'Connected with ' + addr[0] + ':' + str(addr[1])
                                           
    temp_str = conn.recv(1024)
    data = temp_str.split(':')
    
    if data[0] is 'R':
        my_logger.debug ('Remote Required temperature: ' + data[1])
        #update the required temp file
        if int (data[1]) != 555:
            try:
                f = open ('/tmp/desired_temperature.txt','wt')
                f.write (data[1])
                f.close ()
            except IOError:
                print ("Cant open file temperature.txt for writing")
                my_logger.exception("Cant open file temperature.txt for writimg")
    if data[2] is 'M':
        my_logger.debug ('Remote Measured temperature: ' + data[3])
        #update the measured temperature file
        if float (data[3]) != 555.0:
            try:
                f = open ('./remote_measured_temp.txt','wt')
                f.write (data[3])
                f.close ()
            except IOError:
                my_logger.exception("Cant open file remote_measured_temp.txt for writing")
    else:
        my_logger.debug ("Recived bad message from remote sensor " + temp_str)
    if not data: 
        my_logger.debug ('no data') 
conn.close()
s.close()
