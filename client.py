import socket
import threading
import time


global tLock
tLock = threading.Lock()
global shutdown
shutdown = False


def receving(name, sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(3000)
                append_message(data)
        except:
            pass
        finally:
            tLock.release()


def append_message(message):
    print message


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    local_ip_address = s.getsockname()[0]
    s.close()
    return local_ip_address


host = get_ip()
port = 0

server_ip = raw_input('Server IP: ')
server_port = int(raw_input('Port: '))
server = (server_ip, server_port)

# create udp socket instance
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.daemon = True
rT.start()
# register to chat
name = raw_input('Avatar Name: ')
s.sendto('--reg--' + name, server)
message = ''
while message != 'q':
    # tLock.acquire()
    message = raw_input('')
    # tLock.release()
    s.sendto(message, server)
    time.sleep(0.2)

shutdown = True
s.close()
