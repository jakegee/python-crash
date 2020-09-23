import os
import boto3
import json
from botocore.exceptions import ClientError

topic = os.environ['topicarn']
message_dict = {}

def send_sns_alert(subject,message,topicarn=topic):
    # Construct json document before sending.
    try:
        print('Sending alert.')
        session = boto3.session.Session(region_name='eu-west-1')
        sns = session.client('sns')
        response = sns.publish(
            TopicArn=topicarn,
            Message=message,
            Subject=subject,
        )
        print(response)
    except ClientError as e:
        print(e)

def lambda_handler(event, context):
    event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:eu-west-1:803700595459:OpsGenieCoreHAProxyPipelineTopic:39c1da1a-3d23-4065-90b5-3a9536c8db1c', 'Sns': {'Type': 'Notification', 'MessageId': '703b2686-70d3-51fe-bd27-707a62649ec7', 'TopicArn': 'arn:aws:sns:eu-west-1:803700595459:OpsGenieCoreHAProxyPipelineTopic', 'Subject': None, 'Message': '{"version":"0","id":"dd93259d-579f-43c4-9cb2-6021293efce7","detail-type":"CodePipeline Pipeline Execution State Change","source":"aws.codepipeline","account":"803700595459","time":"2020-03-30T15:29:56Z","region":"eu-west-1","resources":["arn:aws:codepipeline:eu-west-1:803700595459:AnsiblePipeline"],"detail":{"pipeline":"AnsiblePipeline","execution-id":"20567b42-c2ef-4a39-9e87-3e69f7ce5199","state":"STARTED","version":7.0}}', 'Timestamp': '2020-03-30T15:29:59.553Z', 'SignatureVersion': '1', 'Signature': 'luVpklCprnLD+YvQbQbU401vFQHEvbZn8QltFXGdY3KEKeABIuu34XCUqqE/6rLni8mf14V8I+pHFysbEm6mjY1+Cl+ePpYuiZ32CHx7ofQnTJE5aZewFI1wxsJMH0/wPXnGkcExzj4LQTlkG5u9ap1eJ78aniFHvNyicx8YpaYIv/XH73jQF6qBMjDKXOTfECAeTqaSpfFmNBByHmm+A4a01miPDL6f/q3O7Cvc6PhhfsvSQV7lQpFQVTXAZwikyUXe5lMarvMjrCj0NbKo4AU7UzwVG/Q45NJTUdJWpnmEvMSWSB7/zYkQuo/SaSD1nFSGVYdejizN4I1L2qfgbA==', 'SigningCertUrl': 'https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-a86cb10b4e1f29c941702d737128f7b6.pem', 'UnsubscribeUrl': 'https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-1:803700595459:OpsGenieCoreHAProxyPipelineTopic:39c1da1a-3d23-4065-90b5-3a9536c8db1c', 'MessageAttributes': {}}}]}
    message = event['Records'][0]['Sns']['Message']
    print(message)
    results = json.loads(message)
    message_dict = results
    print(message_dict.values())
    #['0', 'dd93259d-579f-43c4-9cb2-6021293efce7', 'CodePipeline Pipeline Execution State Change', 'aws.codepipeline', '803700595459', '2020-03-30T15:29:56Z', 'eu-west-1', ['arn:aws:codepipeline:eu-west-1:803700595459:AnsiblePipeline'], {'pipeline': 'AnsiblePipeline', 'execution-id': '20567b42-c2ef-4a39-9e87-3e69f7ce5199', 'state': 'STARTED', 'version': 7.0}]
    print(message_dict['detail'])
    pipe_details = (message_dict['detail'])
    print(pipe_details)
    #{'pipeline': 'AnsiblePipeline', 'execution-id': '20567b42-c2ef-4a39-9e87-3e69f7ce5199', 'state': 'STARTED', 'version': 7.0}
    states = ['STARTED','SUCCEEDED','FAILED']
    for key, value in pipe_details.items():
        if value in states:
            print(f"THIS IS WORKING TEST {value}")
            alert_subject = f"Core HA Proxy Pipeline has {value}"
            alert_message = message
            send_sns_alert(subject=alert_subject,message=alert_message)
        elif value not in states:
            print(f"NOT WORKING State {value} ignored - see pipeline for more details")