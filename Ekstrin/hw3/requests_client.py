import time

import requests

begin = time.time()
num_operations = 100
f = 1000
for i in range(num_operations):
    # r = requests.get('http://127.0.0.1:5000/')
    r = requests.get('http://127.0.0.1:5000/factorial', params={'n': f})
end = time.time()
print(f'{num_operations / (end - begin)} requests per second')
