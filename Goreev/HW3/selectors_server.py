import socket
import selectors
import simple_operations

selector = selectors.DefaultSelector()


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
    print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')
    selector.register(
        fileobj=client_socket,
        events=selectors.EVENT_READ,
        data=send_message
    )


def send_message(client_sock: socket.socket) -> None:
    request = client_sock.recv(4096)
    print(f'Received: {request}')

    if request:
        print('Sending message to client...')
        client_sock.send(str(simple_operations.fib(5)).encode())
    else:
        print('Client has gone. Closing client socket...')
        selector.unregister(client_sock)
        client_sock.close()


def event_loop():
    while True:
        events = selector.select()
        for key, _ in events:
            callback_func = key.data
            callback_func(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
