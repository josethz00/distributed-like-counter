import socket

class RedisProxyClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # initial socket handshake
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_command(self, command):
        try:
            # we need to reassign the socket because it's closed after each command
            # otherwise, if we try to reuse the same socket, we get a "Error: [Errno 9] Bad file descriptor"
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.socket.sendall(command.encode('utf-8'))
            response = self.socket.recv(1024)
            return response.decode('utf-8')
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.close()

    def close(self):
        self.socket.close()
