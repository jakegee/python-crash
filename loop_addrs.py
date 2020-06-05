import requests
import json
import sys
from requests.auth import HTTPBasicAuth

ip_base = '10.22.2.99:15672'
b_dict = {}
c_dict = {}
def lambda_handler():
    a_dict = {'a1': 'rabbit@ip-10-22-10-99', 'a2': 'rabbit@ip-10-22-2-99', 'a3': 'rabbit@ip-10-22-6-99'}
    for value in a_dict.values():
        response = requests.get('http://{}/api/nodes/{}'.format(ip_base, value), auth=HTTPBasicAuth('monitor', 'monitor'))
        results = response.json()
#        print(results.keys())
        b_dict[value] = results['mem_used']
        c_dict[value] = results['name']
    print(b_dict['rabbit@ip-10-22-10-99'])
    print(c_dict['rabbit@ip-10-22-10-99'])
    sys.exit(0)

lambda_handler()
