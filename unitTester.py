import requests
import time 

url  = 'http://127.0.0.1:5500/addUser'

n_requests = 300

for i in range(n_requests):
    res = requests.post(url)
    print(f"Request: {i+1}: Status Code - {res.status_code}")
    