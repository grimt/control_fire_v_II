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
    if data[0] = 'R':
        print 'Remote Reaquired temperature: ' + data[1]
    else if data[0]= 'M':

        print 'Remote Measured temperature: ' + data[1]

    # Next write temperature to a file.
    if not data: 
        print 'no data' 
                                         
#    conn.sendall(reply)
                                                       
conn.close()
s.close()
