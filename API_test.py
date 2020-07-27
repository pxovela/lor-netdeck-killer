import os
import requests

os.environ['NO_PROXY'] = '127.0.0.1'
r = requests.get('http://127.0.0.1:21337')
print(r.content)
print(r)