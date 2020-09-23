import os
import boto3
from botocore.exceptions import ClientError

# TOPIC = os.environ['TOPICARN']
TOPIC = 'test'

"""Including sample event to prove functions can mutate the right parts of the message"""
event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:eu-west-1:803700595459:OpsGenieCoreHAProxyPipelineTopic:39c1da1a-3d23-4065-90b5-3a9536c8db1c', 'Sns': {'Type': 'Notification', 'MessageId': '703b2686-70d3-51fe-bd27-707a62649ec7', 'TopicArn': 'arn:aws:sns:eu-west-1:803700595459:OpsGenieCoreHAProxyPipelineTopic', 'Subject': None, 'Message': '{"version":"0","id":"dd93259d-579f-43c4-9cb2-6021293efce7","detail-type":"CodePipeline Pipeline Execution State Change","source":"aws.codepipeline","account":"803700595459","time":"2020-03-30T15:29:56Z","region":"eu-west-1","resources":["arn:aws:codepipeline:eu-west-1:803700595459:AnsiblePipeline"],"detail":{"pipeline":"AnsiblePipeline","execution-id":"20567b42-c2ef-4a39-9e87-3e69f7ce5199","state":"STARTED","version":7.0}}', 'Timestamp': '2020-03-30T15:29:59.553Z', 'SignatureVersion': '1', 'Signature': 'luVpklCprnLD+YvQbQbU401vFQHEvbZn8QltFXGdY3KEKeABIuu34XCUqqE/6rLni8mf14V8I+pHFysbEm6mjY1+Cl+ePpYuiZ32CHx7ofQnTJE5aZewFI1wxsJMH0/wPXnGkcExzj4LQTlkG5u9ap1eJ78aniFHvNyicx8YpaYIv/XH73jQF6qBMjDKXOTfECAeTqaSpfFmNBByHmm+A4a01miPDL6f/q3O7Cvc6PhhfsvSQV7lQpFQVTXAZwikyUXe5lMarvMjrCj0NbKo4AU7UzwVG/Q45NJTUdJWpnmEvMSWSB7/zYkQuo/SaSD1nFSGVYdejizN4I1L2qfgbA==', 'SigningCertUrl': 'https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-a86cb10b4e1f29c941702d737128f7b6.pem', 'UnsubscribeUrl': 'https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-1:803700595459:OpsGenieCoreHAProxyPipelineTopic:39c1da1a-3d23-4065-90b5-3a9536c8db1c', 'MessageAttributes': {}}}]}
# message = event['Records'][0]['Sns']['Message']
# print(message)
# state = message
# print(state)

def send_sns_alert(subject,message,topicarn=TOPIC):
    """Create connection to aws SNS service"""
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
    message = event['Records'][0]['Sns']['Message']
    print(message)
    # message = "StackId='arn:aws:cloudformation:eu-west-1:086884017483:stack/cfn-alert-test/59b706d0-3952-11ea-b8af-0a79771fa9ee'\nTimestamp='2020-01-17T17:54:04.453Z'\nEventId='59b7ca20-3952-11ea-b8af-0a79771fa9ee'\nLogicalResourceId='cfn-alert-test'\nNamespace='086884017483'\nPhysicalResourceId='arn:aws:cloudformation:eu-west-1:086884017483:stack/cfn-alert-test/59b706d0-3952-11ea-b8af-0a79771fa9ee'\nPrincipalId='AROAIXMJPWJEJ24HXV5UQ:BertieVoros'\nResourceProperties='null'\nResourceStatus='CREATE_FAILED'\nResourceStatusReason='User Initiated'\nResourceType='AWS::CloudFormation::Stack'\nStackName='cfn-alert-test'\nClientRequestToken='Console-CreateStack-18efed3e-26c0-527a-ae7d-196a1b63ecf3'\n"
    # Removes new line at the end of the message string.
    message_cleaned = message.rstrip('\n')
    # Splits message string by the newline characters.
    message_parts = message_cleaned.split('\n')
    message_dict = {}
    status_detail = ['STARTED', 'SUCCEEDED', 'FAILED']
    
    # Parse message string and process into a dictionary for ease of use.
    # Turns each line into a key value pair and stores them in a dictionary.
    for part in message_parts:
        splitparts = part.split('=')
        # Removes quotes and double quotes.
        key = splitparts[0].strip('\"\'')
        value = splitparts[1].strip('\"\'')
        message_dict[key] = value
    
    if message_dict['status'] in status_detail:
        print('status')
        # Alert needs to be raised.
        # Example: 'StackName: DELETE_FAILED'
    #     alert_subject = '{}: {}'.format(message_dict['StackName'],
    #                                     message_dict['ResourceStatus'])
    #     alert_message = message
    #     send_sns_alert(subject=alert_subject,message=alert_message)
    # elif message_dict['ResourceStatus'] in OKSTATUS:
    #     print(message_dict['StackName'],message_dict['ResourceType'],message_dict['ResourceStatus'])
