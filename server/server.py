# import socket module
import select
import socket
import sys
import threading
import os.path

class MyHTTPServer():
    def __init__(self):
        self.host = 'localhost'
        self.port = 5000
        self.backlog = 5
        self.size = 1024
        self.server_socket = None
        self.threads = []

    def open_socket(self):
        # creating socket server object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind socket server to defined server address and port in tuple
        self.server_socket.bind((self.host, self.port))

        # listening connection from client, only 1 backlog
        self.server_socket.listen(5)

    def run(self):
        self.open_socket()
        input_socket = [self.server_socket]
        # infinite loop for receiving message from client
        running = 1
        while running:
            read_ready, write_ready, exception = select.select(input_socket, [], [])
            for sock in read_ready:
                if sock == self.server_socket:
                    # handle the server socket
                    client_socket, client_address = self.server_socket.accept()
                    klien = Handle_Client((client_socket, client_address))
                    klien.start()
                    self.threads.append(klien)

                elif sock == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0
                    print 'close'

        # close all threads
        self.server_socket.close()
        for klien in self.threads:
            klien.join()

class Handle_Client(threading.Thread):
    def __init__(self, (client, address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        while True:
            # receive message from client, 1024 is buffer size in bytes
            data = self.client.recv(self.size)
            print 'recv: ', self.address
            if data:
                command = data.split()
            link = command[1]
            command = command[0]
            cek = handle_file(link[1:])
            body = cek.cek_file()
            print command
            print link

            if (command == 'GET'):
                self.handle_get(body)

            elif (command == 'HEAD'):
                self.handle_head(body)

            elif (command == 'POST'):
                self.handle_post(body)

            else:
                self.handle_error(body)

            # close client socket
            self.client.close()
            break

    def handle_get(self, body):
        if body == 'Error 404':
            response = 'HTTP/1.1 404 Not Found\r\n\r\n'
            self.client.send(response)
            self.client.send(body)
        elif body == 'Error 403':
            response = 'HTTP/1.1 403 Forbidden\r\n\r\n'
            self.client.send(response)
            self.client.send(body)
        elif 'HTTP/1.1 301 Moved Permanently' in body:
            self.client.send(body)
        else:
            response = 'HTTP/1.1 200 OK\r\n\r\n'
            self.client.send(response)
            self.client.send(body)
            print 'GET'

    def handle_head(self, body):
        if body == 'Error 404':
           response = 'HTTP/1.1 404 Not Found\r\n\r\n'
           self.client.send(response)
        elif body == 'Error 403':
            response = 'HTTP/1.1 403 Forbidden\r\n\r\n'
            self.client.send(response)
        elif 'HTTP/1.1 301 Moved Permanently' in body:
            self.client.send(body.split('\r\n\r\n')[0])
        else:
            response = 'HTTP/1.1 200 OK\r\n\r\n'
            self.client.send(response)
            print 'HEAD'

    def handle_post(self, body):
        if body == 'Error 404':
            response = 'HTTP/1.1 404 Not Found\r\n\r\n'
            self.client.send(response)
        elif body =='Error 403':
            response = 'HTTP/1.1 403 Forbidden\r\n\r\n'
            self.client.send(response)
        elif 'HTTP/1.1 301 Moved Permanently' in body:
            self.client.send(body)
        else:
            response = 'HTTP/1.1 200 OK\r\n\r\n'
            self.client.send(response)
            print 'POST'

    def handle_error(self, body):
        response = 'HTTP/1.1 500 Internal Server Error\r\n\r\n'
        body = 'Internal Server Error'
        self.client.send(response)
        self.client.send(body)

class handle_file():
    def __init__(self, path):
        self.path = path

    def cek_file(self):
        path = self.path.split('/')
        path = '/'.join(path)
        if path is not '':
            if path[-1] is not '/':
                path += '/'
        if os.path.isfile(path+'redir.mmm'):
            faile = open(path+'redir.mmm', 'rb')
            redir = faile.read()
            path += redir
        if os.path.isfile(path+'denied.mmm'):
            return 'Error 403'
        elif os.path.isfile(path+'moved.mmm'):
            if'.' not in self.path:
                self.path += 'index.html'
            if os.path.isfile(self.path):
                kirim = 'HTTP/1.1 301 Moved Permanently\r\n'
                faile = open(path+'moved.mmm', 'rb')
                kirim += faile.read()
                faile.close()
                kirim += '\r\n\r\n'
                faile = open(self.path,'rb')
                kirim += faile.read()
                faile.close()
                return kirim
        else:
            if '.' not in self.path:
                self.path += 'index.html'
            if os.path.isfile(self.path):
                faile = open(self.path, 'rb')
                kirim = faile.read()
                faile.close()
                return kirim
            else:
                return 'Error 404'


if __name__ == "__main__":
    s = MyHTTPServer()
    s.run()

