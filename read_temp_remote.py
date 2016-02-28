
# Note this file is for thr pi II

import sys
import Adafruit_DHT
import time
import socket   #for sockets

import gc


print 'Socket Created'

port = 5000;


remote_ip = '192.168.1.151'

gc_count = 0

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
        temp = "%.9f" % temperature
        print 'Temperature = ' + temp
        try :

            #Connect to remote server
            s.sendall(temp)
        except socket.error:
            #Send failed
            print 'Send failed'
    else:
        print 'Failed to get reading. Try again!'
    s.close()
# Suspect repeated allocation of socket may be chewing up memory so garbace collect
    if gc_count > 5:
        gc_count = 0
        gc.collect()
    else:
        gc_count += 1
    time.sleep(2)
