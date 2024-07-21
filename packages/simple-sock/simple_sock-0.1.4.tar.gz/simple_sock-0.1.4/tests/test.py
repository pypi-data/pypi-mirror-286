import unittest
import threading
from simple_sock import Server, Client

class TestServerClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tcp_server = Server()
        @cls.tcp_server.tcp_listen()
        def handle_tcp(data):
            return "Hello from TCP server"
        cls.tcp_server_thread = threading.Thread(target=cls.tcp_server.run, args=("localhost", 5454))
        cls.tcp_server_thread.start()

        cls.udp_server = Server(udp=True)
        @cls.udp_server.udp_listen()
        def handle_udp(data):
            return "Hello from UDP server"
        cls.udp_server_thread = threading.Thread(target=cls.udp_server.run, args=("localhost", 5455))
        cls.udp_server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.tcp_server.close()
        cls.udp_server.close()
        cls.tcp_server_thread.join()
        cls.udp_server_thread.join()

    def test_tcp_client(self):
        client = Client()
        client.connect("localhost", 5454, udp=False)
        client.send("Hello from TCP client")
        response = client.recv()
        client.close()
        self.assertEqual(response, "Hello from TCP server")

    def test_udp_client(self):
        client = Client()
        client.connect("localhost", 5455, udp=True)
        client.send("Hello from UDP client")
        response, _ = client.recv()
        client.close()
        self.assertEqual(response, "Hello from UDP server")

if __name__ == "__main__":
    unittest.main()
