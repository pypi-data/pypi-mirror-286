# simple-sock

`simple-sock` offers a straightforward interface for TCP and UDP sockets in Python, with support for optional SSL/TLS encryption and routing for TCP connections.

## Basic Usage

### Basic TCP Server

```python
from simple_sock import Server

app = Server()

@app.tcp_listen()
def handle_tcp(data):
    print("Received:", data.msg)
    return "Response from TCP server"

app.run("localhost", 5454)  # Optional parameters: keyfile=None, certfile=None, timeout=0, buffer_size=1024
```

### TCP Server with Routing

```python
from simple_sock import Server

app = Server()

@app.parse_route
def parse_route(data):
    return data.msg.split()[0]

@app.tcp_listen()
def default_route(data):
    return "Default response"

@app.tcp_listen("route1")
def route1(data):
    return "Response for route1"

app.run("localhost", 5454)
```

### Basic TCP Client

```python
from simple_sock import Client

client = Client()
client.connect("localhost", 5454)  # Optional parameters: udp=False, tls=False
client.send("Hello from TCP client")
response = client.recv()
print(response)
client.close()
```

### UDP Support

UDP usage is similar; use `@app.udp_listen()` for servers and set `udp=True` for clients. Example:

```python
# UDP Server
app = Server(udp=True)
@app.udp_listen()
def handle_udp(data):
    print("Received:", data.msg)
    return "Response from UDP server"
app.run("localhost", 5455")

# UDP Client
client.connect("localhost", 5455, udp=True)
client.send("Hello from UDP client")
response, _ = client.recv()
print(response)
client.close()
```

## License

MIT License

## Contact

For questions, contact Leonardo Oliveira at [email](mailto:lo570354@gmail.com).