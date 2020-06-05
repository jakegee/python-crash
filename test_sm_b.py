#!/usr/bin/env python3
"""Implements functions to be used from R to access AWS resources."""
import sys
import json
import boto3
import socket
import base64
import requests
from datetime import datetime
from botocore.exceptions import ClientError

inAws = False

# try:
#     whereami = requests.get('http://169.254.169.254/latest/dynamic/instance-identity/document',timeout=0.1)
#     if whereami.status_code is 200:
#         responseDataDict = json.loads(whereami.text)
#         REGION = responseDataDict['region']
#         inAws = True
# except requests.exceptions.Timeout:
#     inAws = False
# except requests.exceptions.RequestException as e:
#     inAws = False


# def in_aws():
#     """Check local ip address agains set list."""
#     try:
#         host_name = socket.gethostname()
#         ip_address = socket.gethostbyname(host_name)
#     except OSError as msg:
#         return 'error'

#     IPRANGES = ['10.25.0.0','10.26.0.0']
#     OCTETS = []

#     if ip_address != 'error':
#         mySecondOctet = ip_address.split('.')[1]
#         # collect second octets into list
#         # for easy comparison
#         for iprange in IPRANGES:
#             secondOctet = iprange.split('.')[1]
#             OCTETS.append(secondOctet)
#         # compare second octet of ip addresses
#         # we are in AWS if the second octet matches
#         if mySecondOctet in OCTETS:
#             return('yes')
#         else:
#             return('no')


# def get_aws_role_credentials(keyid,
#                              accesskey,
#                              mfadevice,
#                              mfacode,
#                              region='eu-west-1'):
#   """Get role credentials."""
#   session = boto3.session.Session(region_name=region,
#                                   aws_access_key_id=keyid,
#                                   aws_secret_access_key=accesskey)
#   sts_client = session.client('sts')
#   assumed_role_object=sts_client.assume_role(
#     RoleArn="arn:aws:iam::086884017483:role/am-ds-infra-human",
#     RoleSessionName="AssumeRoleSession1",
#     SerialNumber=mfadevice,
#     TokenCode=mfacode
#   )

#   cerdentials=assumed_role_object['Credentials']
#   # The following three lines change the date format
#   # to one that can be converted to datetime in R
#   expirationDate = cerdentials['Expiration']
#   dateFormattedForR = expirationDate.strftime("%d-%m-%Y %H:%M:%S")
#   cerdentials['Expiration'] = dateFormattedForR
#   return cerdentials


def get_secret(secretname, **kwargs):
    """Retrieve secret from AWS Secrets Manager."""
    if len(kwargs) == 0 and inAws:
        """When in AWS."""
        session = boto3.session.Session(region_name=REGION)
        client = session.client('secretsmanager')

    elif len(kwargs) == 4 and inAws == False:
        """When not in AWS and MFA has to be used."""
        session = boto3.session.Session(region_name=kwargs['region'],
                                        aws_access_key_id=kwargs['aws_access_key_id'],
                                        aws_secret_access_key=kwargs['aws_secret_access_key'],
                                        aws_session_token=kwargs['aws_session_token'])
  
        client = session.client('secretsmanager')

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secretname
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            resultJson = secret
            resultDict = json.loads(resultJson)
            return resultDict[secretname]
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret

print(get_secret('talk'))


# def list_R_servers(**kwargs):
#     """List running R servers."""
#     if len(kwargs)  == 0 and inAws:
#         """When in AWS."""
#         session = boto3.session.Session(region_name=REGION)
#         client = session.client('ec2')

#     elif len(kwargs) == 4 and inAws == False:
#         session = boto3.session.Session(region_name=kwargs['region'],
#                                         aws_access_key_id=kwargs['aws_access_key_id'],
#                                         aws_secret_access_key=kwargs['aws_secret_access_key'],
#                                         aws_session_token=kwargs['aws_session_token'])

#         client = session.client('ec2')

#     filters = [{'Name': 'tag:Name', 'Values': ['R-Server','RServer_by_Rundeck']},
#                 {'Name': 'instance-state-name', 'Values': ['running']}]
#     try:
#         response = client.describe_instances(Filters=filters)
#         instances = response['Reservations']
#     except ClientError as e:
#         print(e.response['Error']['Message'])
#         sys.exit(0)
    
#     allinstances = []

#     for item in instances:
#         instance = item['Instances'][0]
#         for tag in instance['Tags']:
#             if tag['Key'] == 'aws:cloudformation:stack-name':
#                 stackname = tag['Value']
#                 thisInstance = {'stackname': stackname,
#                                 'type': instance['InstanceType'],
#                                 'address': instance['PrivateIpAddress'],
#                                 'id': instance['InstanceId']}
#                 allinstances.append(thisInstance)
        
#     return allinstances


# def launch_r_server(stackname,
#                     daystorun,
#                     instancetype,
#                     username,
#                     password,
#                     emailaddress,
#                     disksize='218',
#                     script='No script',
#                     **kwargs):
#     """Create CloudFormation stack."""
#     if len(kwargs) == 0 and inAws:
#         session = boto3.session.Session(region_name=REGION)
#         client = session.client('cloudformation')

#     elif len(kwargs) == 4 and inAws == False:
#         session = boto3.session.Session(region_name=kwargs['region'],
#                                         aws_access_key_id=kwargs['aws_access_key_id'],
#                                         aws_secret_access_key=kwargs['aws_secret_access_key'],
#                                         aws_session_token=kwargs['aws_session_token'])
#         client = session.client('cloudformation')


#     templateurl = 'https://s3-eu-west-1.amazonaws.com/argus-cloudformation-templates-eu/datascience/rServer_by_Rundeck.yml'
#     response = client.create_stack(
#         StackName=stackname,
#         TemplateURL=templateurl,
#         Parameters=[
#         {
#             'ParameterKey': 'DaysToRun',
#             'ParameterValue': daystorun
#         },
#         {
#             'ParameterKey': 'InstanceType',
#             'ParameterValue': instancetype
#         },
#         {
#             'ParameterKey': 'diskSize',
#             'ParameterValue': disksize
#         },
#         {
#             'ParameterKey': 'Username',
#             'ParameterValue': username
#         },
#         {
#             'ParameterKey': 'Password',
#             'ParameterValue': password
#         },
#         {
#             'ParameterKey': 'emailAddress',
#             'ParameterValue': emailaddress
#         },
#         {
#             'ParameterKey': 'scriptKey',
#             'ParameterValue': script
#         }
#         ],
#     )

#     return response

# def delete_R_server(stackname,
#                     **kwargs):
#     """Delete a Cloudformation stack by name."""
#     if len(kwargs) == 0 and inAws:
#         session = boto3.session.Session(region_name=REGION)
#         client = session.client('cloudformation')

#     elif len(kwargs) == 4 and inAws == False:
#         session = boto3.session.Session(region_name=kwargs['region'],
#                                         aws_access_key_id=kwargs['aws_access_key_id'],
#                                         aws_secret_access_key=kwargs['aws_secret_access_key'],
#                                         aws_session_token=kwargs['aws_session_token'])
#         client = session.client('cloudformation')
#     response = client.delete_stack(StackName=stackname)
#     response = client.describe_stacks(StackName=stackname)
#     for stack in response['Stacks']:
#         status = '{}:{}'.format(stack['StackName'],
#                                 stack['StackStatus'])
#         return status