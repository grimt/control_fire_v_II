import socket
import sys
 
HOST = '192.168.1.151'   # Symbolic name meaning all available interfaces
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
    print data[0]
    print data[1]
    print data[2]
    print data[3]
    
    if data[0] is 'R':
        print 'Remote Required temperature: ' + data[1]
        #update the required temp file
        try:
            f = open ('/tmp/temperature.txt','wt')
            f.write (data[1])
            f.close ()
        except IOError:
            if my_fire.debug_level >=2:
                print ("Cant open file temperature.txt for writing")
            my_logger.exception("Cant open file temperature.txt for writimg")
    elif data[0] is 'M':
        print 'Remote Measured temperature: ' + data[1]
        #update the measured temperature file
        try:
            f = open ('./remote_measured_temp.txt','wt')
            f.write (data[1])
            f.close ()
        except IOError:
            if my_fire.debug_level >=2:
                print ("Cant open file remote_measured_temp.txt for writing")
            #my_logger.exception("Cant open file remote_measured_temp.txt for writing")
    else:
        print ("Recived bad message from remote sensor " + temp_str)
        #my_logger.exception("Recived bad message from remote sensor" + temp_str)
    # Next write temperature to a file.
    if not data: 
        print 'no data' 
                                         
#    conn.sendall(reply)
                                                       
conn.close()
s.close()
