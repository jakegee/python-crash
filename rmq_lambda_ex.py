import json
from botocore.vendored import requests
from botocore.client import Config
import boto3
import sys
import os
import argparse
import json
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

RMQ = os.environ['RMQ_ADDRESS']
VHOST = (os.environ['RMQ_VHOST']).strip()
RMQ_USER = (os.environ['RMQ_USER']).strip()
RMQ_PWD = (os.environ['RMQ_PASSWORD']).strip()

# /api/queues/aom_qa
URL = 'http://{}:15672/api/queues/{}'.format(RMQ, VHOST)
logger.info('server: {}'.format(RMQ))
logger.info('url: {}'.format(URL))
logger.info('user: {}'.format(RMQ_USER))
logger.info('user: {}'.format(RMQ_PWD))

def lambda_handler(event, context):
    try:
        r = requests.get(URL, auth=(RMQ_USER, RMQ_PWD), timeout=1)
        logger.info('connected to'.format(URL))
    except requests.exceptions.RequestException as e:
        logger.error(e)
        sys.exit(1)
    # Converts returned json into dictionary.
    RESULTS = json.loads(r.text)
    
    client = boto3.client('cloudwatch')

    
    def push_metrics(metrics,
                     dimensions,
                     namespace='RabbitMQ'):

        response = client.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    'MetricName': 'messages',
                    'Dimensions': [
                        {
                            'Name': 'queue',
                            'Value': dimensions['queue']
                        },
                  sys.      {
                            'Name': 'node',
                            'Value': dimensions['node']
                        },
                        {
                            'Name': 'vhost',
                            'Value': dimensions['vhost']
                        },
                        {
                            'Name': 'type',
                            'Value': 'queue'
                        },
                        {
                            'Name': 'Application',
                            'Value': 'AOM'
                        },
                    ],
                    'Value': metrics['messages'],
                    'Unit': 'Count',
                },
                {
                    'MetricName': 'messages_ready',
                    'Dimensions': [
                        {
                            'Name': 'queue',
                            'Value': dimensions['queue']
                        },
                        {
                            'Name': 'node',
                            'Value': dimensions['node']
                        },
                        {
                            'Name': 'vhost',
                            'Value': dimensions['vhost']
                        },
                        {
                            'Name': 'type',
                            'Value': 'queue'
                        },
                        {
                            'Name': 'Application',
                            'Value': 'AOM'
                        },
                    ],
                    'Value': metrics['messages_ready'],
                    'Unit': 'Count',
                },
                {
                    'MetricName': 'messages_unacknowledged',
                    'Dimensions': [
                        {
                            'Name': 'queue',
                            'Value': dimensions['queue']
                        },
                        {
                            'Name': 'node',
                            'Value': dimensions['node']
                        },
                        {
                            'Name': 'vhost',
                            'Value': dimensions['vhost']
                        },
                        {
                            'Name': 'type',
                            'Value': 'queue'
                        },
                        {
                            'Name': 'Application',
                            'Value': 'AOM'
                        },
                    ],
                    'Value': metrics['messages_unacknowledged'],
                    'Unit': 'Count',
                },
                {
                    'MetricName': 'consumers',
                    'Dimensions': [
                        {
                            'Name': 'queue',
                            'Value': dimensions['queue']
                        },
                        {
                            'Name': 'node',
                            'Value': dimensions['node']
                        },
                        {
                            'Name': 'vhost',
                            'Value': dimensions['vhost']
                        },
                        {
                            'Name': 'type',
                            'Value': 'queue'
                        },
                        {
                            'Name': 'Application',
                            'Value': 'AOM'
                        },
                    ],
                    'Value': metrics['consumers'],
                    'Unit': 'Count',
                },
            ]
        )
    
    for queue in RESULTS:
        DIMENSiONS = {'queue': queue['name'],
                      'node': queue['node'],
                      'vhost': queue['vhost']}
    
        METRICS = {'messages': queue['messages'],
                   'messages_ready': queue['messages_ready'],
                   'messages_unacknowledged': queue['messages_unacknowledged'],
                   'consumers': queue['consumers']}
    
        push_metrics(metrics=METRICS, dimensions=DIMENSiONS)

    return {
        "statusCode": 200,
        "body": json.dumps('Done.')
    }