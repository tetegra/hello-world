from socket import *
from sys import argv
import sys
import time



def send(socket,msg):
    print "===>sending: " + msg
    socket.send(msg + "\r\n")
    recv = socket.recv(1024)
    print "<===receive: " + recv
    return recv

def ls(sockets, dataSocket):
    print "list of all file in current dicrectory:"
    sockets.send('NLST\r\n')
    recv = sockets.recv(1024)
    print '<====receive from control socket: '+recv
    recv = sockets.recv(1024)
    print '<====receive from control socket: '+recv
    dataSocket, addr = localSocket.accept()
    message = dataSocket.recv(1024)
    print '<===receive from data socket\n' + message
    message = dataSocket.recv(1024)

def get(sockets,localSocket,fileName):
    print '===>getting files %s'% fileName
    sockets.send('RETR %s\r\n' % fileName )
    recv = sockets.recv(1024)
    print '<===receive: ' + recv
    dataSocket, addr = localSocket.accept()
    message = dataSocket.recv(2048)
    fileOut = open(fileName,'wb')
    fileOut.write(message)
    fileOut.close()
    sockets.recv(1024)
    print str(len(open(fileName,'rb').read())) + ' bytes transfered'

def put(sockets, localSocket,fileName):
    file = open(fileName,'rb')
    print '===>uploading file ', fileName
    sockets.send('STOR %s\r\n' % fileName)
    recv = sockets.recv(1024)
    print '<===receive from control port '+recv
    dataSocket, addr = localSocket.accept()
    print '<===sending data to data port'
    dataSocket.send(file.read())
    print 'before dataSocket.recv(2048)'
    message = sockets.recv(1024)
    print message
    print str(len(open(fileName,'rb').read())) + ' bytes transfered'

def delete(sockets, fileName):
    print '===>deleting file ', fileName
    sockets.send('DELE %s\r\n' % fileName)
    recv = sockets.recv(1024)
    print '<===receive ' + recv

def quit(sockets):
    print '===>quiting ftp serve '
    sockets.send('QUIT\r\n')
    recv = sockets.recv(1024)
    print '<===receive ' + recv

if len(sys.argv) != 2:
    sys.exit('usage: myftp servername')
print 'program started'
serverName = sys.argv[1]
# Use port 21 for connection
serverPort = 21
controlSocket = socket(AF_INET, SOCK_STREAM)
controlSocket.connect((serverName, serverPort))
controlSocket.recv(1024)
user = raw_input('Please enter your user name> ')
message = send(controlSocket,"USER %s" % user)
password = raw_input('Please enter your passowrd> ')
message = send(controlSocket,"PASS %s" % password)
# Create data connection. Here we use port 12002
localSocket = socket(AF_INET, SOCK_STREAM)
localSocket.bind(('', 21003))
time.sleep(1)
localSocket.listen(1)

# prepare for the 'PORT' command info
localIp = gethostbyname(gethostname())
portModulo = 21003 % 256
portOcta = 21003/256
localInfo = str(localIp).replace('.',',')+','+str(portOcta)+','+str(portModulo)
while True:
    time.sleep(1)
    print 'Pleaee enter your command, type q to exit.\n'
    cmd = raw_input('> ')
    cmd_parse = cmd.split(' ')

    if cmd_parse[0] == 'ls':
        controlSocket.send('PORT %s\r\n' % localInfo)
        ls(controlSocket,localSocket)
    elif cmd_parse[0] == 'get':
        controlSocket.send('PORT %s\r\n' % localInfo)
        get(controlSocket,localSocket,cmd_parse[1])
    elif cmd_parse[0] == 'put':
        controlSocket.send('PORT %s\r\n' % localInfo)
        put(controlSocket,localSocket,cmd_parse[1])
    elif cmd_parse[0] == 'delete':
        controlSocket.send('PORT %s\r\n' % localInfo)
        delete(controlSocket,cmd_parse[1])
    elif cmd_parse[0] == 'quit':
        controlSocket.send('PORT %s\r\n' % localInfo)
        quit(controlSocket)
        break
    elif cmd_parse[0] == 'q':
        break
    else:
        print 'only accept ls, put, get, delete and quit command!'

localSocket.close()
