import socket


def main():
    host = get_ip()
    port = 5000

    # create udp socket instance
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    s.setblocking(True)
    print "Lintening to {}:{}".format(host, port)

    users = {}
    while True:
        data, addr = s.recvfrom(3000)
        data = str(data)

        # register new user
        if data.startswith('--reg--'):
            name = data.replace('--reg--', '')
            send_message_to_clients(name + ' joined the chat', users, s)
            users[str(addr)] = [name, addr]
            print "User registered: {}".format(name)
            continue

        # send received message to all clients
        sender = users[str(addr)][0]
        message = '{}: {}'.format(sender, data)
        send_message_to_clients(message, users, s, exclude=[str(addr)])

    s.close()


def send_message_to_clients(message, client, socket, exclude=[]):
    for address in client:
        if address in exclude:
            continue
        receiver_address = client[address][1]
        print "sending to {}".format(receiver_address)
        socket.sendto(message, receiver_address)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    local_ip_address = s.getsockname()[0]
    s.close()
    return local_ip_address


if __name__ == '__main__':
    main()