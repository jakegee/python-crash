import json
import os
import sys
import logging
import boto3
import requests
from requests.auth import HTTPBasicAuth
import botocore
from botocore.client import Config

# Capturing AWS environment variables, then stripping from code/logs
rmq_user = (os.environ['rmq_user']).strip()
rmq_passwd = (os.environ['rmq_passwd']).strip()
rmq_ip = (os.environ['rmq_ip']).strip()
rmq_port = (os.environ['rmq_port']).strip()
rmq_addr1 = (os.environ['rmq_addr1']).strip()
rmq_addr2 = (os.environ['rmq_addr2']).strip()
rmq_addr3 = (os.environ['rmq_addr3']).strip()

# Errors will be logged
logger = logging.getLogger()
logger.setLevel(logging.INFO)

b_dict = {}
c_dict = {}
def lambda_handler(event, context):
    a_dict = {'a1': rmq_addr1, 'a2': rmq_addr2, 'a3': rmq_addr3 }
    for address in a_dict.values():
        response = requests.get('http://{}:{}/api/nodes/{}'.format(rmq_ip, rmq_port, address), auth=HTTPBasicAuth(rmq_user, rmq_passwd))
        logger.info('successfully connected: {}'.format(address))
        results = response.json()
        b_dict[address] = results['mem_used']
        c_dict[address] = results['name']
    print(b_dict)
    print(c_dict)

    # Creates cloudwatch client    
    cloudwatch = boto3.client('cloudwatch')
	# Pushes custom metrics to cloudwatch
    cloudwatch.put_metric_data(
	    MetricData=[
		    {
		    	'MetricName': 'mem_used',
		    	'Dimensions': [
					{
						'Name': 'name',
						'Value': c_dict[rmq_addr1]
					},
					{
						'Name': 'Application',
                    	'Value': 'AOM'
                	},
            	],
            	'Unit': 'Bytes',
            	'Value': b_dict[rmq_addr1]
			},
			{
		    	'MetricName': 'mem_used',
		    	'Dimensions': [
					{
						'Name': 'name',
						'Value': c_dict[rmq_addr2]
					},
					{
						'Name': 'Application',
                    	'Value': 'AOM'
                	},
            	],
            	'Unit': 'Bytes',
            	'Value': b_dict[rmq_addr2]
			},
			{
		    	'MetricName': 'mem_used',
		    	'Dimensions': [
					{
						'Name': 'name',
						'Value': c_dict[rmq_addr3]
					},
					{
						'Name': 'Application',
                    	'Value': 'AOM'
                	},
            	],
            	'Unit': 'Bytes',
            	'Value': b_dict[rmq_addr3]
			},
		],
    	Namespace='RabbitMQ'
    )