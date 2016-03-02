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
    if data[0] is 'R':
        print 'Remote Required temperature: ' + data[1]
        #update the required temp file
        try:
            f = open ('/tmp/temperature.txt','wt')
            f.write (data[1])
            f.close ()
        except IOError:
            if my_fire.debug_level >=2:
                print ("Cant open file temperature.txt for reading")
            my_logger.exception("Cant open file temperature.txt for reading")
    elif data[0] is 'M':
        print 'Remote Measured temperature: ' + data[1]
        #update the measured temperature file

    # Next write temperature to a file.
    if not data: 
        print 'no data' 
                                         
#    conn.sendall(reply)
                                                       
conn.close()
s.close()
