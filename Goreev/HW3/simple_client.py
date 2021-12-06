import socket
import time
import simple_operations

SERVER_HOST = 'localhost'
SERVER_PORT = 8090

client_socket = socket.socket()
client_socket.connect((SERVER_HOST, SERVER_PORT))

num_of_iter = 1000
time_start = time.time()
for i in range(num_of_iter):
    client_socket.send(str(simple_operations.fib(5)).encode())
    client_socket.recv(4096)

time_stop = time.time()
exec_time = time_stop-time_start
print(num_of_iter/exec_time)

print("Closing connection...")
client_socket.close()
