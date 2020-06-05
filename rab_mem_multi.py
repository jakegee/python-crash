import requests
from requests.auth import HTTPBasicAuth

r1 = requests.get('http://10.22.2.99:15672/api/nodes/rabbit@ip-10-22-10-99', auth=HTTPBasicAuth('monitor', 'monitor'))
r2 = requests.get('http://10.22.2.99:15672/api/nodes/rabbit@ip-10-22-2-99', auth=HTTPBasicAuth('monitor', 'monitor'))
r3 = requests.get('http://10.22.2.99:15672/api/nodes/rabbit@ip-10-22-6-99', auth=HTTPBasicAuth('monitor', 'monitor'))

d1 = r1.json()
d2 = r2.json()
d3 = r3.json()

print(d1['mem_used'])
print(d2['mem_used'])
print(d3['mem_used'])