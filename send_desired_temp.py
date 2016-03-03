# Note this file is for the pi II
# Manually simulate the remote pi sending a desired temperature.
# This tests control fire until the hardware arrives

import sys
import Adafruit_DHT
import time
import socket   #for sockets

import gc


print 'Socket Created'

port = 5000;


remote_ip = '192.168.1.151'

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
temp = "R:" + sys.argv[1] 
print 'Temperature = ' + temp
try :
    #Connect to remote server
    s.sendall(temp)
except socket.error:
    #Send failed
    print 'Send failed'
s.close()
