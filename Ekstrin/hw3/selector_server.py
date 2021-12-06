import socket
from select import select

mode = 'cpu_bound'  # cpu_bound or rps


def fact(n):
    a = 1
    for i in range(1, n + 1):
        a *= i
    return a


def get_server_socket():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 8090))
    server_sock.listen()

    return server_sock


to_monitor = []


def accept_connection(server_sock: socket.socket) -> None:
    client_socket, client_addr = server_sock.accept()
    print(
        f'Connection has been received from {client_addr[0]}:{client_addr[1]}')
    to_monitor.append(client_socket)


def send_information(client_sock: socket.socket) -> None:
    request = client_sock.recv(4096)
    # print(f'Received: {request}')

    if request:
        # print('Sending Ping to client...')
        if mode == 'cpu_bound':
            n = int.from_bytes(request, "big")
            factorial = fact(n)
            client_sock.send('Factorial has been calculated!'.encode())
            # client_sock.send(factorial.to_bytes(200, 'big'))
        elif mode == 'rps':
            client_sock.send('Pong'.encode())
    else:
        print('Client has gone. Closing client socket...')
        to_monitor.remove(client_sock)
        client_sock.close()


def event_loop():
    while True:
        # readable, writable, errors
        ready_to_read, _, _ = select(to_monitor, [], [])
        for sock in ready_to_read:
            if sock == server_socket:
                accept_connection(sock)
            else:
                send_information(sock)


if __name__ == '__main__':
    server_socket = get_server_socket()
    to_monitor.append(server_socket)
    event_loop()
