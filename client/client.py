# import socket module
import socket
import sys

response = ''
request = ''

try:
    while True:
        # creating socket client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to server in defined address and port
        client_socket.connect(('localhost', 5000))

        # send message to server
        #client_socket.send("Hi server ... ")
        inputan = raw_input()
        inputan = inputan.split()
        link = " ".join(inputan[1:])
        method = inputan[0]

        request = method
        request += ' / HTTP/1.1\r\nHost: '
        request += link + '\r\n\r\n'
        print request
        client_socket.send(request)

        response = client_socket.recv(1024)
        while (response):
            temp = client_socket.recv(1024)
            if (temp == ''):
                break
            response += temp

        print response

        client_socket.close()


except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)