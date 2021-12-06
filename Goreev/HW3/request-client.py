import requests
import time

num_of_iter = 1000
time_start = time.time()
for i in range(num_of_iter):
    r = requests.get("http://127.0.0.1:5000/fib")
time_stop = time.time()
exec_time = time_stop-time_start
print(num_of_iter/exec_time)
