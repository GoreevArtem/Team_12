import socket
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 8090

client_socket = socket.socket()
client_socket.connect((SERVER_HOST, SERVER_PORT))

num_operations = 10000
begin = time.time()
f = 1000
for i in range(num_operations):
    # print('Sending Ping...')
    client_socket.send(f.to_bytes(4, 'big'))
    # print('Receiving response...')
    response = client_socket.recv(100)
end = time.time()
print(f'{num_operations / (end - begin)} requests per second')

print('Closing connection...')
client_socket.close()
