# import socket module
import socket
import select
import sys

# creating socket server object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind socket server to defined server address and port in tuple
server_socket.bind(('localhost', 5000))

# listening connection from client, only 1 backlog
server_socket.listen(5)

input_socket = [server_socket]

response = ''
command = ''

# infinite loop for receiving message from client
try:
    while (True):
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                # receiving client socket
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)

            else:
                # receive message from client, 1024 is buffer size in bytes
                inputan = sock.recv(1024)
                print inputan
                if (inputan):
                    command = inputan.split()[0]
                if (command):
                    print command
                link = " ".join(command[1:])

                if (command == 'GET'):
                    response = 'HTTP/1.1 200 OK\r\n\r\nHello, World!'
                    sock.send(response)
                    print 'GET'

                elif (command == 'HEAD'):
                    response = 'HTTP/1.1 200 OK\r\n\r\nHello, World!'
                    sock.send(response)
                    print 'HEAD'

                elif (command == 'POST'):
                    response = 'HTTP/1.1 200 OK\r\n\r\nHello, World!'
                    sock.send(response)
                    print 'POST'

                else:
                    response = 'HTTP/1.1 500 Internal Server Error\r\n\r\nInternal Server Error'
                    sock.send(response)

                # close client socket
                sock.close()
                input_socket.remove(sock)

# when user press CTRL + C (in Linux), close socket server and exit
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
