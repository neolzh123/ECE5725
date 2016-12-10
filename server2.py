'''
    Simple socket server using threads
'''
 
import socket
import sys
import os
import threading
import time
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'


try:
    #now keep talking with the client
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        data = conn.recv(1024).strip()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        print data
        if data == "time" :
            print "trigger time function"
            os.system("sudo python time_display5.py")
            
        elif data == "weather":
            print "trigger weather function"
            os.system("sudo python weather_report5.py")

        elif data == "calendar":
            print "trigger calendar function"
            os.system("sudo python quickstart5.py")

        elif data == "music":
            print "trigger music function"
            os.system("python MusicPlayer.py")

        elif data == "gesture":
            print "trigger gesture function"
            os.system("python hand_recognize.py --bounding-box 10,350,225,590")
            
except KeyboardInterrupt:
    s.close()
    sys.exit()
