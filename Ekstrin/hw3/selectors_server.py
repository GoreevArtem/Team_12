import selectors
import socket

mode = 'cpu_bound'  # cpu_bound or rps
selector = selectors.DefaultSelector()


def fact(n):
    a = 1
    for i in range(1, n + 1):
        a *= i
    return a


def server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 8090))
    server_sock.listen()

    selector.register(
        fileobj=server_sock,
        events=selectors.EVENT_READ,
        data=accept_connection
    )


to_monitor = []


def accept_connection(server_sock: socket.socket) -> None:
    client_socket, client_addr = server_sock.accept()
    print(
        f'Connection has been received from {client_addr[0]}:{client_addr[1]}')
    selector.register(
        fileobj=client_socket,
        events=selectors.EVENT_READ,
        data=send_message
    )


def send_message(client_sock: socket.socket) -> None:
    request = client_sock.recv(4096)
    # print(f'Received: {request}')

    if request:
        # print('Sending Ping to client...')
        if mode == 'cpu_bound':
            n = int.from_bytes(request, "big")
            factorial = fact(n)
            client_sock.send('Factorial has been calculated!'.encode())
        elif mode == 'rps':
            client_sock.send('Pong'.encode())
    else:
        print('Client has gone. Closing client socket...')
        selector.unregister(client_sock)
        client_sock.close()


def event_loop():
    while True:
        events = selector.select()  # key, events (bit mask read or write)
        for key, _ in events:  # key has fileobj, events, data
            callback_function = key.data
            callback_function(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
