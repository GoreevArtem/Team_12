import socket

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


server_socket = get_server_socket()

while True:
    print('Waiting new connection...')
    client_socket, client_addr = server_socket.accept()
    print(
        f'Connection has been received from {client_addr[0]}:{client_addr[1]}')

    while True:
        request = client_socket.recv(4096)
        # print(f'Received: {request}')

        if request:
            # print('Sending Ping to client...')
            if mode == 'cpu_bound':
                n = int.from_bytes(request, "big")
                factorial = fact(n)
                client_socket.send('Factorial has been calculated!'.encode())
            elif mode == 'rps':
                client_socket.send('Pong'.encode())
        else:
            print('Client has gone. Closing client socket...')
            client_socket.close()
            break
