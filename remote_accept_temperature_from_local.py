# This is for the REMOTE PI
# Accept and parse a message from the local pi.
# This message contains the local Pi's desired temperature
# as read from the remote control. 

import socket
import sys
 
HOST = '192.168.1.161'
PORT = 5000 # Arbitrary non-privileged port
  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
   
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
                    
print 'Socket bind complete'
            
s.listen(10)
print 'Socket now listening'
                      
#now keep talking with the client
while 1:
#wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
                                           
    temp_str = conn.recv(1024)
    data = temp_str.split(':')
    
    if data[0] is 'R':
        # print 'Remote Required temperature: ' + data[1]
        #update the required temp file
        print "desired temp = " + data[1]
        if int (data[1]) != 555:
            try:
                f = open ('./desired_temperature.txt','wt')
                f.write (data[1])
                f.close ()
            except IOError:
                print ("Cant open file temperature.txt for writing")
                my_logger.exception("Cant open file temperature.txt for writimg")
    else:
        print ("Recived bad message from remote sensor " + temp_str)
        #my_logger.exception("Received bad message from remote sensor" + temp_str)
    if not data: 
        print 'no data' 
                                         
#    conn.sendall(reply)
                                                       
conn.close()
s.close()
