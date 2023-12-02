import socket

class RedisProxyClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send_command(self, command):
        self.socket.sendall(command.encode('utf-8'))
        response = self.socket.recv(1024)
        return response.decode('utf-8')

    def close(self):
        self.socket.close()
