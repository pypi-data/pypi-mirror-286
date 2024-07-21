import socket
import sys
from concurrent.futures import ThreadPoolExecutor
from atexit import register as _register
from ssl import wrap_socket as ssl_socket

# Conn object
class Conn:
    def __init__(self, conn, client, msg):
        self.msg = msg
        self.client = client
        self.conn = conn

class Server:
    def __init__(self, max_workers=10):
        self.udp = False
        self.listen_dict = {}
        self.multi_route = False
        self.buffer_size = 1024
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def _create_server(self, address, port, udp=False, keyfile=None, certfile=None):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM if udp else socket.SOCK_STREAM)
        self.server.bind((address, port))
        if not udp:
            self.server.listen(5)

        # SSL
        if keyfile and certfile:
            self.server = ssl_socket(self.server, keyfile=keyfile, certfile=certfile, server_side=True)

    def udp_listen(self, *args):
        self.udp = True
        def wrapper(func):
            def f(data):
                function_return = func(data)
                if function_return:
                    self.server.sendto(function_return.encode(), data.client)
            if args:
                self.listen_dict[args[0]] = f
            else:
                self.default_route = f
            return f
        return wrapper

    def tcp_listen(self, *args):
        self.udp = False
        def wrapper(func):
            def f(data):
                function_return = func(data)
                if function_return:
                    data.conn.sendall(function_return.encode())
            if args:
                self.listen_dict[args[0]] = f
            else:
                self.default_route = f
            return f
        return wrapper

    def listen(self):
        while True:
            try:
                if self.udp:
                    msg, client = self.server.recvfrom(self.buffer_size)
                    msg = msg.decode()
                    data = Conn(None, client, msg)
                else:
                    conn, client = self.server.accept()
                    msg = conn.recv(self.buffer_size).decode()
                    data = Conn(conn, client, msg)

                if self.multi_route:
                    parsed = self.parse_function(data)
                    if parsed in self.listen_dict:
                        self.executor.submit(self.listen_dict[parsed], data)
                    else:
                        self.executor.submit(self.default_route, data)
                else:
                    self.executor.submit(self.default_route, data)

            except KeyboardInterrupt:
                self.cleanup()
            except Exception as e:
                print(f"Error: {e}")

    def parse_route(self, func):
        self.parse_function = func
        self.multi_route = True
        return func

    def send(self, data, msg):
        try:
            if self.udp:
                self.server.sendto(msg.encode(), data.client)
            else:
                data.conn.sendall(msg.encode())
        except KeyboardInterrupt:
            self.server.close()
            sys.exit()
        except Exception as e:
            print(f"Error: {e}")

    def close(self):
        if self.server:
            self.server.close()

    def cleanup(self):
        self.server.close()
        self.executor.shutdown(wait=False)
        sys.exit()

    def run(self, address, port, certfile=None, keyfile=None, timeout=0, buffer_size=1024):
        _register(self.close)
        self.buffer_size = buffer_size
        self._create_server(address, port, udp=self.udp, certfile=certfile, keyfile=keyfile)
        if timeout:
            self.server.settimeout(timeout)
        self.listen()

class Client:
    def __init__(self):
        self.client = None
        self.udp = False
        self.addr = None

    def connect(self, address, port, udp=False, timeout=0, tls=False):
        self.udp = udp
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM if udp else socket.SOCK_STREAM)

        # SSL
        if tls:
            from ssl import CERT_NONE, PROTOCOL_TLS
            self.client = ssl_socket(self.client, cert_reqs=CERT_NONE, ssl_version=PROTOCOL_TLS)

        if timeout:
            self.client.settimeout(timeout)
        if udp:
            self.addr = (address, port)
        else:
            try:
                self.client.connect((address, port))
            except Exception as e:
                print(f"{e}")

    def send(self, data):
        try:
            if self.udp:
                self.client.sendto(data.encode(), self.addr)
            else:
                self.client.sendall(data.encode())
        except Exception as e:
            print(f"{e}")

    def recv(self):
        try:
            if self.udp:
                msg, addr = self.client.recvfrom(1024)
                return msg.decode(), addr
            else:
                return self.client.recv(1024).decode()
        except Exception as e:
            print(f"{e}")

    def close(self):
        if self.client:
            self.client.close()
