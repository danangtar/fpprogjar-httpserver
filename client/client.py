# import socket module
import socket
import sys

class MyHTTPClient():
    def __init__(self):
        # creating socket client
        self.client_socket = []
        self.response = ''
        self.request = ''
        self.host = ''
        self.host = 80

    def input_request(self, inputan):
        # request
        inputan = inputan.split()
        link = "%20".join(inputan[1:])
        link = link.split('/')
        host = link[0]
        if(':' in host):
            host = host.split(':')
            port = int(host[1])
            host = host[0]
        else:
            port = 80
        link = "/".join(link[1:])
        link = "/" + link

        method = inputan[0]

        request = method
        request += ' ' + link + ' HTTP/1.1\r\nHost: '
        request += host + ':' + str(port) + '\r\n\r\n'
        self.request = request
        self.host = host
        self.port = port

    def connect(self):
        # connect to server in defined address and port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_request(self):
        # send message to server
        self.client_socket.send(self.request)

        response = self.client_socket.recv(1024)
        while (response):
            temp = self.client_socket.recv(1024)
            if (temp == ''):
                break
            response += temp

        self.response = response

    def print_response(self):
        return self.response

    def exit(self):
        self.client_socket.close()

client = MyHTTPClient()

try:
    while True:
        inputan = raw_input()

        client.input_request(inputan)
        client.connect()
        client.send_request()
        print client.print_response()
        client.exit()

except KeyboardInterrupt:
    client.exit()
    sys.exit(0)
